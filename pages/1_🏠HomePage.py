import streamlit as st
st.markdown(
    """
    <style>
    /* Page background */
    body {
        background-color: #cef1ff;  /* light blue background */
    }

    /* Optional: main content containers background */
    .css-1d391kg {
        background-color: #ffffff;  /* keep content white for readability */
        padding: 10px;
        border-radius: 10px;
    }

    /* Optional: remove extra padding/margins */
    .block-container {
        padding-top: 20px;
        padding-bottom: 20px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🏠 Home Page")
st.write("Welcome to the Home Page!")
