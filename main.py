import streamlit as st
import pandas as pd
import numpy as np


st.title("Uber pickups in NYC")

# Buscando dados

DATE_COLUMN ='date/time'
DATA_URL = ("https://s3-us-west-2.amazonaws.com/"
'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Carregando dados')
data = load_data(10000)
data_load_state.text('Carregamento de dados concluido usando cache.')

# inspecionando os dados brutos

#st.subheader("Dados brutos")
#st.write(data)
if st.checkbox('Exibir dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

# construindo um histograma para inspecionar o horario 

st.subheader("Número de corridas por hora")

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24)
)[0]

st.bar_chart(hist_values)

# plotando  dados no mapa

#st.subheader("Plotando os pontos de corrida")
#st.map(data)

hour_to_filter = st.slider("hour", 0, 23, 17) #min:0h, max 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Mapa dos pontos de corrida as {hour_to_filter}:00')
st.map(filtered_data)
