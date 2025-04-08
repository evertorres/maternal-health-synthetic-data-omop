import os, argparse, sqlite3, json
from collections import OrderedDict
import pandas as pd
import numpy as np
from tqdm import tqdm
from sqlalchemy import create_engine

def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def construct_demogrpahic_features(example,pt_features_disc,pt_features_cont):
    person_id = example.person_id
    demo_df = pd.read_sql(f'SELECT * from {schema}.person WHERE person_id = {person_id}', engine)
    #each person can have multiple entries in the person table based on the provider and location id
    #just use the first row to collect common information
    demo_df.columns = demo_df.columns.str.lower()
    demos = demo_df.mode().iloc[0]
    dob = demos.birth_datetime
    dob = pd.to_datetime(dob)
    start_pregnancy = example.start_pregnancy
    age_at_pregnancy = int((start_pregnancy - dob).days/365.25)
    age_greater_than_45 = age_at_pregnancy > 45.0
    age_less_than_15 = age_at_pregnancy < 15.0

    #add demographic featrues
    # pt_features_disc['person_gender'] = gender | sólo teenmos mujeres, pero podemos poner algo de la raza
    pt_features_cont['age_at_pregnancy'] = age_at_pregnancy
    pt_features_disc['lt15_person_age'] = age_less_than_15
    pt_features_disc['gt45_person_age'] = age_greater_than_45


def construct_condition_occurrence_features(example, pt_features_disc,pt_features_cont):
    person_id = example.person_id
    start_pregnancy = example.start_pregnancy
    finish_pregnancy = example.finish_pregnancy
    
    query = f'''SELECT *  
                FROM {schema}.condition_occurrence  
                WHERE person_id = {person_id} AND condition_start_date BETWEEN \'{start_pregnancy.strftime('%Y-%m-%d')}\' AND \'{finish_pregnancy.strftime('%Y-%m-%d')}\';
             '''
    results_df = pd.read_sql_query(query, engine)
    results_df.columns = results_df.columns.str.lower()
    results_df['condition_start_date'] = pd.to_datetime(results_df['condition_start_date'])
    results_df.sort_values('condition_concept_id',inplace=True)
    conditions_in_pregnancy_stats = results_df['condition_concept_id'].value_counts()
    
    for concept_id, count in  conditions_in_pregnancy_stats.items():
        pt_features_disc['cnt-cond_CONCEPT_{}'.format(str(concept_id))] = count

def construct_obs_features(example, pt_features_disc,pt_features_cont):
    person_id = example.person_id
    start_pregnancy = example.start_pregnancy
    finish_pregnancy = example.finish_pregnancy
    
    query = f'''SELECT * 
            FROM {schema}.observation  
            WHERE person_id = {person_id} AND observation_date BETWEEN \'{start_pregnancy.strftime('%Y-%m-%d')}\' AND \'{finish_pregnancy.strftime('%Y-%m-%d')}\';
         '''
    results_df = pd.read_sql_query(query, engine)
    results_df.columns = results_df.columns.str.lower()
    results_df['observation_date'] = pd.to_datetime(results_df['observation_date'])

    obs_in_pregnancy_stats = results_df['observation_concept_id'].value_counts()
    
    for concept_id, count in obs_in_pregnancy_stats.items():
        pt_features_disc[f'cnt-obs_CONCEPT_{str(concept_id)}'] = count

def construct_procedures_features(example, pt_features_disc):
    person_id = example.person_id
    start_pregnancy = example.start_pregnancy
    finish_pregnancy = example.finish_pregnancy
    
    # person_id, condition_start_date, condition_end_date, condition_concept_id
    query = f'''SELECT *  
                FROM {schema}.procedure_occurrence  
                WHERE person_id = {person_id} AND procedure_date BETWEEN \'{start_pregnancy.strftime('%Y-%m-%d')}\' AND \'{finish_pregnancy.strftime('%Y-%m-%d')}\';
             '''
    results_df = pd.read_sql_query(query, engine)
    results_df.columns = results_df.columns.str.lower()
    results_df['procedure_date'] = pd.to_datetime(results_df['procedure_date'])
    results_df.sort_values('procedure_concept_id',inplace=True)
 
    pro_in_pregnancy_stats = results_df['procedure_concept_id'].value_counts()
    
    for concept_id, count in pro_in_pregnancy_stats.items():
        pt_features_disc[f'cnt-pro_CONCEPT_{str(concept_id)}'] = count

def construct_device_exposure_features(example, pt_features_disc,pt_features_cont):
    person_id = example.person_id
    start_pregnancy = example.start_pregnancy
    finish_pregnancy = example.finish_pregnancy


    query = f'''SELECT * 
                 FROM {schema}.device_exposure  
                 WHERE person_id = {person_id} AND device_exposure_start_date BETWEEN \'{start_pregnancy.strftime('%Y-%m-%d')}\' AND \'{finish_pregnancy.strftime('%Y-%m-%d')}\';
            '''
    results_df = pd.read_sql_query(query,engine)
    results_df.columns = results_df.columns.str.lower()
    
    if not results_df.empty:
        results_df['device_exposure_start_date'] = pd.to_datetime(results_df['device_exposure_start_date'])
        dev_concepts = results_df['device_concept_id']
    
        for concept_id in dev_concepts:
            pt_features_disc[f'bool-dev_CONCEPT_{str(concept_id)}'] = 1.0

def construct_measurement_features(example, pt_features_disc,pt_features_cont):
    
    person_id = example.person_id
    start_pregnancy = example.start_pregnancy
    finish_pregnancy = example.finish_pregnancy

    query = f'''SELECT concept.concept_name, measurement.*
                FROM {schema}.measurement INNER JOIN {schema}.concept ON measurement.value_as_concept_id = concept.concept_id 
                WHERE person_id = {person_id} AND measurement_date BETWEEN \'{start_pregnancy.strftime('%Y-%m-%d')}\' AND \'{finish_pregnancy.strftime('%Y-%m-%d')}\';
               '''
    results_df = pd.read_sql_query(query, engine)
    results_df.columns = results_df.columns.str.lower()
    results_df['measurement_date'] = pd.to_datetime(results_df['measurement_date'])
    
        
    #filter any NAN
    results_df = results_df[results_df['value_as_number'].notnull()]

    results_df.sort_values('measurement_concept_id',inplace=True)
    
    #continuous features (min,max,mean)
    results_df = results_df.groupby('measurement_concept_id')['value_as_number'].agg(['min','max','mean'])
    
    for row in results_df.iterrows():
        concept_id = row[0]
        measurement_min = row[1]['min']
        measurement_max = row[1]['max']
        measurement_mean = row[1]['mean']

        pt_features_cont[f'min-meas_CONCEPT_{str(concept_id)}'] = measurement_min
        pt_features_cont[f'max-meas_CONCEPT_{str(concept_id)}'] = measurement_max
        pt_features_cont[f'mean-meas_CONCEPT_{str(concept_id)}'] = measurement_mean


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("--db_path", type=str, help="relative path/to/omop.sqlite database")
    parser.add_argument("--examples_path", type=str, help="relative path/to/examples.csv")
    #parser.add_argument("--model_name", type=str, help="model_name")

    args = parser.parse_args()
    assert args.examples_path, 'Please use --examples_path to specify a .csv file containing person_ids and labels'
    #assert args.model_name, 'Please use --model_name and specify base_model_name'

    #model_name = args.model_name
    output_dir = 'OMOP_features'
    make_dir_if_not_exists(output_dir)

    #open connection to sqlite database
    database = '1000_pregnant_db'
    schema = 'cdm_synthea10' #cdmdatabaseschema'

    engine = create_engine( 
    f"postgresql+psycopg2://netux-idi:netux-idi@localhost:5432/{database}") 

    #load exmaples
    examples_df = pd.read_csv(args.examples_path, parse_dates=['start_pregnancy', 'finish_pregnancy'])

    # #add start and end dates for data collection for each example --- ya tendriamos las fechas de inicio y fin
    # examples_df['start_date'] = [(event_date - offset - days_before).strftime('%Y-%m-%d') for event_date in examples_df['dx_date']]
    # examples_df['end_date'] =  [(event_date + days_after).strftime('%Y-%m-%d') for event_date in examples_df['dx_date']]

    #load dictionary of MME conversion data(takes concept_ids for keys)- no lo utilizaremos
    # with open('supporting_files/mme_OMOP.json','r') as fh:
    #     rx_cui_to_mme_dict = json.load(fh)

    features_disc_df = pd.DataFrame()
    features_cont_df = pd.DataFrame()
    
    for example in tqdm(examples_df.itertuples(), total=examples_df.shape[0]):
        pt_features_disc = OrderedDict()
        pt_features_cont = OrderedDict()
        construct_demogrpahic_features(example, pt_features_disc,pt_features_cont)
        construct_condition_occurrence_features(example, pt_features_disc,pt_features_cont)
        construct_measurement_features(example, pt_features_disc,pt_features_cont)
        construct_procedures_features(example,pt_features_disc)
        construct_obs_features(example, pt_features_disc, pt_features_cont)
        construct_device_exposure_features(example, pt_features_disc,pt_features_cont)

        features_disc_df = features_disc_df._append(pt_features_disc,ignore_index=True)
        features_cont_df = features_cont_df._append(pt_features_cont,ignore_index=True)

    features_disc_df.to_csv(os.path.join(output_dir,'omop_features_disc.csv'),index=False)
    features_cont_df.to_csv(os.path.join(output_dir,'omop_features_cont.csv'),index=False)