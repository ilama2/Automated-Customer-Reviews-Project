import streamlit as st
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import gdown
import os

# === CONFIG ===
MODEL_DIR = "final_modelv3py"
ZIP_FILE = "final_modelv3py.zip"
FILE_ID = "1gd-5Ah8c_0-qF_LHckISCvpFhIKAb0Fk"  # Replace with your actual file ID
GDRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"

# === DOWNLOAD + UNZIP ===
def download_and_extract_model():
    if not os.path.exists(MODEL_DIR):
        st.info("Downloading model from Google Drive...")
        gdown.download(GDRIVE_URL, ZIP_FILE, quiet=False)

        st.info("Extracting model...")
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall()

        st.success("Model ready!")

# === Load the model ===
download_and_extract_model()

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
