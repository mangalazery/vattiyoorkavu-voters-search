import streamlit as st
import pandas as pd
import glob
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Vattiyoorkavu Voters Search", layout="wide", page_icon="🗳️")

# --- 2. ADVANCED STYLING (CSS) ---
# Custom CSS for Shabz Software Solutions branding
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    
    /* Massive Central Banner for Title */
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

    /* Search Registry Card */
    .registry-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-top: 6px solid #de1e22;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* Fixed Bottom Banner for Flag & Branding */
    .bottom-branding {
        text-align: center;
        padding: 20px;
        border-top: 2px solid #cbd5e1;
        margin-top: 60px;
        color: #475569;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP ASSET BAR: SYMBOL (LEFT) | TITLE (CENTER) | CANDIDATE (RIGHT) ---
col_left, col_center, col_right = st.columns([1, 4, 1])

with col_left:
    if os.path.exists("symbol.png"):
        st.image("symbol.png", use_container_width=True)
    else:
        st.info("ℹ️ Symbol Left")

with col_center:
    st.markdown(f"""
        <div class="ward-banner">
            <div class="ward-title">Vattiyoorkavu Ward<br>Voters Search</div>
            <div class="designer-sub">Technology by <b>Shabz Software Solutions</b> | Created by <b>Shabna Salam A</b></div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    if os.path.exists("candidate.jpg"):
        st.image("candidate.jpg", caption="Our Candidate", use_container_width=True)
    else:
        st.info("ℹ️ Candidate Right")

# --- 4. DATA ENGINE (LATIN-1 FIX) ---
@st.cache_data
def load_combined_data():
    files = glob.glob("csv_data/*.csv")
    if not files: return pd.DataFrame()
    # Combined with latin1 to handle characters like byte 0xa0 found in content
    return pd.concat([pd.read_csv(f, encoding='latin1') for f in files], ignore_index=True)

voter_df = load_combined_data()

# --- 5. INTERACTIVE SEARCH INTERFACE ---
if not voter_df.empty:
    st.markdown('<div class="registry-box">', unsafe_allow_html=True)
    st.write("### 🔍 Search Voter Registry")
    s1, s2 = st.columns(2)
    with s1:
        q_name = st.text_input("👤 Voter Name", placeholder="Type name here...")
    with s2:
        q_id = st.text_input("🆔 New SEC ID No.", placeholder="Type SEC ID here...")
    st.markdown('</div>', unsafe_allow_html=True)

    # Filtering Logic
    results = voter_df.copy()
    if q_name:
        results = results[results['Name'].str.contains(q_name, case=False, na=False)]
    if q_id:
        results = results[results['New SEC ID No.'].astype(str).str.contains(q_id, na=False)]

    # Result Display
    if q_name or q_id:
        st.success(f"Matches Found: {len(results)}")
        # Specific columns from user CSV: Serial No., Name, Guardian's Name, OldWard No/ House No., House Name, Gender / Age, New SEC ID No., Polling Station
        display_cols = ['Serial No.', 'Name', "Guardian's Name", 'OldWard No/ House No.', 
                        'House Name', 'Gender / Age', 'New SEC ID No.', 'Polling Station']
        
        st.dataframe(results[display_cols], use_container_width=True, hide_index=True)
    else:
        # Welcome Ward Statistics
        m1, m2, m3 = st.columns(3)
        m1.metric("Registered Voters", f"{len(voter_df):,}")
        m2.metric("Ward Portions", "6 Portions")
        m3.metric("Ward Number", "Vattiyoorkavu")
        st.info("💡 Start typing a Name or ID to filter the record.")
else:
    st.error("⚠️ Data files not detected! Please ensure the CSV files are in the 'csv_data' folder.")

# --- 6. BOTTOM BANNER: FLAG & COMPANY PRIDE ---
st.markdown("---")
st.markdown('<div class="bottom-branding">', unsafe_allow_html=True)

if os.path.exists("flag.jpg"):
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f2:
        st.image("flag.jpg", caption="CPI(M) Flag - Party Pride", use_container_width=True)

st.write("Vattiyoorkavu Ward Management System v1.0")
st.write("Developed for Shabna Salam A | Provided by **Shabz Software Solutions**")
st.markdown('</div>', unsafe_allow_html=True)