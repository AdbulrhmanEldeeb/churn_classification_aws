import streamlit as st
import requests
import json

# API Endpoint
API_URL = "https://gng8qcrjc6.execute-api.us-east-1.amazonaws.com/prod"

st.title("Customer Churn Prediction")
st.write("Enter customer details to predict whether they will exit or not.")

# Input fields
credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=670)
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=18, max_value=100, value=38)
tenure = st.number_input("Tenure (Years)", min_value=0, max_value=10, value=7)
balance = st.number_input("Balance ($)", min_value=0.0, step=100.0, value=0.0)
num_of_products = st.number_input("Number of Products", min_value=1, max_value=4, value=2)
has_cr_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
is_active_member = st.selectbox("Is Active Member?", ["Yes", "No"])
estimated_salary = st.number_input("Estimated Salary ($)", min_value=0.0, step=100.0, value=77864.41)

# Country selection
country = st.selectbox("Country", ["France", "Germany", "Spain"])

# Convert categorical values to numerical
gender_map = {"Male": 1, "Female": 0}
has_cr_card_map = {"Yes": 1, "No": 0}
is_active_member_map = {"Yes": 1, "No": 0}
country_map = {"France": [1, 0, 0], "Germany": [0, 1, 0], "Spain": [0, 0, 1]}

# Prepare the input data
input_data = [
    credit_score,
    gender_map[gender],
    age,
    tenure,
    balance,
    num_of_products,
    has_cr_card_map[has_cr_card],
    is_active_member_map[is_active_member],
    estimated_salary,
] + country_map[country]

if st.button("Predict Churn"):
    payload = json.dumps({"data": input_data})
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(API_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json().get("result", "Error retrieving prediction")
        st.success(f"Prediction: {result}")
    else:
        st.error("Failed to get prediction. Check API status.")
