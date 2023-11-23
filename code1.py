#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Cargar la data 
#eliminé los saltos de línea en los encabezados de data.xlsx
@st.cache
def load_data():
    try:
        data = pd.read_excel(rf"C:\Users\LECP1\streamlit_app\13_Monitoreo_Junio_2021.xlsx")
        return data
    except Exception as e:
        st.error(f"Error al cargar la data: {e}")
        return pd.DataFrame()  

df = load_data()

st.title('Dashboard')

st.write('Raw Data')
st.write(df)

#Gráfico de barras de los contaminantes 
pollutants = ['CO (ug/m3)', 'H2S (ug/m3)', 'NO2 (ug/m3)', 'O3 (ug/m3)', 
              'PM10 (ug/m3)', 'PM2.5 (ug/m3)', 'SO2 (ug/m3)']

pollutants_mean = df[pollutants].mean()
st.write('Average Pollutant Levels')
st.bar_chart(pollutants_mean)

#Lineas de tendencia para Humedad, Presión y Temperatura
st.write('Trend Lines for Humidity, Pressure, and Temperature by Day')

df['Fecha'] = pd.to_datetime(df['Fecha'])
daily_means = df.set_index('Fecha').resample('D')[['Humedad (%)', 'Presion (Pa)', 'Temperatura (C)']].mean()

for column in daily_means.columns:
    st.line_chart(daily_means[column])

#Mapa de Calor de Temperatura (No me muestra)
st.write('Mapa de Calor de Temperatura')

temperature_pivot = df.pivot_table(
    values='Temperatura (C)', 
    index=df['Fecha'].dt.day, 
    columns=df['Fecha'].dt.day_name(),
    aggfunc='mean'
)

plt.figure(figsize=(10, 8))
sns.heatmap(temperature_pivot, cmap='coolwarm', annot=True)
st.pyplot(plt)
