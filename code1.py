import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

# CSS to inject contained in a string
css = """
<style>
    html, body, [class^="css"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .stButton>button {
        color: #ffffff !important;
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
    }
    /* Eliminar el relleno del contenedor principal */
    .reportview-container .main .block-container{
        padding: 0px;
        max-width: none;
    }
    /* Opcional: ajustar el relleno y márgenes de otros elementos si es necesario */
    .reportview-container .main {
        color: #ffffff;
        background-color: #000000;
    }
    .reportview-container {
        background: #000000;
    }
    /* Ajustar el ancho de la barra lateral si es necesario */
    .sidebar .sidebar-content {
        width: 300px;
        background-color: #000000;
    }
    .reportview-container .main .block-container{
        background-color: #000000;
    }
    .reportview-container .main {
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #000000;
    }
    header .decoration {
        background-color: #000000;
    }
    /* Ajustar max-width basándose en atributos que no cambian */
    
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.title('Monitoreo de calidad de aire QAIRA')
st.info('El presente dashboard contiene información de variables usadas para monitorear la calidad del aire durante el mes de Junio 2021 en el Ovalo de Miraflores - Lima, Perú.', icon="ℹ️")

@st.cache_data
def load_data():
    try:
        # Leer el archivo Excel
        data = pd.read_excel(rf"https://www.datosabiertos.gob.pe/sites/default/files/13_Monitoreo_Junio_2021.xlsx")

        # Nombres de las nuevas cabeceras
        new_headers = [
            "ID", "CODIGO DE LA ENTIDAD", "CODIGO UBIGEO INEI", "CODIGO PAIS", 
            "NOMBRE DE LA UO", "Fecha", "CO", "H2S", 
            "NO2", "O3", "PM10", "PM2.5", 
            "SO2", "Ruido (dB)", "UV", "Humedad (%)", 
            "Latitud", "Longitud", "Presion (Pa)", "Temperatura (C)"
        ]

        # Reemplazar las cabeceras existentes
        data.columns = new_headers

        # Establecer la columna 'ID' como el índice del DataFrame
        data.set_index('ID', inplace=True)

        return data
    except Exception as e:
        st.error(f"Error al cargar la data: {e}")
        return pd.DataFrame()
df = load_data()




presion_mean = df['Presion (Pa)'].mean()
temp_mean = df['Temperatura (C)'].mean()
hum_mean = df['Humedad (%)'].mean()

presion_mean = round(presion_mean, 1)
temp_mean = round(temp_mean, 1)
hum_mean = round(hum_mean, 1)

st.markdown('<h3 style="color:white;">Principales KPI del dataset (Valor Promedio)</h3>', unsafe_allow_html=True)
    # Usar st.beta_columns para mostrar los gráficos uno al lado del otro
col1, col2 , col3= st.columns(3)
with col1:
        
        
        st.metric(label=":orange[Presión (Pa)]", value=presion_mean)

with col2:
        st.metric(label=":orange[Temperatura (C)]", value=temp_mean)

with col3:
        st.metric(label=":orange[Humedad (%)]", value=hum_mean)

st.divider()
################################# GRÁFICO 1: Promedio de las variables contaminantes #################################


pollutants = ['H2S', 'NO2', 'O3', 'PM10', 'PM2.5', 'SO2']


pollutants_mean = df[pollutants].mean().sort_values(ascending=False)

# Configurar el estilo de seaborn
sns.set(style="whitegrid")

# Crear el gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))


bar_plot = sns.barplot(x=pollutants_mean.index, y=pollutants_mean.values, palette="Blues_r")

# Añadir etiquetas encima de cada barra
for index, value in enumerate(pollutants_mean.values):
    bar_plot.text(index, value + 0.5, round(value, 2), ha='center', va='bottom', fontsize=10)

# Configurar el estilo del gráfico
ax.set(ylabel='Promedio (ug/m3)', xlabel='Contaminantes')
st.markdown('<h3 style="color:white;">1. Promedio de las variables contaminantes</h3>', unsafe_allow_html=True)
ax.title.set_fontsize(20)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)


st.divider()
################################# GRÁFICO 2: Líneas de tendencia para Humedad, Presión y Temperatura por Día #################################

st.markdown('<h3 style="color:white;">2. Lineas de tendencia para Humedad, Presión y Temperatura por Día</h3>', unsafe_allow_html=True)

df['Fecha'] = pd.to_datetime(df['Fecha'])
daily_means = df.set_index('Fecha').resample('D')[['Humedad (%)', 'Presion (Pa)', 'Temperatura (C)']].mean()

# Asignar una fecha por defecto
default_date = pd.to_datetime('2021-06-01')
default_date2 = pd.to_datetime('2021-06-30')

# Crear el widget date_input para seleccionar el rango de fechas
date_range = st.date_input('Seleccione un rango de fechas', 
                           min_value=df['Fecha'].min(), 
                           max_value=df['Fecha'].max(), 
                           value=(default_date, default_date2),
                           key='date_range_1')

# Obtener las fechas de inicio y fin del rango seleccionado
if len(date_range) == 2:
    start_date, end_date = date_range

    # Filtrar el DataFrame según el rango de fechas seleccionado
    filtered_data = daily_means.loc[start_date:end_date]
    st.write("\n")
    st.write("\n")
    st.write('##### Humedad Promedio por Día')
    
    # Use Streamlit's columns to create a two-column layout
    left_column, right_column = st.columns([1, 3])

    # Place the slider in the left column
    with left_column:
        max_humedad = filtered_data['Humedad (%)'].max()
        min_humedad = filtered_data['Humedad (%)'].min()
        y_axis_scale = st.slider(f'Porcerntaje de Temperatura', min_value=min_humedad-5, max_value=max_humedad+5, value=(min_humedad-5,max_humedad+5))
        text_markdown_H = f'<p style="color:white;">El valor máximo de porcentaje de Humedad fue {max_humedad:.2f}% y el valor mínimo fue {min_humedad:.2f}% </p>'
        st.markdown(text_markdown_H, unsafe_allow_html=True)
    with right_column:
    
        #st.line_chart(filtered_data, use_container_width=True, height=400, key='custom_chart', y_axis_scale=(0, y_axis_scale))
        chart = alt.Chart(filtered_data['Humedad (%)'].reset_index()).mark_line(strokeWidth=3).encode(
            x='Fecha:T',
            y=alt.Y('Humedad (%)', scale=alt.Scale(domain=[y_axis_scale[0],y_axis_scale[1]])),
        )

        st.altair_chart(chart, use_container_width=True)
        st.write("\n") 


    st.write('##### Presión Promedio por Día')
    left_column2, right_column2 = st.columns([1, 3])
    with left_column2:
        max_presion = filtered_data['Presion (Pa)'].max()
        min_presion = filtered_data['Presion (Pa)'].min()
        y_axis_scale2 = st.slider(f'Presión (Pa)', min_value=min_presion-5, max_value=max_presion+5, value=(min_presion-5,max_presion+5))
        text_markdown_P = f'<p style="color:white;">El valor máximo de porcentaje de Presión fue {max_presion:.2f} y el valor mínimo fue {min_presion:.2f}</p>'
        st.markdown(text_markdown_P, unsafe_allow_html=True)
        
    
    with right_column2:
        chart2 = alt.Chart(filtered_data['Presion (Pa)'].reset_index()).mark_line(strokeWidth=3).encode(
            x='Fecha:T',
            y=alt.Y('Presion (Pa)', scale=alt.Scale(domain=[y_axis_scale2[0], y_axis_scale2[1]])),
        )
        st.altair_chart(chart2, use_container_width=True)
        st.write("\n") 

    st.write('##### Temperatura Promedio por Día')
    left_column3, right_column3 = st.columns([1, 3])
    with left_column3:
        max_temperatura = filtered_data['Temperatura (C)'].max()
        min_temperatura = filtered_data['Temperatura (C)'].min()
        y_axis_scale3 = st.slider(f'Temperatura', min_value=min_temperatura-5, max_value=max_temperatura+5, value=(min_temperatura-5,max_temperatura+5))
        text_markdown_T = f'<p style="color:white;">El valor máximo de porcentaje de Temperatura fue {max_temperatura:.2f} °C y el valor mínimo fue {min_temperatura:.2f} °C</p>'
        st.markdown(text_markdown_T, unsafe_allow_html=True)
    
    with right_column3:
        chart3 = alt.Chart(filtered_data['Temperatura (C)'].reset_index()).mark_line(strokeWidth=3).encode(
            x='Fecha:T',
            y=alt.Y('Temperatura (C)', scale=alt.Scale(domain=[y_axis_scale3[0], y_axis_scale3[1]])),
        )
        st.altair_chart(chart3, use_container_width=True)
    
else:
    st.error("Debe colocar un rango de fechas válido")

st.divider()

################################# GRÁFICO 3: Mapa de Calor de Temperatura por Día de la semana y Hora #################################
# Establecer el idioma a español

st.markdown('<h3 style="color:white;">3. Mapa de Calor de Temperatura por Día de la semana y Hora</h3>', unsafe_allow_html=True)
temperature_pivot = df.pivot_table(
    values='Temperatura (C)', 
    index=df['Fecha'].dt.hour, 
    columns=df['Fecha'].dt.day_name(),
    aggfunc='mean'
)

day_names_es = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
temperature_pivot.columns = [day_names_es[col] for col in temperature_pivot.columns]

# Ordenar los días de la semana
ordered_days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
temperature_pivot.columns = pd.CategoricalIndex(temperature_pivot.columns, categories=ordered_days, ordered=True)
temperature_pivot = temperature_pivot.sort_index(axis=1)


plt.figure(figsize=(12, 15))
sns.heatmap(temperature_pivot, cmap='coolwarm', annot=True, fmt=".1f")
plt.xlabel('Día de la semana')
plt.ylabel('Hora')
st.pyplot(plt)

dfS5 = df.set_index('Fecha')
st.divider()

#################################  Mostrar dataset #################################


st.markdown('<h3 style="color:white;">4. Dataset calidad de aire QAIRA Junio 2021 </h3>', unsafe_allow_html=True)
st.write(df)
st.link_button("Ir al dataset",  "https://www.datosabiertos.gob.pe/dataset/monitoreo-de-calidad-de-aire-qaira%C2%A0-municipalidad-de-miraflores/resource/5ccaf849-33a6-46ff")

st.divider()


################################# GRÁFICO 5: Variación Diaria de Humedad, Presión y Temperatura #################################
st.markdown('<h3 style="color:white;">5. Variación Diaria de Humedad, Presión y Temperatura</h3>', unsafe_allow_html=True)

# Crear el widget date_input para seleccionar el rango de fechas
date_range_variation = st.date_input('Seleccione el rango de fechas para la variación diaria', 
                                     min_value=df['Fecha'].min(), 
                                     max_value=df['Fecha'].max(), 
                                     value=(default_date, default_date2))

# Obtener las fechas de inicio y fin del rango seleccionado
start_date_variation, end_date_variation = date_range_variation

# Filtrar el DataFrame según el rango de fechas seleccionado
df2 = df.set_index('Fecha')
evolution_data_variation = df2.loc[start_date_variation:end_date_variation]

# Calcular la variación diaria para Humedad, Presión y Temperatura
evolution_data_variation['Variacion Humedad'] = evolution_data_variation['Humedad (%)'].diff()
evolution_data_variation['Variacion Presion'] = evolution_data_variation['Presion (Pa)'].diff()
evolution_data_variation['Variacion Temperatura'] = evolution_data_variation['Temperatura (C)'].diff()

# Configurar el estilo de seaborn
sns.set(style="whitegrid")

# Crear el gráfico de líneas
fig_variation, ax_variation = plt.subplots(figsize=(10, 6))

# Formatear las fechas para mostrar solo el día del mes
evolution_data_variation['Dia_Mes'] = evolution_data_variation.index.strftime('%d')

# Graficar la variación diaria de la humedad
sns.lineplot(x='Dia_Mes', y='Variacion Humedad', data=evolution_data_variation, label='Variación Humedad', ax=ax_variation)

# Graficar la variación diaria de la presión
sns.lineplot(x='Dia_Mes', y='Variacion Presion', data=evolution_data_variation, label='Variación Presión', ax=ax_variation)

# Graficar la variación diaria de la temperatura
sns.lineplot(x='Dia_Mes', y='Variacion Temperatura', data=evolution_data_variation, label='Variación Temperatura', ax=ax_variation)

# Configurar las etiquetas y el título
ax_variation.set(xlabel='Día del Mes', ylabel='Variación Diaria', title='Variación Diaria de Humedad, Presión y Temperatura')
ax_variation.legend()

# Mostrar el gráfico en Streamlit
st.pyplot(fig_variation)
    

st.divider()


########################################################################################
