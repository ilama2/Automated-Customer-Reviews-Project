import streamlit as st
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import gdown
import os

# Function to download the model from Google Drive
def download_model():
    # Replace 'FILE_ID' with the actual file ID from your Google Drive model link
    url = "https://drive.google.com/drive/folders/1-ku8JPLxNa_uzaLQMTVJmCxtaAke3c-h?usp=sharing"
    output = './final_modelv3py'  # The path to save the model locally
    gdown.download(url, output, quiet=False)

# Check if the model is already downloaded
if not os.path.exists('./final_modelv3py'):
    st.write("Downloading the model...")
    download_model()
    st.write("Model downloaded successfully!")


# Load the tokenizer and model (make sure to replace the model path with the correct one)
model_path = './final_modelv3py'
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)

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
