import streamlit as st
import aiohttp
import asyncio

# Define the FastAPI server URL
API_URL = "https://partly-gentle-mollusk.ngrok-free.app/"  # Replace with your FastAPI server URL and port

async def get_saved_translations():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/get_translations") as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"translations": []}

async def translate(text, model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/{model}", json={"msg": text}) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"response": "Translation failed"}

async def save_translation(text, translation, model):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/save_translation", json={"text": text, "translation": translation, "model": model}) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"message": "Error saving translation"}

def run_async_tasks(async_func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(async_func(*args))

# Streamlit UI
st.title("Translation Model Tester")

# Model selection
model = st.selectbox("Choose a model:", ("ar_en", "darija", "en_ar", "fr_en", "en_fr"))

# Text input
text_input = st.text_area("Enter text to translate:")

# Translate button
if st.button("Translate"):
    if text_input.strip():
        result = run_async_tasks(translate, text_input, model)
        st.write("**Result:**")
        st.success(result.get("response", "Translation failed"))

        if st.button("Save"):
            save_message = run_async_tasks(save_translation, text_input, result.get("response", ""), model)
            st.info(save_message.get("message", "Error saving translation"))
    else:
        st.warning("Please enter text to translate.")

if st.button("Show Saved Translations"):
    saved_translations = run_async_tasks(get_saved_translations)
    if saved_translations.get("translations"):
        for translation in saved_translations["translations"]:
            st.write(f"**Model:** {translation['model']}")
            st.write(f"**Text:** {translation['text']}")
            st.write(f"**Translation:** {translation['translation']}")
            st.write("---")
    else:
        st.warning("No saved translations found or error occurred.")
