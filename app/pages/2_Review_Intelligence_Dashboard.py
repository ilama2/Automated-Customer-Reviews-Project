import streamlit as st
import pandas as pd
import os

# Load reviews data with error handling
@st.cache_data
def load_reviews_data():
    file_path = "app/reviews_with_clusters.csv"
    
    # Check if file exists
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found!")
        return pd.DataFrame()  # Return an empty DataFrame
    
    try:
        reviews_df = pd.read_csv(file_path)
        if reviews_df.empty:
            st.warning(f"The file '{file_path}' is empty!")
        return reviews_df
    except Exception as e:
        st.error(f"Error loading the file '{file_path}': {e}")
        return pd.DataFrame()  # Return an empty DataFrame if reading fails

def display_reviews_and_sentiment(reviews_df, product_name):
    product_reviews = reviews_df[reviews_df['name'] == product_name]

    if product_reviews.empty:
        st.warning(f"No reviews found for the product '{product_name}'.")
        return

    positive_reviews = product_reviews[product_reviews['sentiment'] == 'Positive']
    negative_reviews = product_reviews[product_reviews['sentiment'] == 'Negative']
    neutral_reviews = product_reviews[product_reviews['sentiment'] == 'Neutral']

    sentiment_distribution = {
        'Positive': len(positive_reviews),
        'Negative': len(negative_reviews),
        'Neutral': len(neutral_reviews)
    }

    st.markdown(f"###  **Sentiment Overview for `{product_name}`**")
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Positive", sentiment_distribution['Positive'])
    col2.metric("❌ Negative", sentiment_distribution['Negative'])
    col3.metric("   Neutral", sentiment_distribution['Neutral'])

    st.markdown("---")
    st.markdown("### 🌟 Top Positive Reviews")
    for review in positive_reviews['reviews.text'][:5]:
        st.success(f"💬 {review}")

    st.markdown("### 🚫 Top Negative Reviews")
    for review in negative_reviews['reviews.text'][:5]:
        st.error(f"💬 {review}")

# Title of the page
st.title("Review Intelligence Dashboard")

# Load Data
reviews_df = load_reviews_data()

# Input for product name
product_name = st.text_input("🔍 Enter Product Name:")

if product_name:
    if product_name in reviews_df['name'].values:
        display_reviews_and_sentiment(reviews_df, product_name)
    else:
        st.warning(f"Product '{product_name}' not found. Please check spelling.")
