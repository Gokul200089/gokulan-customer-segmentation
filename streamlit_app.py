import streamlit as st
import pandas as pd

st.title('Customer Segmentation App')

st.info('This app segments customer by their characteristics')

 with st.expander("Data"):
  st.write("**Raw Data**")
  df = pd.read_csv("https://raw.githubusercontent.com/Gokul200089/gokulan-customer-segmentation/master/cleaned_data_no_index.csv")
  df
