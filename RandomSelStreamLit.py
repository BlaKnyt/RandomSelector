import streamlit as st
import pandas as pd
import random
import base64
import os

# --- 1. THE BACKGROUND LOGIC ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_bg(image_file):
    if not os.path.exists(image_file):
        st.error(f"❌ DEBUG: File NOT found at: {os.path.abspath(image_file)}")
        return

    file_extension = image_file.lower().split('.')[-1]
    mime_type = f"image/{file_extension}"
    if file_extension in ['jpg', 'jpeg']:
        mime_type = "image/jpeg"

    bin_str = get_base64_of_bin_file(image_file)

    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:{mime_type};base64,{bin_str}");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    [data-testid="stVerticalBlock"] {{
        background-color: rgba(0, 0, 0, 0.7); 
        padding: 2rem;
        border-radius: 15px;
        margin-top: 20px;
    }}

    h1, h2, h3, p, label, .stMarkdown, .stRadio {{
        color: #A9A9A9 !important;
    }}
    
    .stTextArea textarea {{
        background-color: #1A1A1A !important;
        color: #A9A9A9 !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# --- 2. RESET FUNCTION ---
def reset_app():
    # Clear session state and rerun
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- 3. APP CONFIGURATION ---
st.set_page_config(page_title="Random Selector", page_icon="🎲", layout="centered")

# Ensure this matches your filename in IntelliJ exactly
YOUR_IMAGE_FILENAME = 'RainingChips.jpg'
set_page_bg(YOUR_IMAGE_FILENAME)

# --- 4. UI ELEMENTS ---
st.title("🎲 Random Selector")

# Using session_state for the radio button so it resets correctly
option = st.radio("Choose input method:", ("Paste Text", "Upload File"), key="input_method")

items = []

if option == "Paste Text":
    # The 'key' allows the reset function to clear this specific box
    data = st.text_area("Paste items (comma or line separated):", height=150, key="text_input")
    if data:
        items = [item.strip() for item in data.replace("\n", ",").split(",") if item.strip()]
else:
    # The 'key' allows the reset function to clear the file uploader
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"], key="file_input")
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            items = df.iloc[:, 0].dropna().astype(str).tolist()
        except Exception as e:
            st.error(f"File Error: {e}")

# --- 5. BUTTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("PICK A WINNER", use_container_width=True):
        if items:
            winner = random.choice(items)
            st.balloons()
            st.markdown(f"""
                <div style="border: 2px solid #A9A9A9; padding: 20px; text-align: center; border-radius: 10px; background-color: rgba(0,0,0,0.5);">
                    <h1 style='color: white; font-size: 40px;'>🎉 {winner} 🎉</h1>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No data found! Please paste names or upload a file.")

with col2:
    # This button triggers the reset_app function defined above
    if st.button("RESET EVERYTHING", use_container_width=True, on_click=reset_app):
        pass # The on_click handles the logic
