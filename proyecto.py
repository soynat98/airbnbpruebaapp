# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 20:01:26 2021

@author: natyc
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
import numpy as np
import plotly.express as px

from PIL import Image
image = Image.open('im.png')
st.image(image, caption='Airbnb',
use_column_width=True)


# Para que los datos solo se descarguen una vez
@st.cache
def get_data():
    url = "http://data.insideairbnb.com/mexico/df/mexico-city/2020-12-23/visualisations/listings.csv"
    return pd.read_csv(url)


st.title("Herramientas para el análisis de datos")

st.header("Integrantes: \nNatalia Quijano \n\nValeria Sosa")

st.markdown("### Analisaremos los datos de AIRBNB de México")

dato = get_data()

##Datos sin limpiar
st.warning("Estos son los datos sin limpiar")
dato.shape

dato.isnull().sum()
dato = dato.dropna(subset=["name","host_name","last_review","reviews_per_month"])
dato = dato.drop(columns=['neighbourhood_group'])

##Datos limpios
st.success("Estos son los datos limpios")
dato.shape

dato.isnull().sum()
dato.head()

##tabla
dato = get_data()
st.dataframe(dato.head())
##mapa
st.map(dato)

##1. ##
st.info("¿Qué tipo de alojamiento es el que más hay (cuarto, dept.completo, etc)?")
tipal=dato.room_type.value_counts().head()
tipal

##2. ##
st.info("¿Cuales son los neighbourhood con más alojamientos?")
masal=dato.neighbourhood.value_counts().head()
masal 
dato.neighbourhood.value_counts(normalize=True).plot.barh()

##5##
st.info("Mostrar la distribución de los precios de los alojamientos")
distr =(dato.groupby('price').size())
distr

##5.1##
st.info("Rango de precios ")
values = st.sidebar.slider("Rango de precios", float(dato.price.min()), 3000.0,
                           (200.0, 500.0))

f = px.histogram(dato[(dato.price > int(values[0])) & (dato.price < int(values[1]))],
                 x="price",
                 nbins=15,
                 title="Distribucion de precios")
f.update_xaxes(title="Precio")
f.update_yaxes(title="Cantidad de Neighbourhood")
st.plotly_chart(f)


##6##
st.info("¿Donde se encuentra el alojamiento más caro y el más barato?")
dfCorto=dato[ ["neighbourhood","price"] ]
dfCm=dfCorto.max()
dfCm
dfCmin=dfCorto.min()
dfCmin

##8##
st.info("¿Que cantidad de días se alojan más?")
diasd=dato.minimum_nights.value_counts().head()
diasd
hist_values = np.histogram(dato['minimum_nights'], bins=5, range=(1,5))[0]
st.bar_chart(hist_values)

##9##
st.info("¿Que host tiene más propiedades?")
@st.cache
def contar_hosts(data):
    host_count = pd.DataFrame(dato.groupby('host_id')['id'].count()).sort_values(by='id', ascending=0).id.value_counts()
    host_per = pd.DataFrame(dato.groupby('host_id')['id'].count()).sort_values(by='id', ascending=0).id.value_counts(normalize=True)
    host_total = pd.concat([host_count,host_per], axis=1, keys=['counts', '%'])
    host_total['cantidad propiedades'] = host_total.index
    superhost = host_total[['cantidad propiedades', 'counts', '%']].sort_values(by='cantidad propiedades')
    return superhost

superhost = contar_hosts(dato)
superhost

st.markdown('La anterior información nos muestra los host en la plataforma tienen 1 o 2 departamentos disponibles para renta (**86%** del total),  el mayor de propiedades que tiene un host fue **108** propiedades publicadas.')

##9##
st.info("Precio promedio por tipo de habitacion")
st.table(dato.groupby("room_type").price.mean().reset_index()\
    .round(2).sort_values("price", ascending=False)\
    .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

##10##
st.info("¿El número de reviews afecta cuantas veces se renta un lugar?")
st.write("Ingrese un rango de números en la barra lateral para ver las propiedades cuyo recuento de reseñas se encuentra en ese rango.")
minim = st.sidebar.number_input("Minimo", min_value=0)
maxim = st.sidebar.number_input("Maximo", min_value=0, value=5)
if minim > maxim:
    st.error("Please enter a valid range")
else:
    dato.query("@minim<=number_of_reviews<=@maxim").sort_values("number_of_reviews", ascending=False)\
        .head(50)[["name", "number_of_reviews", "neighbourhood", "availability_365", "price","room_type"]]

st.write("***557, 534, 507***, son los numeros más altos en reviews, estos se encuentran en Venustiano Carranza, con precios de $382, $442, $402, respectivamente. Por lo que podemos deducir que si afecta tanto el precio como los reviews al momento de rentar.")

##11##
st.info("seleccina una columna ")
st.info("De las 16 columnas, es posible que desee ver solo un subconjunto.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
cols = st.multiselect("Columns", dato.columns.tolist(), default=defaultcols)
st.dataframe(dato[cols].head(10))