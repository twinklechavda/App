### KYC APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()  # Load all environment variables from .env file

# Configure Google Gemini API with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash') 
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process the uploaded image file
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Getting the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initialize the Streamlit app
st.set_page_config(page_title="Extracting Information from Card")
st.header("App for Extracting Information")

# Input for prompt customization
input_text = st.text_input("Input Prompt:", key="input")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Define the detailed prompt for the Gemini model
input_prompt = """
You are an expert in OCR and analyzing information from Aadhar, PAN, Credit Card, and Debit Card.
Identify if the card is original or a photocopy, then extract the Name, Card Number, Date of Birth, Address, and Gender from the card.
1. Authenticity - Original or not original
2. Name - Name of the person on the card
3. Card Number - Number on the card
4. Date of Birth - Date of birth as it appears on the card
5. Address - Address as printed on the card (if applicable)
6. Gender - Gender as specified on the card
"""

# Button to submit and extract information
submit = st.button("Extract")

# If submit button is clicked
if submit:
    # Prepare the image for Gemini API processing
    image_data = input_image_setup(uploaded_file)
    
    # Get response from Gemini API
    response = get_gemini_response(input_prompt, image_data, input_text)
    
    # Display the response in the app
    st.subheader("The Response is:")
    st.write(response)
