import plotly.express as px
import streamlit as st

import airbnb.data as data
import airbnb.chart
import airbnb.per_city as per_city

px.set_mapbox_access_token(
    "pk.eyJ1IjoiYWxqZXNoaXNoZSIsImEiOiJjbGJwaHJiajMwc3pxM3FxaDc4anltemN1In0.XZoRGDAvlJjbC21qfZTJcA")


df = data.load("../results/2022-12-21_02-59-19"). \
    pipe(per_city.filter_price, treshold=50). \
    pipe(per_city.group_per_city)



fig = airbnb.chart.create_per_city_chart(df)

st.markdown("# Airbnb listings")
st.dataframe(df)
st.plotly_chart(fig)
