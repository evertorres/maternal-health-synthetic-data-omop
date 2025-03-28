#!/bin/bash

# Verificar si se ha pasado el parámetro de población base
if [ $# -lt 3 ]; then
  echo "Por favor, proporciona los parámetros: -p (Población Base) -g (F o M), -a (rango de edades) y la población base"
  exit 1
fi

# Obtener los parámetros de entrada
p_param=$1  # -p, población requerida (entero)
g_param=$2  # -g, el valor de género (F o M)
a_param=$3  # -a, el rango de edades (por ejemplo 20-30)

if [[ "$g_param" != "F" && "$g_param" != "M" ]]; then
  echo "El valor para -g debe ser 'F' o 'M'."
  exit 1
fi

# Diccionario de porcentajes por ciudad
declare -A city_percentages
city_percentages["ANTIOQUIA"]=13.52
city_percentages["ATLANTICO"]=5.30
city_percentages["BOGOTA"]=16.26
city_percentages["BOLIVAR"]=4.32
city_percentages["BOYACA"]=2.57
city_percentages["CALDAS"]=2.09
city_percentages["CAQUETA"]=0.81
city_percentages["CAUCA"]=2.81
city_percentages["CESAR"]=2.48
city_percentages["CORDOBA"]=3.52
city_percentages["CUNDINAMARCA"]=6.32
city_percentages["CHOCO"]=1.03
city_percentages["HUILA"]=2.28
city_percentages["LA GUAJIRA"]=1.86
city_percentages["MAGDALENA"]=2.86
city_percentages["META"]=2.08
city_percentages["NARINO"]=3.02
city_percentages["NORTE DE SANTANDER"]=3.04
city_percentages["QUINDIO"]=1.15
city_percentages["RISARALDA"]=1.90
city_percentages["SANTANDER"]=4.54
city_percentages["SUCRE"]=1.95
city_percentages["TOLIMA"]=2.78
city_percentages["VALLE DEL CAUCA"]=8.58
city_percentages["ARAUCA"]=0.54
city_percentages["CASANARE"]=0.86
city_percentages["PUTUMAYO"]=0.64
city_percentages["ARCHIPIELAGO DE SAN ANDRES"]=0.10
city_percentages["AMAZONAS"]=0.14
city_percentages["GUAINIA"]=0.10
city_percentages["GUAVIARE"]=0.16
city_percentages["VAUPES"]=0.08
city_percentages["VICHADA"]=0.17

# Calcular la suma de los porcentajes
total_percentage=0
for percentage in "${city_percentages[@]}"; do
  total_percentage=$(echo "$total_percentage + $percentage" | bc)
done

# Bucle para ejecutar el comando para cada ciudad
first=true  # Para no agregar --exporter.csv.append_mode=true en el primer comando

# Distribuir el número base proporcionalmente entre las ciudades
for city in "${!city_percentages[@]}"; do
  # Calcular el valor de -p para cada ciudad proporcionalmente a su porcentaje
  percentage=${city_percentages[$city]}
  p_calculated=$(echo "$p_param * $percentage / $total_percentage" | bc)  # Calcula el valor de -p como número entero

  # Si es el primer comando, no agregar --exporter.csv.append_mode=true
  if [ "$first" == true ]; then
    first=false
    # Ejecutar el comando para la primera ciudad (ANTIOQUIA) sin --exporter.csv.append_mode=true
    echo "Ejecutando para $city con -p $p_calculated, -g $g_param, -a $a_param"
    ./run_synthea -k keep_pregnant.json -p $p_calculated -g $g_param -a $a_param "$city"
  else
    # Para el resto de las ciudades, agregar --exporter.csv.append_mode=true
    echo "Ejecutando para $city con -p $p_calculated, -g $g_param, -a $a_param"
    ./run_synthea -k keep_pregnant.json -p $p_calculated -g $g_param -a $a_param "$city" --exporter.csv.append_mode=true
  fi
done