import streamlit as st
import pandas as pd
import os

# --- 1. Data Loading Function with Caching ---
# Caching ensures the data is loaded from the file only once when the app starts, 
# significantly speeding up performance for large datasets.
@st.cache_data
def load_data():
    # --- ⚠️ ACTION REQUIRED: Update this filename to match your cleaned data file ---
    DATA_FILE = 'voter_data.csv' 
    
    if os.path.exists(DATA_FILE):
        try:
            # Assuming your clean extracted data is saved in a CSV file
            df = pd.read_csv(DATA_FILE)
            
            # Ensure the search column is a string for proper filtering
            if 'Voter_Name' in df.columns:
                df['Voter_Name'] = df['Voter_Name'].astype(str)
            
            st.success(f"Data successfully loaded. Total records: {len(df)}")
            return df
        
        except Exception as e:
            st.error(f"Error loading data from {DATA_FILE}: {e}")
            return pd.DataFrame() 
    else:
        # --- Mock Data for Demonstration (Will run if 'voter_data.csv' is not found) ---
        st.warning(f"Could not find '{DATA_FILE}'. Using mock data for demonstration.")
        return pd.DataFrame({
            'EPIC_Number': ['ABC1234567', 'XYZ9876543', 'PQR1122334', 'MNO5566778', 'JKL0000001', 'DEF2223334'],
            'Sl_No_In_Part': [1, 2, 3, 4, 5, 6],
            'Voter_Name': ['Anand S Kumar', 'SARASWATHY Amma', 'Rema T P', 'Anil Kumar', 'Ravi Shankar', 'Geetha Nair'],
            'Relative_Name': ['Rajesh S', 'Krishnan N', 'Prabhu T', 'Suresh K', 'Leela', 'Ramachandran P'],
            'House_No_Address': ['H No 1/123, Vattiyoorkavu', 'Kripa Bhavan', 'TC 3/45', 'Anil Nivas', 'Shankar Nivas', 'Geetha Bhavan'],
            'Age': [35, 62, 45, 29, 50, 48],
            'Sex': ['MALE', 'FEMALE', 'FEMALE', 'MALE', 'MALE', 'FEMALE']
        })

# Load the voter data
voter_data = load_data()

# --- 2. Streamlit Application Layout ---
st.set_page_config(page_title="Vattiyoorkavu Voter Search", layout="centered")

st.title("Search Vattiyoorkavu Voter List")
st.markdown("---")

# Check if data was loaded successfully and proceed
if not voter_data.empty:
    
    # --- 3. The Live Search Input ---
    search_term = st.text_input(
        "Enter Voter Name (Type to search):",
        placeholder="Start typing a name (e.g., 'Anil' or 'Saras') for live results...",
        key="name_search_input"
    ).strip() # .strip() cleans up any accidental spaces

    # --- 4. Filtering and Display Logic ---
    if search_term:
        # Core Filtering: Use str.contains() for partial matching.
        # case=False: makes the search case-insensitive (e.g., 'ravi' matches 'Ravi').
        # na=False: treats missing names as not matching.
        filtered_data = voter_data[
            voter_data['Voter_Name'].str.contains(search_term, case=False, na=False)
        ]

        # Display results
        num_matches = len(filtered_data)
        
        if num_matches > 0:
            st.success(f"✅ Found **{num_matches}** matching voters.")
            
            # Define columns to display
            columns_to_display = ['EPIC_Number', 'Sl_No_In_Part', 'Voter_Name', 'Relative_Name', 'House_No_Address', 'Age', 'Sex']
            
            # Use st.dataframe for an interactive, clean table
            st.dataframe(
                filtered_data[columns_to_display],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning(f"No voters found matching '**{search_term}**'. Try a different spelling or a shorter part of the name.")
    else:
        # Prompt user when the search box is empty
        st.info(f"Please enter the name or part of the name of a voter to begin the live search. (Total records: {len(voter_data)})")

