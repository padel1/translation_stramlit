import streamlit as st
import requests
import csv
import os

# Define the FastAPI server URL
API_URL = "https://partly-gentle-mollusk.ngrok-free.app/"  # Replace with your FastAPI server URL and port

def get_saved_translations():
    endpoint = f"{API_URL}/get_translations"  # FastAPI endpoint for retrieving translations
    response = requests.get(endpoint)  # Send a GET request to the endpoint
    if response.status_code == 200:
        return response.json().get("translations", [])
    else:
        return "Error retrieving translations"
# Function to send a translation request to the FastAPI backend
def translate(text, model):
    endpoint = f"{API_URL}/{model}"  # Construct the API endpoint based on the selected model
    response = requests.post(endpoint, json={"msg": text})  # Send a POST request with the input text
    if response.status_code == 200:
        return response.json().get("response", "Translation failed")
    else:
        return "Error in translation request"

def save_translation(text, translation, model):
    endpoint = f"{API_URL}/save_translation"  # FastAPI endpoint for saving translations
    data = {"text": text, "translation": translation, "model": model}
    response = requests.post(endpoint, json=data)  # Send a POST request with the data
    if response.status_code == 200:
        return response.json().get("message", "Error saving translation")
    else:
        return "Error in save request"
    


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

        if st.button("Save"):
            save_message = save_translation(text_input, result, model)
            st.info(save_message)
        
        
    else:
        st.warning("Please enter text to translate.")
if st.button("Show Saved Translations"):
    saved_translations = get_saved_translations()
    if isinstance(saved_translations, list) and saved_translations:
        for translation in saved_translations:
            st.write(f"**Model:** {translation['model']}")
            st.write(f"**Text:** {translation['text']}")
            st.write(f"**Translation:** {translation['translation']}")
            st.write("---")
    else:
        st.warning("No saved translations found or error occurred.")
