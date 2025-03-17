import streamlit as st
import base64
from groq import Groq
from groq_api_key import groq_api_key  # Import the Groq API key

# Initialize Groq client with the imported key
client = Groq(api_key=groq_api_key)

# System prompt for prescription analysis
system_prompt = """
You are an expert in prescription analysis. You are tasked with examining images of prescriptions (handwritten or typed) to extract and interpret key information for a healthcare provider. Your expertise will help in identifying medication details, dosages, and instructions.

Your key responsibilities:
1. Detailed Analysis: Scrutinize the prescription image to identify all visible text, focusing on medication names, dosages, administration instructions, and any additional notes.
2. Extracted Information: Document the findings in a clear, structured format, including:
   - Medication Name(s)
   - Dosage(s)
   - Frequency (e.g., daily, twice daily)
   - Route of Administration (e.g., oral, injection)
   - Duration (if specified)
   - Additional Instructions (if any)
3. Potential Issues: Highlight any unclear text, illegible handwriting, or ambiguous instructions that may require clarification.
4. Disclaimer: Include the disclaimer: "Verify with a pharmacist or doctor before acting on this analysis."

Important Notes:
1. Scope: Only analyze images of prescriptions related to human medication.
2. Clarity: If the image is unclear, note that certain details are 'Unable to be accurately determined based on the uploaded image'.
3. Your analysis assists healthcare professionals but is not a substitute for professional verification.

Please provide the final response with these headings:
- Detailed Analysis
- Extracted Information
- Potential Issues
- Disclaimer
"""

# Streamlit UI configuration
st.set_page_config(page_title="Prescription Analyzer", page_icon="💊", layout="wide")
st.title("Prescription Analyzer 💊")
st.subheader("An app to extract and analyze prescription details from images")

# File uploader
file_uploaded = st.file_uploader("Upload the prescription image for analysis", type=["png", "jpg", "jpeg"])

# Display uploaded image
if file_uploaded:
    st.image(file_uploaded, width=200, caption="Uploaded Prescription")

# Submit button
submit = st.button("Analyze Prescription")

# Process the image and generate analysis
if submit and file_uploaded:
    try:
        # Read image data
        image_data = file_uploaded.getvalue()
        if not image_data:
            st.error("Error: No image data found.")
        else:
            # Determine MIME type dynamically
            mime_type = "image/jpeg" if file_uploaded.type in ["image/jpeg", "image/jpg"] else "image/png"
            
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Prepare the prompt with image and text
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                    ]
                }
            ]

            # Call Groq API
            with st.spinner("Analyzing prescription..."):
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",  # Multimodal model
                    messages=messages,
                    max_tokens=8192,
                    temperature=1.0,
                )

            # Display response
            if response and response.choices:
                st.title("Analysis of the Uploaded Prescription")
                st.markdown(response.choices[0].message.content)
            else:
                st.error("No response received from the API.")

    except Exception as e:
        st.error(f"Error analyzing prescription: {str(e)}")
        if isinstance(e, client.APIConnectionError):
            st.write("Could not connect to the Groq API. Check your network or API key.")
        elif isinstance(e, client.RateLimitError):
            st.write("Rate limit exceeded. Please wait and try again.")
        elif isinstance(e, client.APIStatusError):
            st.write(f"API returned an error: {e.status_code} - {e.response}")

# Footer
st.markdown("---")
st.write("Powered by Groq API | Date: March 17, 2025")