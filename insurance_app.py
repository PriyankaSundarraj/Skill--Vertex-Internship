# -*- coding: utf-8 -*-
"""insurance_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1snNSXjLfgcsjp4MRxw88hibucUmTQQRd
"""

#!pip install streamlit
import streamlit as st
import pandas as pd
#!pip install xgboost
from xgboost import XGBRegressor
import joblib

model_path = model_path = r'final_model.pkl'
# Replace with the actual path
model = joblib.load(model_path)


# Define custom CSS style for attribution
custom_css = """
    <style>
        .attribution {
            font-size: 18px;
            color: #3366ff; /* Blue color */
            font-weight: bold;
            font-family: Arial, sans-serif;
        }
    </style>
"""


# Define the Streamlit app
def main():
    # Set the title and description
    st.title('Health Insurance Charges Prediction App')
    st.write('This app predicts health insurance charges based on user input.')
    

    # Create input fields for user data
    age = st.slider('Age', 18, 64, 30)
    bmi = st.slider('BMI', 15.0, 53.1, 25.0)
    children = st.slider('Number of Children', 0, 5, 1)
    smoker = st.selectbox('Smoker', ['No', 'Yes'])

    # Map categorical input to numerical values
    smoker = 1 if smoker == 'Yes' else 0

    # Create a DataFrame with user input
    input_data = pd.DataFrame({'age': [age], 'bmi': [bmi], 'children': [children], 'smoker': [smoker]})

    # Predict insurance charges
    currency_symbol = st.selectbox('Select Currency Symbol', ['$', '₹'])

    if st.button('Predict'):
        prediction = model.predict(input_data)
        formatted_prediction = f'Predicted Insurance Charges: {currency_symbol}{prediction[0]:.2f}'
        st.write(formatted_prediction)

    

   # Add the attribution with custom formatting
    st.markdown(
        """
        <div style="text-align:center; font-size: 24px; color: #ff5733; font-weight: bold;">
            Created by Priyanka Sundarraj
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    main()
