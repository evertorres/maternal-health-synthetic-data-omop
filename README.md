# 🤰 Maternal Health in Colombia: Synthetic Data

## 🧪 Descripción

Este repositorio contiene los archivos necesarios para la generación de datos sintéticos relacionados con la salud materna Utilizando [**Synthea**](https://github.com/synthetichealth/synthea) y transformados al estándar [**OMOP CDM (Common Data Model)**](https://ohdsi.github.io/CommonDataModel/index.html)

un pipeline para la generación y procesamiento de datos sintéticos relacionados con la salud materna, utilizando el estándar  Está orientado a la simulación de datos clínicos para pruebas, desarrollo de modelos y análisis sin comprometer datos reales de pacientes.

---


## 🚀 Cómo usar

1. Descargar [Synthea](https://github.com/synthetichealth/synthea)
2. Reemplazar el archivo pregnancy.json en la carpeta `synthea/src/main/resources/modules/`
3. Incluir el arhivo `keep_pregnant.json` en la raiz de la carpeta de Synthea
4. Ejecutar el archivo `generate_synthea_col.sh`
5. Descargar [ETL-Synthea](https://github.com/OHDSI/ETL-Synthea)
6. Reemplazar el archivo `create_states_map.sql` en la carpeta `/inst/sql/sql_server/cdm_version/v540/` y ejecutar.


---

## 📊 Ejemplos de uso

Se generó un dataset sintético de 10.000 pacientes disponible en [Kaggle](https://www.kaggle.com/datasets/evertorres/maternal-health-in-colombia-synthetic-data)

1. En el notebook `simple_eda_cohort_generation.ipynb` se realiza un anális exploratorio de datos simple y se generá la cohorte de pacientes para trabajar la fenotipificación computacional. 
2. En el archivo `main.py` adaptado de [Jonathan Badger y equipo](https://github.com/jbadger3/ml_4_pheno_ooe) se genera el conjunto de características para los modelos de Machine Learning
3. En el notebook `pregnancy_phenotypes.ipynb` se realiza un ejercicio de Machine Learning completo conm los datos sintéticos. 
---

## 📌 Requisitos

- Python >= 3.8
- PostgreSQL (si se desea cargar en una instancia OMOP)
- OMOP CDM V5.4
- Synthea 3.3.0
- ETL-Synthea

---

## 📚 Recursos relacionados

- [Synthea]((https://github.com/synthetichealth/synthea))
- [OMOP CDM Documentation](https://ohdsi.github.io/CommonDataModel/)
- [ETL-Synthea](https://github.com/OHDSI/ETL-Synthea)
- [OHDSI Tools](https://www.ohdsi.org/)

---

## 🤝 Contribuciones

¡Contribuciones son bienvenidas! Por favor abre un issue o un pull request.

---

## Agradecimientos: 

## **Agradecimientos**  

Este conjunto de datos fue desarrollado con financiación del **Centro Latinoamericano de Inteligencia Artificial ([CLIAS](https://clias.iecs.org.ar/))**, dentro del proyecto **"Fenotipos Computacionales de Morbilidad Materna mediante Inteligencia Artificial" (ID 82).**  

<table>
  <tbody><tr>
    <td>
      <img src="https://cdn.prod.website-files.com/5d66946a1b07767aacb25958/5d66a65a071de8b2d1f132e0_Logo%20v5%20t-n.png", width = '60%'>
    </td>
    <td>
      <img src="https://clias.iecs.org.ar/wp-content/uploads/2023/04/logo2-1.png", width = '50%'>
    </td>
  </tr>
  <tr>
    <td><strong><a href="https://www.netux.com/">Netux SAS</a></strong></td>
    <td><strong><a href="https://clias.iecs.org.ar/">CLIAS</a></strong></td>
  </tr>
</tbody></table>

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
