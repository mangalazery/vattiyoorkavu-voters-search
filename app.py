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
        /* Add fixed height or padding to prevent content shift */
        min-height: 120px; 
    }

    .bottom-branding {
        text-align: center;
        padding: 20px;
        border-top: 2px solid #cbd5e1;
        margin-top: 60px;
        color: #475569;
    }
    /* Custom style for the expander title to allow HTML formatting */
    /* Use a direct reference to the Streamlit expander button for better targeting */
    [data-testid="stExpander"] button {
        background-color: #f7f7f7 !important; 
        border-radius: 8px !important;
        margin-bottom: 5px;
        padding: 10px 15px;
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

# --- 4. DATA ENGINE ---
@st.cache_data
def load_combined_data():
    files = glob.glob("csv_data/*.csv")
    if not files: return pd.DataFrame()
    try:
        df_list = []
        for f in files:
            df = pd.read_csv(f, encoding='latin1')
            df_list.append(df.astype(str))
        return pd.concat(df_list, ignore_index=True)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

voter_df = load_combined_data()

# --- 5. SEARCH INTERFACE ---
if not voter_df.empty:
    
    # --- Search Inputs (ALWAYS VISIBLE) ---
    st.markdown('<div class="registry-box">', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    
    with s1:
        q_name = st.text_input("👤 Voter Name", placeholder="Enter name...", key='name_input')
    with s2:
        q_id = st.text_input("🆔 SEC ID Number", placeholder="SEC034...", key='id_input')
        
    st.markdown('</div>', unsafe_allow_html=True)

    
    is_searching = bool(q_name or q_id)
    results = voter_df.copy()

    # --- Filtering Logic (Incremental Search) ---
    if q_name:
        results = results[results['Name'].str.contains(q_name, case=False, na=False)]
        
    if q_id:
        results = results[results['New SEC ID No.'].str.contains(q_id, na=False)]

    # --- DISPLAY LOGIC (Flicker Fix) ---
    
    # Use a container to hold the dynamic results. This helps manage the area.
    result_container = st.container()

    if is_searching:
        num_results = len(results)
        result_container.success(f"Matches Found: {num_results:,}")
        
        if num_results > 0:
            for index, row in results.iterrows():
                serial_no = row.get('Serial No.', 'N/A')
                sec_id = row.get('New SEC ID No.', 'N/A')
                
                # --- FIX FOR FLICKERING: Use a unique, persistent key for the expander ---
                # The key must be stable across reruns for the open/close state to persist.
                expander_key = f"voter_{sec_id}_{serial_no}" 
                
                expander_title = f"<span style='color: #de1e22; font-weight: bold;'>{row.get('Name', 'Name N/A')}</span> | ID: {sec_id}"
                
                # Use the container to place the result list
                with result_container.expander(expander_title, expanded=False, key=expander_key):
                    st.markdown(f"**Serial No.:** {serial_no}")
                    st.markdown(f"**Guardian's Name:** {row.get('Guardian\'s Name', 'N/A')}")
                    st.markdown(f"**Gender / Age:** {row.get('Gender / Age', 'N/A')}")
                    st.markdown(f"**House No.:** {row.get('OldWard No/ House No.', 'N/A')}")
                    st.markdown(f"**House Name:** {row.get('House Name', 'N/A')}")
                    st.markdown(f"**Polling Station:** {row.get('Polling Station', 'N/A')}")
                    
        else:
            result_container.warning("No matching records found. Try refining your search.")

    else:
        # Only show metrics when no search is active
        m1, m2, m3 = st.columns(3)
        m1.metric("Registered Voters", f"{len(voter_df):,}")
        m2.metric("Ward Portions", "6 Portions")
        m3.metric("Ward", "Vattiyoorkavu")

else:
    st.error("Data missing in 'csv_data/' folder or data loading failed.")
    
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










