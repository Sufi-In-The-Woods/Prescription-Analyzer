import streamlit as st
import base64
from groq import Groq
from groq_api_key import groq_api_key  # Import the Groq API key

# Streamlit UI configuration (MUST BE FIRST STREAMLIT COMMAND)
st.set_page_config(
    page_title="EarlyMed Analyzer", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Groq client with the imported key (non-Streamlit code can come before set_page_config)
client = Groq(api_key=groq_api_key)

# Custom CSS for professional medical UI
st.markdown("""
    <style>
    /* Global styling */
    body {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* Main title styling */
    .main-title {
        font-size: 2.6em;
        font-weight: 700;
        color: #0d4a8a;
        text-align: center;
        margin-bottom: 0.3em;
        letter-spacing: -0.5px;
    }
    
    /* Subheader styling */
    .subheader {
        font-size: 1.5em;
        color: #2271b8;
        text-align: center;
        margin-bottom: 1.5em;
        font-weight: 400;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        justify-content: center;
        margin: 10px auto 20px auto;
    }
    .logo-container img {
        max-height: 120px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8em;
        color: #0d4a8a;
        margin-top: 1.2em;
        margin-bottom: 0.8em;
        font-weight: 600;
        border-bottom: 2px solid #e6f0fa;
        padding-bottom: 8px;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 1px solid #f0f5fa;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #2271b8;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        background: rgba(240, 248, 255, 0.5);
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #0d4a8a;
        color: white;
        border-radius: 8px;
        padding: 0.8em 1.5em;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2271b8;
        box-shadow: 0 4px 12px rgba(34, 113, 184, 0.3);
        transform: translateY(-2px);
    }
    
    /* How it works section */
    .how-it-works {
        background: #f9fbff;
        border-radius: 12px;
        padding: 25px;
        margin: 30px 0;
        border-left: 5px solid #2271b8;
    }
    .step {
        margin-bottom: 15px;
        display: flex;
        align-items: flex-start;
    }
    .step-number {
        background: #0d4a8a;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    /* Result styling */
    .analysis-result {
        background: white;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 20px 0;
        border-top: 4px solid #2271b8;
    }
    
    /* Footer styling */
    .footer-text {
        font-size: 0.9em;
        color: #4b5e7e;
        text-align: center;
        margin-top: 2em;
        padding: 15px;
        background: #f9fbff;
        border-radius: 8px;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #0d4a8a !important;
    }
    
    /* Progress bar customization */
    .stProgress > div > div {
        background-color: #2271b8;
    }
    
    /* Disclaimer box */
    .disclaimer-box {
        background-color: #fff8e6;
        border-left: 4px solid #ffb74d;
        padding: 15px;
        margin: 20px 0;
        border-radius: 4px;
    }
    
    /* File uploader customization */
    .stFileUploader {
        padding: 5px;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .logo-container img {
            max-height: 80px;
        }
        .main-title {
            font-size: 2em;
        }
        .subheader {
            font-size: 1.2em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Enhanced system prompt for medical document analysis
system_prompt = """
You are an expert in analyzing medical documents, including prescriptions and medical test reports. You are tasked with examining images of these documents (handwritten or typed) to extract and interpret key information for patients and healthcare providers.

Your key responsibilities depend on the document type:

For Prescriptions:
1. Document Identification: Confirm the document is a prescription and identify its key components.
2. Detailed Analysis: Scrutinize the prescription image to identify all visible text, focusing on:
   - Medication names (brand and generic if available)
   - Dosages and formulations
   - Administration instructions (timing, method, duration)
   - Prescriber information and date
   - Patient information (if visible, without mentioning specific names)
   - Refill information and special instructions
3. Plain Language Explanation: Provide a simplified explanation of what each medication is typically used for and any important administration details.
4. Critical Warnings: Highlight any potential drug interactions, common side effects, or special precautions patients should be aware of.

For Medical Test Reports:
1. Document Identification: Confirm the document is a medical test report and identify the type of test.
2. Detailed Analysis: Extract all relevant information including:
   - Test name(s) and date performed
   - Results with units and reference ranges
   - Flagged abnormal values (high/low)
   - Laboratory/facility information
   - Physician notes or interpretations (if present)
3. Plain Language Explanation: Translate medical terminology and explain what each test measures in simple terms.
4. Context for Results: Provide general information about what abnormal results might indicate, while being careful not to diagnose.

For Both Document Types:
1. Quality Assessment: Note any illegible text, missing information, or ambiguous instructions.
2. Recommended Follow-up: Suggest appropriate next steps based on the document content.
3. Privacy Protection: Do not include any personally identifiable information in your analysis.
4. Medical Disclaimer: Include this disclaimer: "This analysis is provided for educational purposes only. Always consult with your healthcare provider before making any changes to your treatment plan or interpreting test results."

Structure your response with these headings:
1. Document Type & Overview
2. Detailed Analysis
3. Plain Language Explanation
4. Important Considerations
5. Recommended Actions
6. Medical Disclaimer
"""

# Logo at the top
st.markdown('<div class="logo-container"><img src="https://i.postimg.cc/ZRSsW8hC/logo.png" alt="EarlyMed Logo"></div>', unsafe_allow_html=True)

# Title and subheader
st.markdown('<div class="main-title">EarlyMed Prescription and Test Report Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">AI-Powered Analysis of Medical Documents</div>', unsafe_allow_html=True)

# Main content in a container with card styling
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])  # Two-column layout

with col1:
    # File uploader with improved styling
    st.markdown('<h3 style="color: #0d4a8a; text-align: center;">Upload Your Document</h3>', unsafe_allow_html=True)
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    file_uploaded = st.file_uploader("Select a prescription or medical test report", 
                                     type=["png", "jpg", "jpeg"], 
                                     help="Supported formats: PNG, JPG, JPEG")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display uploaded image
    if file_uploaded:
        st.image(file_uploaded, width=250, caption="Uploaded Medical Document")
        st.markdown("<p style='text-align: center; font-style: italic; color: #666;'>Document preview shown above</p>", unsafe_allow_html=True)
    
    # Submit button with enhanced styling
    submit = st.button("Analyze Document")
    
    # Quick instructions
    if not file_uploaded:
        st.markdown("""
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h4 style="margin-top: 0; color: #0d4a8a;">Quick Guide:</h4>
            <ol style="margin-bottom: 0; padding-left: 20px;">
                <li>Upload a clear image of your prescription or medical report</li>
                <li>Click "Analyze Document"</li>
                <li>Review the detailed analysis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

with col2:
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

                # Call Groq API with progress bar
                with st.spinner("Analyzing your medical document..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        import time
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
                    response = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",  # Multimodal model
                        messages=messages,
                        max_tokens=8192,
                        temperature=0.7,
                    )

                # Display response with enhanced styling
                if response and response.choices:
                    st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
                    st.markdown('<h2 style="color: #0d4a8a; text-align: center; margin-bottom: 20px;">Analysis Results</h2>', unsafe_allow_html=True)
                    st.markdown(response.choices[0].message.content)
                    
                    # Download button for results
                    result_text = response.choices[0].message.content
                    b64 = base64.b64encode(result_text.encode()).decode()
                    download_button = f'''
                    <div style="text-align: center; margin-top: 25px;">
                        <a href="data:file/txt;base64,{b64}" download="EarlyMed_Analysis.txt" 
                           style="background-color: #0d4a8a; color: white; padding: 10px 15px; text-decoration: none; 
                                  border-radius: 5px; font-weight: 600;">
                            Download Analysis as Text
                        </a>
                    </div>
                    '''
                    st.markdown(download_button, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("No response received from the API.")

        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            if hasattr(client, 'APIConnectionError') and isinstance(e, client.APIConnectionError):
                st.write("Could not connect to the Groq API. Check your network or API key.")
            elif hasattr(client, 'RateLimitError') and isinstance(e, client.RateLimitError):
                st.write("Rate limit exceeded. Please wait and try again.")
            elif hasattr(client, 'APIStatusError') and isinstance(e, client.APIStatusError):
                st.write(f"API returned an error: {e.status_code} - {e.response}")
    else:
        # App description when no analysis is running
        st.markdown("""
        <h3 style="color: #0d4a8a;">Welcome to EarlyMed</h3>
        <p>EarlyMed's Prescription and Test Report Analyzer helps you understand your medical documents with the power of AI. Upload your:</p>
        <ul>
            <li><strong>Prescriptions</strong> - Get detailed information about your medications, dosages, and instructions</li>
            <li><strong>Laboratory Reports</strong> - Understand your test results and what they mean for your health</li>
            <li><strong>Medical Test Results</strong> - Decode complex medical terminology into plain language</li>
        </ul>
        
        <div class="disclaimer-box">
            <p><strong>Privacy Note:</strong> Your documents are processed securely and not stored on our servers. We prioritize the confidentiality of your medical information.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# How It Works Section with enhanced styling
st.markdown('<div class="how-it-works">', unsafe_allow_html=True)
st.markdown('<div class="section-header">How EarlyMed Works</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="step">
        <div class="step-number">1</div>
        <div>
            <strong>Document Upload:</strong> When you upload a medical document image, it's securely transmitted to our system without being stored permanently.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">2</div>
        <div>
            <strong>AI Processing:</strong> The Groq API powered by llama-3.2-11b-vision-preview model analyzes the visual content of your document using advanced computer vision and natural language processing.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">3</div>
        <div>
            <strong>Document Recognition:</strong> The system automatically identifies whether your document is a prescription or a medical test report and applies the appropriate analytical approach.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">4</div>
        <div>
            <strong>Information Extraction:</strong> For prescriptions, the AI extracts medication names, dosages, and instructions. For test reports, it identifies test names, results, and reference ranges.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">5</div>
        <div>
            <strong>Medical Translation:</strong> Complex medical terminology is converted into easy-to-understand language, helping you comprehend what your medications do or what your test results mean.
        </div>
    </div>
    
    <p style="margin-top: 25px;">
        <strong>EarlyMed's Vision:</strong> Developed by our team at VIT-AP University, EarlyMed aims to empower users to stay proactive about their health. By integrating AI tools like this analyzer, we're building a platform to simplify medical document interpretation, promote early detection of health issues, and bridge the gap between technology and well-being. Our goal is a healthier, more informed community.
    </p>
    
    <div class="disclaimer-box" style="margin-top: 20px;">
        <strong>Important:</strong> This tool is designed to help you better understand your medical documents, but it is not a replacement for professional medical advice. Always consult with your healthcare provider for proper interpretation of your medical documents and before making any healthcare decisions.
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with enhanced styling
st.markdown("---")
st.markdown("""
<div class="footer-text">
    <p><strong>EarlyMed</strong> | Powered by Groq API | Date: March 18, 2025</p>
    <p>A platform developed by our team at <b>VIT-AP University</b>.</p>
    <p>Our goal is to help users stay aware of their health and leverage technology and AI for a healthier life.</p>
</div>
""", unsafe_allow_html=True)
