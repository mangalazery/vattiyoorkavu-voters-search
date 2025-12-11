import streamlit as st
import pandas as pd
import glob
import os
import re # 👈 NEW: Required for safely escaping special characters in the search term

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
    if os.path.exists("Candidate.jpg"):
        st.image("Candidate.jpg", use_container_width=True)
    else:
        st.info("Candidate Image Required")

# --- 4. DATA ENGINE (Updated for Data Type Consistency) ---
@st.cache_data
def load_combined_data():
    files = glob.glob("csv_data/*.csv")
    if not files: return pd.DataFrame()
    
    df_list = [pd.read_csv(f, encoding='latin1') for f in files]
    voter_df = pd.concat(df_list, ignore_index=True)
    
    # CRITICAL ENHANCEMENT: Ensure search columns are strings for reliable partial matching
    if 'Name' in voter_df.columns:
        voter_df['Name'] = voter_df['Name'].astype(str)
    if 'New SEC ID No.' in voter_df.columns:
        voter_df['New SEC ID No.'] = voter_df['New SEC ID No.'].astype(str)
        
    return voter_df

voter_df = load_combined_data()

# --- 5. SEARCH INTERFACE (Updated for Live Search Robustness) ---
if not voter_df.empty:
    st.markdown('<div class="registry-box">', unsafe_allow_html=True)
    st.write("### 🔍 Search Voter Registry (Live Filtering)")
    s1, s2 = st.columns(2)
    
    with s1:
        # st.text_input causes instant rerun, enabling live search
        q_name = st.text_input("👤 Voter Name", placeholder="Start typing name...", key="name_input").strip()
    with s2:
        q_id = st.text_input("🆔 SEC ID Number", placeholder="Start typing ID...", key="id_input").strip()
        
    st.markdown('</div>', unsafe_allow_html=True)

    results = voter_df.copy()
    
    # 1. Filter by Name (Live, Case-Insensitive, Partial Match)
    if q_name:
        # re.escape treats characters like '(' or '.' as literal text, preventing search errors
        escaped_name = re.escape(q_name)
        results = results[
            # regex=True is required when using re.escape
            results['Name'].str.contains(escaped_name, case=False, na=False, regex=True)
        ]
        
    # 2. Filter by ID (Live, Partial Match)
    if q_id:
        escaped_id = re.escape(q_id)
        results = results[
            results['New SEC ID No.'].str.contains(escaped_id, na=False, regex=True)
        ]

    if q_name or q_id:
        st.success(f"Matches Found: {len(results):,}")
        
        display_cols = ['Serial No.', 'Name', "Guardian's Name", 'OldWard No/ House No.', 
                        'House Name', 'Gender / Age', 'New SEC ID No.', 'Polling Station']
        
        st.dataframe(results[display_cols], use_container_width=True, hide_index=True)
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Registered Voters", f"{len(voter_df):,}")
        m2.metric("Ward Portions", "6 Portions")
        m3.metric("Ward", "Vattiyoorkavu")
else:
    st.error("Data missing in 'csv_data/' folder. Please ensure your CSV files are present.")

# --- 6. BOTTOM BANNER ---
st.markdown("---")
st.markdown('<div class="bottom-branding">', unsafe_allow_html=True)
if os.path.exists("Flag.jpg"):
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f2:
        st.image("Flag.jpg", caption="CPI(M) Flag", use_container_width=True)
st.write("Vattiyoorkavu Ward Management System v1.0")
st.write("Designed by Shabna Salam A | Provided by Shabz Software Solutions")
st.markdown('</div>', unsafe_allow_html=True)


