import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_events import plotly_events

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

df=[]
df= pd.DataFrame(df)
df['year']= x
df['lifeExp']= y

fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')

selected_points = plotly_events(fig)
st.write(selected_points)
