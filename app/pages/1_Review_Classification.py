import streamlit as st
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import gdown
import os
import zipfile 

# === CONFIG ===
MODEL_DIR = "final_modelv3py"
ZIP_FILE = "final_modelv3py.zip"
ZIP_PATH = "final_modelv3py.zip"
FILE_ID = "1gd-5Ah8c_0-qF_LHckISCvpFhIKAb0Fk"  
GDRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

# === DOWNLOAD + UNZIP ===
if not os.path.exists(MODEL_DIR):
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, ZIP_PATH, quiet=False)
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(ZIP_PATH)

# Load the tokenizer and model (make sure to replace the model path with the correct one)
tokenizer = RobertaTokenizer.from_pretrained(MODEL_DIR)
model = RobertaForSequenceClassification.from_pretrained(MODEL_DIR)

# Set up the app layout
st.title("Review Classification")

st.write("""
    Enter a product review or any text below to classify its sentiment as Positive, Neutral, or Negative.
""")

# Text input from the user
user_input = st.text_area("Enter your text here:")

# Button to classify sentiment
if st.button("Classify The Review"):
    if user_input:
        # Tokenize the input text
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # Perform the forward pass (inference)
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted class (the index of the max logit)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=-1).item()

        # Map the predicted class to sentiment label
        sentiment = {0: "Negative", 1: "Neutral", 2: "Positive"}
        st.write(f"Predicted Sentiment: {sentiment[predicted_class]}")
    else:
        st.warning("Please enter some text to classify.")
