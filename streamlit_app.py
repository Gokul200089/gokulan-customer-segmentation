import streamlit as st
import pandas as pd

st.title('Customer Segmentation App')

st.info('This app segments customer by their characteristics')

with st.expander("Data"):
  st.write("**Raw Data**")
  df = pd.read_csv("https://raw.githubusercontent.com/Gokul200089/gokulan-customer-segmentation/master/cleaned_data_no_index.csv")
  df

  st.write('**X**')
  X_raw = df.drop('Segmentation', axis=1)
  X_raw

  st.write('**y**')
  y_raw = df.Segmentation
  y_raw
