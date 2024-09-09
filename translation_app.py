import streamlit as st
import requests
import csv
import os

# Define the FastAPI server URL
API_URL = "http://localhost:8000"  # Replace with your FastAPI server URL and port

# Function to send a translation request to the FastAPI backend
def translate(text, model):
    endpoint = f"{API_URL}/{model}"  # Construct the API endpoint based on the selected model
    response = requests.post(endpoint, json={"msg": text})  # Send a POST request with the input text
    if response.status_code == 200:
        return response.json().get("response", "Translation failed")
    else:
        return "Error in translation request"

# Function to save translations to CSV
def save_to_csv(en_text, ar_text):
    file_exists = os.path.isfile('translations.csv')
    
    with open('translations.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['English', 'Arabic'])  # Write header if file does not exist
        writer.writerow([en_text, ar_text])  # Write the English and Arabic translations

# Streamlit UI
st.title("Translation Model Tester")

# Model selection
model = st.selectbox("Choose a model:", ("ar_en", "en_ar", "fr_en", "en_fr"))

# Text input
text_input = st.text_area("Enter text to translate:")

# Translate button
if st.button("Translate"):
    if text_input.strip():
        result = translate(text_input, model)
        st.write("**Result:**")
        st.success(result)
        
        # Save translations to CSV
        if model in ["ar_en", "en_ar"]:
            en_text = text_input if model == "ar_en" else result
            ar_text = result if model == "ar_en" else text_input
            save_to_csv(en_text, ar_text)
        
    else:
        st.warning("Please enter text to translate.")
