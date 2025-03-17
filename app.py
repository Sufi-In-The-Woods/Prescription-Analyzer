import streamlit as st
import base64
from groq import Groq
from groq_api_key import groq_api_key  # Import the Groq API key

# Initialize Groq client with the imported key
client = Groq(api_key=groq_api_key)

# System prompt for analyzing prescriptions and medical test reports
system_prompt = """
You are an expert in analyzing medical documents, including prescriptions and medical test reports. You are tasked with examining images of these documents (handwritten or typed) to extract and interpret key information for a healthcare provider. Your expertise will help in identifying medication details from prescriptions or explaining test results from medical reports.

Your key responsibilities depend on the document type:

For Prescriptions:
1. Detailed Analysis: Scrutinize the prescription image to identify all visible text, focusing on medication names, dosages, administration instructions, and any additional notes.
2. Extracted Information: Document the findings in a clear, structured format, including:
   - Medication Name(s)
   - Dosage(s)
   - Frequency (e.g., daily, twice daily)
   - Route of Administration (e.g., oral, injection)
   - Duration (if specified)
   - Additional Instructions (if any)
3. Potential Issues: Highlight any unclear text, illegible handwriting, or ambiguous instructions that may require clarification.

For Medical Test Reports:
1. Detailed Analysis: Examine the test report image to identify all visible text, focusing on test names, results, reference ranges, and any comments or interpretations.
2. Extracted Information: Document the findings in a clear, structured format, including:
   - Test Name(s)
   - Result(s) (with units, if applicable)
   - Reference Range(s)
   - Abnormal Findings (if any, e.g., values outside reference ranges)
   - Comments or Notes (if present)
3. Potential Issues: Highlight any unclear text, missing data, or ambiguous results that may require further investigation.

General Responsibilities:
4. Explanation: Provide a brief explanation of the extracted information (e.g., what a medication is used for, or what a test result might indicate), tailored to the document type.
5. Disclaimer: Include the disclaimer: "Verify with a pharmacist or doctor before acting on this analysis. This is not a substitute for professional medical advice."

Important Notes:
1. Scope: Only analyze images of prescriptions or medical test reports related to human health.
2. Clarity: If the image is unclear, note that certain details are 'Unable to be accurately determined based on the uploaded image'.
3. Detection: Automatically determine whether the image is a prescription or a medical test report based on its content (e.g., presence of medication names vs. test results). If uncertain, analyze it as both and note the ambiguity.
4. Your analysis assists healthcare professionals but is not a definitive diagnosis or prescription.

Please provide the final response with these headings:
- Detailed Analysis
- Extracted Information
- Potential Issues
- Explanation
- Disclaimer
"""

# Streamlit UI configuration
st.set_page_config(page_title="Medical Document Analyzer", page_icon="📝", layout="wide")
st.title("Medical Document Analyzer 📝")
st.subheader("An app to analyze prescriptions and medical test reports from images")

# File uploader
file_uploaded = st.file_uploader("Upload a prescription or medical test report image for analysis", type=["png", "jpg", "jpeg"])

# Display uploaded image
if file_uploaded:
    st.image(file_uploaded, width=200, caption="Uploaded Document")

# Submit button
submit = st.button("Analyze Document")

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
            with st.spinner("Analyzing document..."):
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",  # Multimodal model
                    messages=messages,
                    max_tokens=8192,
                    temperature=1.0,
                )

            # Display response
            if response and response.choices:
                st.title("Analysis of the Uploaded Document")
                st.markdown(response.choices[0].message.content)
            else:
                st.error("No response received from the API.")

    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        if isinstance(e, client.APIConnectionError):
            st.write("Could not connect to the Groq API. Check your network or API key.")
        elif isinstance(e, client.RateLimitError):
            st.write("Rate limit exceeded. Please wait and try again.")
        elif isinstance(e, client.APIStatusError):
            st.write(f"API returned an error: {e.status_code} - {e.response}")

# Footer
st.markdown("---")
st.write("Powered by Groq API | Date: March 17, 2025")
