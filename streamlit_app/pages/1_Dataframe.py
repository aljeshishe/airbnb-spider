import streamlit as st

from airbnb import data

df = data.load("../results/2022-12-21_02-59-19")
st.dataframe(df)
