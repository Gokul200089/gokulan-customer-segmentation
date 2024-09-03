import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

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

#Input features
with st.sidebar:
  st.header("Input Features")
  Gender = st.selectbox("Gender", ("Male", "Female"))
  Ever_Married = st.selectbox("Ever_Married", ("Yes", "No"))
  Graduated = st.selectbox("Graduated", ("Yes", "No"))
  Profession = st.selectbox("Profession", ("Artist", "Doctor", "Engineer", "Entertainment", "Executive", "Healthcare", "Homemaker", "Lawyer", "Marketing"))
  Var_1 = st.selectbox("Var_1", ("Cat_1", "Cat_2", "Cat_3", "Cat_4", "Cat_5", "Cat_6", "Cat_7"))
  Spending_Score = st.selectbox("Spending_Score", ("Low", "Average", "High"))
  Age = st.number_input("Age", min_value=1, max_value=200)
  Work_Experience = st.number_input("Work_Experience", min_value=1, max_value=50)
  Family_Size = st.number_input("Family_Size", min_value=1, max_value=100)

 # Create a DataFrame for the input features
  data = {'Gender': Gender,
          'Ever_Married':Ever_Married,
          'Graduated': Graduated,
          'Profession': Profession,
          'Var_1': Var_1,
          'Spending_Score': Spending_Score,
          'Age': Age,
          'Work_Experience': Work_Experience,
          'Family_Size':Family_Size}
  input_df = pd.DataFrame(data, index=[0])
  input_customers = pd.concat([input_df, X_raw], axis=0)

with st.expander('Input features'):
  st.write('**Input customer**')
  input_df
  st.write('**Combined customer data**')
  input_customers


# Data preparation
# Encode X
encode = ['Gender', 'Ever_Married', 'Graduated', 'Profession', 'Var_1', 'Spending_Score']
df_customers = pd.get_dummies(input_customers, prefix=encode)

X = df_customers[1:]
input_row = df_customers[:1]

# Encode y
target_mapper = {'A': 0,
                 'B': 1,
                 'C': 2,
                 'D': 3}
def target_encode(val):
  return target_mapper[val]

y = y_raw.apply(target_encode)

with st.expander('Data preparation'):
  st.write('**Encoded X (input customer)**')
  input_row
  st.write('**Encoded y**')
  y

# Model training and inference
## Train the ML model
clf = GradientBoostingClassifier()
clf.fit(X, y)

## Apply model to make predictions
prediction = clf.predict(input_row)
prediction_proba = clf.predict_proba(input_row)

df_prediction_proba = pd.DataFrame(prediction_proba)
df_prediction_proba.columns = ['A', 'B', 'C', 'D']
df_prediction_proba.rename(columns={0: 'A',
                                 1: 'B',
                                 2: 'C',
                                 3: 'D'})

# Display predicted species
st.subheader('Customer is mostly likely belong to the segment')

# First row with two columns
row1_col1, row1_col2 = st.columns(2)

# Second row with two columns
row2_col1, row2_col2 = st.columns(2)

# Display the data in each column
with row1_col1:
    st.dataframe(df_prediction_proba[['A']],
                 column_config={
                   'A': st.column_config.ProgressColumn(
                     'A',
                     format='%f',
                     width='medium',
                     min_value=0,
                     max_value=1
                   ),
                 }, hide_index=True)

with row1_col2:
    st.dataframe(df_prediction_proba[['B']],
                 column_config={
                   'B': st.column_config.ProgressColumn(
                     'B',
                     format='%f',
                     width='medium',
                     min_value=0,
                     max_value=1
                   ),
                 }, hide_index=True)

with row2_col1:
    st.dataframe(df_prediction_proba[['C']],
                 column_config={
                   'C': st.column_config.ProgressColumn(
                     'C',
                     format='%f',
                     width='medium',
                     min_value=0,
                     max_value=1
                   ),
                 }, hide_index=True)

with row2_col2:
    st.dataframe(df_prediction_proba[['D']],
                 column_config={
                   'D': st.column_config.ProgressColumn(
                     'D',
                     format='%f',
                     width='medium',
                     min_value=0,
                     max_value=1
                   ),
                 }, hide_index=True)


customer_segment = np.array(['A', 'B', 'C', 'D'])
st.success(str(customer_segment[prediction][0]))
