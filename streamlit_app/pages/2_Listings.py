import plotly.express as px
import streamlit as st

from airbnb import data, chart

px.set_mapbox_access_token(
    "pk.eyJ1IjoiYWxqZXNoaXNoZSIsImEiOiJjbGJwaHJiajMwc3pxM3FxaDc4anltemN1In0.XZoRGDAvlJjbC21qfZTJcA")

df = data.load("../results/2022-12-21_02-59-19")
fig = chart.create_chart(df)
st.markdown("# Airbnb listings")
st.plotly_chart(fig)
