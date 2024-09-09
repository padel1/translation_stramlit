import streamlit as st
import requests
import csv
import os

# Define the FastAPI server URL
API_URL = "https://suited-rat-famous.ngrok-free.app"  # Replace with your FastAPI server URL and port

# Function to send a translation request to the FastAPI backend
def translate(text, model):
    endpoint = f"{API_URL}/{model}"  # Construct the API endpoint based on the selected model
    response = requests.post(endpoint, json={"msg": text})  # Send a POST request with the input text
    if response.status_code == 200:
        return response.json().get("response", "Translation failed")
    else:
        return "Error in translation request"


# Streamlit UI
st.title("Translation Model Tester")

# Model selection
model = st.selectbox("Choose a model:", ("ar_en","darija", "en_ar", "fr_en", "en_fr"))

# Text input
text_input = st.text_area("Enter text to translate:")

# Translate button
if st.button("Translate"):
    if text_input.strip():
        result = translate(text_input, model)
        st.write("**Result:**")
        st.success(result)
        
        
        
    else:
        st.warning("Please enter text to translate.")
