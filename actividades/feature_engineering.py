# -*- coding: utf-8 -*-
"""feature engineering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iPMST07hzgHosipauSUM4QurxhOLwCcm
"""



"""#feature engineering

en la ingeniería de características se busca el escalamiento de las variables para manejar mejor las variables, a su vez se hace el cambio de variables categóricas a numéricas.
"""

#importamos librerias
import sklearn.preprocessing  as MinMaxScaler
import pandas as pd

#importamos .csv
data_emissions=pd.read_csv("Emissions_Canada_CO2.csv")

data_emissions

"""#Escalado de características numéricas
Características numéricas a escalar:
- Engine Size(L)
- Cylinders
- Fuel Consumption city (L/100KM)
- Fuel Consumption Hwy (L/100KM)
- Fuel Consumption cicombty (L/100KM)
- CO2 Emissions (g/km)
"""

# se seleccionan las columnas numericas del dataset que tienen una relacion directa,
#no es necesario incluir aquellas columnas numericas cuya media es muy especifica y propia

numerical_features=["Engine Size(L)",
                    "Cylinders",
                    "Fuel Consumption City (L/100 km)",
                    "Fuel Consumption Hwy (L/100 km)",
                    "Fuel Consumption Comb (L/100 km)",
                    "CO2 Emissions(g/km)"]

#escalamiento de columnas
#se hace el escalado por medio del MinMaxScaler que ajusta los valores que esten entre 0 y 1.

scaler = preprocessing.MinMaxScaler()
data_emissions[numerical_features] = scaler.fit_transform(data_emissions[numerical_features])

#print dataframe

print ("Características escaladas:")
data_emissions

"""## Codificación de variables categóricas
variables categóricas a codificar:
- Transmission
- Fuel type
- vehicle Class
"""

#controlarnique_count = data_emissions["Vehicle Class"].nunique()
fuel_type_unique_count = data_emissions["Fuel Type"].nunique()

print(f"Valores únicos en 'Transmission': {transmission_unique_count}")
print(f"Valores únicos en 'Vehicle Class': {vehicle_class_unique_count}")
print(f"Valores únicos en 'Fuel Type': {fuel_type_unique_count}")

#esta operación es útil cuando se quiere comprobar que el número de columnas mínimas generadas si corresponden
# a la variabilidad de los valores del dataset

#convertir las columnas categóricas a tipo "category" para asegurar que pandas las trate correctamente

categorical_columns=["Vehicle Class","Fuel Type","Transmission"]
for col in categorical_columns:
  data_emissions[col] = data_emissions[col].astype("category")

#Aplicar One-hot Encoding sin eliminar la primera categoría (drop_first=False)

data_encoded= pd.get_dummies(data_emissions,columns=categorical_columns,drop_first=False) #el drop_first=False se hace por que usualmente la primera fila la deja en valores de 0

data_encoded

#convertimos solo las columnas de Onehot enconding a 0 y 1

encoded_columns=data_encoded.columns.difference(data_emissions.columns)
data_encoded[encoded_columns]=data_encoded[encoded_columns].astype(int)

data_encoded

print ("comprobación primeros 10 datos transformados por Onehot enconding :")
data_encoded[["Vehicle Class_COMPACT", "Transmission_AS8", "Transmission_AS9"]].head(10)

#Verificar el número de columnas generadas por encoding
print ("numero de columnas generadas or OneHot Encoding", len(data_encoded.columns))

#se comprueba que el número es correcto
#-cantidad de valores distintos en la columna "Transmission:27
#-cantidad de valores distintos en la columna "Vehicle Class:16
#-cantidad de valores distintos en la columna "Fuel Type:5
#da un total de 48 más 9 columnas de resto del dataset, para un total de 57 columnas generadas

print(data_encoded.head())

"""##Creación característica: Eficiencia Relativa"""

#Creamos la nueva característica de eficiencia relativa
data_emissions['Relative Efficiency']=data_emissions['Fuel Consumption Comb (L/100 km)']/data_emissions['CO2 Emissions(g/km)']

#Imprimimos el dataframe con la nueva característica para verificar el resultado
print ("DataFrame con la nueva característica:")
data_emissions

"""#Feature Selecction

"""

#seleccionamos columnas númericas
numerical_data=data_emissions.select_dtypes(include=['float64','int64'])

#Calcular la matriz de correlación con solo columnas numericas

correlation_matrix=numerical_data.corr()
#mostramos correlación de cada característica con "CO Emissions(g/km)"
if ("CO2 Emissions(g/km)") in correlation_matrix.columns:
  target_correlation = correlation_matrix["CO2 Emissions(g/km)"].sort_values(ascending=False)
  print("Correlación con 'CO2 Emissions(g/km)':")
  print(target_correlation)
else:
  print("La columna 'CO2 Emissions(g/km)' no está presente en el DataFrame.")

# Interpretación de los valores de correlación:
#Valor de correlación	Interpretación
#+1.0	Correlación positiva perfecta
#+0.7 a +0.9	Correlación positiva fuerte
#+0.4 a +0.6	Correlación positiva moderada
#+0.1 a +0.3	Correlación positiva débil
#0	Sin correlación lineal
#-0.1 a -0.3	Correlación negativa débil
#-0.4 a -0.6	Correlación negativa moderada
#-0.7 a -0.9	Correlación negativa fuerte
#-1.0	Correlación negativa perfecta

#mapa de calor
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))  # Ajustar tamaño del gráfico
sns.heatmap(
    correlation_matrix,
    annot=True,                # Mostrar los valores numéricos
    fmt=".2f",                 # Mostrar solo 2 decimales
    cmap="gnuplot",           # Paleta de colores más clara y contrastada
    center=0,                  # Centrar el rango de colores en 0
    linecolor='white',         # Color de las líneas entre celdas
    square=True,               # Cuadrado perfecto en cada celda
    cbar_kws={"shrink": .75}   # Reducir barra de color
)
plt.title("Matriz de Correlación", fontsize=16)
plt.xticks(rotation=45, ha='right')  # Mejorar legibilidad del eje X
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

"""#Umbral de correlación"""

#Umbral de correlación
correlation_threshold= 0.8
#seleccionar características que tengan una correlación absoluta mayor al umbral con "CO2 Emissions(g/km)"
selected_features = target_correlation [abs(target_correlation)>correlation_threshold].index.tolist()
#remover la columna objetivo de la lista de características seleccionadas, ya que no es una caracteristica
selected_features.remove("CO2 Emissions(g/km)")
#crear un nuevo DataFrame con solo las características seleccionadas
data_selected=data_emissions[selected_features]

print ("Características seleccionadas basadas en correlacion con 'CO2 Emissions(g/km)': ")
print (selected_features)
print ("\nDataFrame con características seleccionadas: ")
print (data_selected.head())