if object_id('@cdm_schema.states_map', 'U')  is not null drop table @cdm_schema.states_map;

create table @cdm_schema.states_map(state varchar(50),state_abbreviation varchar(2));

INSERT INTO @cdm_schema.states_map (state, state_abbreviation)
VALUES
    ('AMAZONAS', 'AM'),
    ('ANTIOQUIA', 'AN'),
    ('ARAUCA', 'AR'),
    ('ARCHIPIELAGO DE SAN ANDRES', 'SI'),
    ('ATLANTICO', 'AT'),
    ('BOLIVAR', 'BL'),
    ('BOYACA', 'BY'),
    ('CALDAS', 'CL'),
    ('CAQUETA', 'CQ'),
    ('CASANARE', 'CS'),
    ('CAUCA', 'CA'),
    ('CESAR', 'CE'),
    ('CHOCO', 'CH'),
    ('CORDOBA', 'CO'),
    ('CUNDINAMARCA', 'CU'),
    ('GUAINIA', 'GU'),
    ('GUAVIARE', 'GV'),
    ('HUILA', 'HU'),
    ('LA GUAJIRA', 'LG'),
    ('MAGDALENA', 'MA'),
    ('META', 'ME'),
    ('NARINO', 'NA'),
    ('NORTE DE SANTANDER', 'NO'),
    ('PUTUMAYO', 'PU'),
    ('QUINDIO', 'QU'),
    ('RISARALDA', 'RI'),
    ('SANTANDER', 'SA'),
    ('SUCRE', 'SC'),
    ('TOLIMA', 'TO'),
    ('VALLE DEL CAUCA', 'VC'),
    ('VAUPES', 'VA'),
    ('VICHADA', 'VI'),
    ('BOGOTA', 'BO');