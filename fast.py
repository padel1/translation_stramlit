import csv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
 
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://185.172.57.177:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from typing_extensions import TypedDict
import ctranslate2
import transformers
 
 
 
import asyncio

class Massage(TypedDict):
    msg: str 

    

ar_en = r"C:\wingo\models--wingo-dz--ar-to-en-v6-optimized\snapshots\43d52422a0ebaacaeddac545d7db732cbc905bcb"
darija = r"C:\wingo\models--wingo-dz--darija_test\snapshots\1680c9e23fa54799b0f6627eed6dad5eaa8407a7"
en_ar = r"C:\wingo\models--wingo-dz--ar_en_ct2\snapshots\3bd0796d90e8eb39948c0029805059743296208e"
# fr_en = "/home/ali/Desktop/translation_models/models--wingo-dz--fr-to-en-v3-optimized/snapshots/cd9cefdf35248c5379918aa8074c5317853bdd63"
# en_fr = "/home/ali/Desktop/translation_models/models--wingo-dz--en-to-fr-v3-optimized/snapshots/e36ec621c390ca82cb2a0e47015bab070425a93f"

def save_to_csv_ar(en_text, ar_text):
    file_exists = os.path.isfile('translations.csv')
    
    with open('translations_ar.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # if not file_exists:
            # writer.writerow(['English', 'Arabic'])  # Write header if file does not exist
        writer.writerow([en_text, ar_text])  # Write the English and Arabic translations

def save_to_csv_darija(en_text, ar_text):
    file_exists = os.path.isfile('translations.csv')
    
    with open('translations_darija.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # if not file_exists:.
            # writer.writerow(['English', 'darija'])  # Write header if file does not exist
        writer.writerow([en_text, ar_text])  # Write the English and Arabic translations

translator_ar_en = ctranslate2.Translator(ar_en)
tokenizer_ar_en = transformers.AutoTokenizer.from_pretrained(ar_en)

translator_darija = ctranslate2.Translator(darija)
tokenizer_darija = transformers.AutoTokenizer.from_pretrained(darija)

translator_en_ar = ctranslate2.Translator(en_ar)
tokenizer_en_ar = transformers.AutoTokenizer.from_pretrained(en_ar)

# translator_fr_en = ctranslate2.Translator(fr_en)
# tokenizer_fr_en = transformers.AutoTokenizer.from_pretrained(fr_en)

# translator_en_fr = ctranslate2.Translator(en_fr)
# tokenizer_en_fr = transformers.AutoTokenizer.from_pretrained(en_fr)

@app.post("/ar_en")
async def root(massage: Massage):
    print(massage["msg"])
    source = tokenizer_ar_en.convert_ids_to_tokens(tokenizer_ar_en.encode(massage["msg"]))

    results = await asyncio.to_thread(translator_ar_en.translate_batch, [source])
    
    target = results[0].hypotheses[0]

    response = tokenizer_ar_en.decode(tokenizer_ar_en.convert_tokens_to_ids(target))
    
    return {"response": response}


@app.post("/darija")
async def root(massage: Massage):
    print(massage["msg"])
    source = tokenizer_darija.convert_ids_to_tokens(tokenizer_darija.encode(massage["msg"]))

    results = await asyncio.to_thread(translator_darija.translate_batch, [source])
    
    target = results[0].hypotheses[0]

    response = tokenizer_darija.decode(tokenizer_darija.convert_tokens_to_ids(target))
    
    return {"response": response}
 
# ngrok http --domain=suited-rat-famous.ngrok-free.app 8000
@app.post("/en_ar")
async def root(massage: Massage):
    # print(massage["msg"])
    source = tokenizer_en_ar.convert_ids_to_tokens(tokenizer_en_ar.encode(massage["msg"]))

    results = await asyncio.to_thread(translator_en_ar.translate_batch, [source])
    
    target = results[0].hypotheses[0]

    response = tokenizer_en_ar.decode(tokenizer_en_ar.convert_tokens_to_ids(target))
    
    return {"response": response}


@app.post("/save_translation")
async def save_translation(data: dict):
    text = data.get("text", "")
    translation = data.get("translation", "")
    model = data.get("model", "")

    if model == "ar_en" or model == "en_ar":
        save_to_csv_ar(text, translation)
    elif model == "darija":
        save_to_csv_darija(text, translation)
    else:
        return {"status": "error", "message": "Invalid model type"}

    return {"status": "success", "message": "Translation saved successfully."}

# @app.post("/fr_en")
# async def root(massage: Massage):
#     source = tokenizer_fr_en.convert_ids_to_tokens(tokenizer_fr_en.encode(massage["msg"]))

#     results = await asyncio.to_thread(translator_fr_en.translate_batch, [source])
    
#     target = results[0].hypotheses[0]

#     response = tokenizer_fr_en.decode(tokenizer_fr_en.convert_tokens_to_ids(target))
    
#     return {"response": response}

# @app.post("/en_fr")
# async def root(massage: Massage):
    # source = tokenizer_en_fr.convert_ids_to_tokens(tokenizer_en_fr.encode(massage["msg"]))

    # results = await asyncio.to_thread(translator_en_fr.translate_batch, [source])
    
    # target = results[0].hypotheses[0]

    # response = tokenizer_en_fr.decode(tokenizer_en_fr.convert_tokens_to_ids(target))
    
    # return {"response": response}

@app.get("/get_translations")
async def get_translations():
    translations = []

    # Read translations from CSV files
    if os.path.isfile('translations_ar.csv'):
        with open('translations_ar.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                translations.append({"model": "ar_en", "text": row[0], "translation": row[1]})

    if os.path.isfile('translations_darija.csv'):
        with open('translations_darija.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                translations.append({"model": "darija", "text": row[0], "translation": row[1]})

    # Add more CSV files as needed for other models

    return {"translations": translations}
