import streamlit as st

# Set the page configuration in the main app file
st.set_page_config(page_title="Multi-Page App", layout="wide")

# Title of the app
st.title("Welcome to the Multi-Page Streamlit App!")

# Sidebar for page navigation
page = st.sidebar.radio("Select a page", ("Review Classification", "Review Intelligence Dashboard"))

if page == "Review Classification":
    # Link to the first page
    st.write("You selected the **Review Classification** page!")
    # You can include the content for Review Classification directly here or import the page as a module.
    # For example, import or execute the code from 'pages/1_Review_Classification.py'
    exec(open('app/pages/1_Review_Classification.py').read())

elif page == "Review Intelligence Dashboard":
    # Link to the second page (Review Intelligence Dashboard)
    st.write("You selected the **Review Intelligence Dashboard** page!")
    # You can include the content for Review Intelligence Dashboard directly here or import the page as a module.
    # For example, import or execute the code from 'pages/2_Review_Intelligence_Dashboard.py'
    exec(open('app/pages/2_Review_Intelligence_Dashboard.py').read())
