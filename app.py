import streamlit as st
import base64
from groq import Groq
from groq_api_key import groq_api_key  # Import the Groq API key

# Initialize Groq client with the imported key
client = Groq(api_key=groq_api_key)

# Streamlit UI configuration (MUST BE FIRST STREAMLIT COMMAND)
st.set_page_config(
    page_title="EarlyMed Analyzer", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced system prompt for medical document analysis
system_prompt = """
You are a domain expert in medical image analysis. You are tasked with 
examining medical images for a renowned hospital.
Your expertise will help in identifying or 
discovering any anomalies, diseases, conditions or
any health issues that might be present in the image.

Your key responsibilities:
1. Detailed Analysis: Scrutinize and thoroughly examine each image, 
focusing on finding any abnormalities.
2. Analysis Report: Document all the findings and 
clearly articulate them in a structured format.
3. Recommendations: Based on the analysis, suggest remedies, 
tests or treatments as applicable.
4. Treatments: If applicable, lay out detailed treatments 
which can help in faster recovery.

Important Notes to remember:
1. Scope of response: Only respond if the image pertains to 
human health issues.
2. Clarity of image: In case the image is unclear, 
note that certain aspects are 
'Unable to be correctly determined based on the uploaded image'.
3. Disclaimer: Accompany your analysis with the disclaimer: 
"Consult with a Doctor before making any decisions."
4. Your insights are invaluable in guiding clinical decisions. 
Please proceed with the analysis, adhering to the 
structured approach outlined above.

Please provide the final response with these 4 headings: 
Detailed Analysis, Analysis Report, Recommendations, and Treatments
"""

# Custom CSS for a professional medical UI
st.markdown("""
    <style>
    /* Background and global styling */
    .stApp {
        background: linear-gradient(135deg, #f0f5fa 0%, #ffffff 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Header logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 0;
        padding: 10px;
    }
    .logo-container img {
        max-height: 120px;
    }
    
    /* Glassy container */
    .glass-container {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 25px;
    }
    
    /* Title styling */
    h1 {
        color: #0d4a8a;
        font-weight: 700;
        text-align: center;
        margin-top: 0;
    }
    
    /* Subheader styling */
    h2 {
        color: #2271b8;
        font-weight: 500;
        text-align: center;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #0d4a8a;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #2271b8;
        box-shadow: 0 4px 15px rgba(34, 113, 184, 0.4);
        transform: translateY(-2px);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #2271b8;
        border-radius: 10px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #2271b8;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #0d4a8a !important;
    }
    
    /* How it works section */
    .how-it-works {
        background: rgba(240, 248, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #2271b8;
        margin: 25px 0;
    }
    .how-it-works h3 {
        color: #0d4a8a;
        margin-top: 0;
    }
    .step {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }
    .step-number {
        background: #0d4a8a;
        color: white;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        flex-shrink: 0;
    }
    
    /* Result styling */
    .result-container h2 {
        border-bottom: 2px solid #e6f0fa;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #4b5e7e;
        font-size: 14px;
        margin-top: 30px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
    }
    
    /* Custom for two-column layout */
    .upload-container {
        display: flex;
        flex-direction: column;
    }
    
    /* Responsive tweaks */
    @media (max-width: 768px) {
        .logo-container img {
            max-height: 80px;
        }
        .glass-container {
            padding: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Logo display
st.markdown("""
    <div class="logo-container">
        <img src="https://i.postimg.cc/ZRSsW8hC/logo.png" alt="EarlyMed Logo">
    </div>
""", unsafe_allow_html=True)

# Main header in a glassy container
with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.title("EarlyMed Prescription and Test Report Analyzer")
    st.subheader("AI-Powered Medical Document Analysis")
    st.markdown('</div>', unsafe_allow_html=True)

# Two-column layout for upload and instructions
col1, col2 = st.columns([3, 2])

# File uploader and image display in a glassy container
with col1:
    st.markdown('<div class="glass-container upload-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Upload Your Medical Document</h3>", unsafe_allow_html=True)
    
    file_uploaded = st.file_uploader("Select a prescription, lab report or medical test result", 
                                    type=["png", "jpg", "jpeg"], 
                                    help="Supported formats: JPG, JPEG, PNG")
    
    if file_uploaded:
        st.image(file_uploaded, width=400, caption="Uploaded Medical Document")
        st.markdown("<p style='text-align: center; font-style: italic; color: #666;'>Document preview shown above</p>", unsafe_allow_html=True)
    
    submit = st.button("Analyze Document")
    st.markdown('</div>', unsafe_allow_html=True)

# Instructions in a glassy container
with col2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>How to Use</h3>", unsafe_allow_html=True)
    st.markdown("""
        <ol>
            <li><strong>Upload</strong> a clear image of your prescription, lab report, or medical test result</li>
            <li><strong>Click</strong> the "Analyze Document" button</li>
            <li><strong>Wait</strong> a few seconds for our AI to process your document</li>
            <li><strong>Review</strong> the detailed analysis and simplified explanation</li>
        </ol>
        
        <p style="background-color: #f8f9fa; padding: 10px; border-left: 3px solid #2271b8; margin-top: 15px;">
            <strong>Privacy Note:</strong> Your document is processed securely and not stored on our servers.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
            with st.spinner("Analyzing your medical document... This may take a moment."):
                progress_bar = st.progress(0)
                for i in range(100):
                    import time
                    time.sleep(0.03)
                    progress_bar.progress(i + 1)
                
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",  # Multimodal model
                    messages=messages,
                    max_tokens=8192,
                    temperature=0.7,
                )

            # Display response in a glassy container
            if response and response.choices:
                with st.container():
                    st.markdown('<div class="glass-container result-container">', unsafe_allow_html=True)
                    st.title("Analysis Results")
                    st.markdown(response.choices[0].message.content)
                    
                    # Download button for the analysis
                    result_text = response.choices[0].message.content
                    b64 = base64.b64encode(result_text.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="EarlyMed_Analysis.txt" style="text-decoration:none;">'+\
                        '<div style="text-align:center;margin-top:20px;"><button style="background-color:#0d4a8a;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Download Analysis as Text</button></div></a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("No response received from the API.")

    except Exception as e:
        st.error(f"Error generating analysis: {str(e)}")
        if hasattr(client, 'APIConnectionError') and isinstance(e, client.APIConnectionError):
            st.write("Could not connect to the Groq API. Check your network or API key.")
        elif hasattr(client, 'RateLimitError') and isinstance(e, client.RateLimitError):
            st.write("Rate limit exceeded. Please wait and try again.")
        elif hasattr(client, 'APIStatusError') and isinstance(e, client.APIStatusError):
            st.write(f"API returned an error: {e.status_code} - {e.response}")

# How it works section
st.markdown('<div class="how-it-works">', unsafe_allow_html=True)
st.markdown("<h3>How EarlyMed Works</h3>", unsafe_allow_html=True)
st.markdown("""
    <div class="step">
        <div class="step-number">1</div>
        <div>
            <strong>Document Upload:</strong> When you upload a medical document image, it's securely transmitted to our system.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">2</div>
        <div>
            <strong>AI Processing:</strong> The Groq API powered by llama-3.2-11b-vision-preview model analyzes the visual content of your document.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">3</div>
        <div>
            <strong>Medical Analysis:</strong> The AI identifies medications, dosages, test results, and medical terminology within the document.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">4</div>
        <div>
            <strong>Plain Language Translation:</strong> Medical jargon is translated into simple, easy-to-understand explanations.
        </div>
    </div>
    
    <div class="step">
        <div class="step-number">5</div>
        <div>
            <strong>Structured Response:</strong> You receive a comprehensive analysis with sections for overview, detailed analysis, 
            simplified explanation, important considerations, and recommended actions.
        </div>
    </div>
    
    <p style="margin-top: 20px; padding: 10px; background-color: rgba(255, 255, 240, 0.7); border-radius: 5px;">
        <strong>Note:</strong> EarlyMed is designed to help you better understand your medical documents, but it is not a replacement 
        for professional medical advice. Always consult with your healthcare provider for proper interpretation of your medical documents 
        and before making any healthcare decisions.
    </p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p><strong>EarlyMed</strong> | Powered by Groq API | Date: March 18, 2025</p>
        <p>Developed by our team at <b>VIT-AP University</b> as part of our mission to make healthcare more accessible through technology.</p>
        <p>Our goal is to help users better understand their health information and leverage AI for improved health literacy.</p>
    </div>
""", unsafe_allow_html=True)
