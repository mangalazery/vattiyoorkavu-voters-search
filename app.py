import streamlit as st
import pandas as pd
import glob
import os

# --- 1. PAGE CONFIG & ICON ---
st.set_page_config(page_title="Vattiyoorkavu Voters Search", layout="wide", page_icon="🗳️")

# --- 2. ADVANCED STYLING (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    
    .ward-banner {
        background: linear-gradient(90deg, #de1e22 0%, #1e3a8a 100%);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        margin: 10px 0;
    }
    .ward-title { font-size: 52px; font-weight: 900; line-height: 1.1; }
    .designer-sub { font-size: 18px; font-weight: 300; opacity: 0.9; margin-top: 10px; }

    .registry-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-top: 6px solid #de1e22;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    .bottom-branding {
        text-align: center;
        padding: 20px;
        border-top: 2px solid #cbd5e1;
        margin-top: 60px;
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP ASSET BAR: SYMBOL | TITLE | CANDIDATE ---
col_left, col_center, col_right = st.columns([1, 4, 1])

with col_left:
    if os.path.exists("symbol.png"):
        st.image("symbol.png", use_container_width=True)

with col_center:
    st.markdown(f"""
        <div class="ward-banner">
            <div class="ward-title">Vattiyoorkavu Ward<br>Voters Search</div>
            <div class="designer-sub">Technology by <b>Shabz Software Solutions</b> | Created by <b>Shabna Salam A</b></div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    # Updated to capitalized "Candidate.jpg"
    if os.path.exists("Candidate.jpg"):
        st.image("Candidate.jpg", use_container_width=True)
    else:
        st.info("Candidate Image Required")

# --- 4. DATA ENGINE ---
@st.cache_data
def load_combined_data():
    files = glob.glob("csv_data/*.csv")
    if not files: return pd.DataFrame()
    # Ensure all columns are treated as strings to handle mixed types correctly during search
    try:
        df_list = []
        for f in files:
            # Read and convert all columns to string
            df = pd.read_csv(f, encoding='latin1')
            df_list.append(df.astype(str))
        return pd.concat(df_list, ignore_index=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

voter_df = load_combined_data()

# --- 5. SEARCH INTERFACE ---
if not voter_df.empty:
    
    # --- Search Inputs ---
    st.markdown('<div class="registry-box">', unsafe_allow_html=True)
    st.write("### 🔍 Search Voter Registry")
    s1, s2 = st.columns(2)
    
    # Define text inputs
    with s1:
        q_name = st.text_input("👤 Voter Name", placeholder="Enter name...", key='name_input')
    with s2:
        q_id = st.text_input("🆔 SEC ID Number", placeholder="SEC034...", key='id_input')
        
    st.markdown('</div>', unsafe_allow_html=True)

    
    is_searching = bool(q_name or q_id)
    results = voter_df.copy()

    # --- Filtering Logic (Search-As-You-Type) ---
    if q_name:
        # Case-insensitive search on the 'Name' column
        results = results[results['Name'].str.contains(q_name, case=False, na=False)]
        
    if q_id:







