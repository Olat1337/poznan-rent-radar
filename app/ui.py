import os
import streamlit as st
import requests

# 1. Automatic Streamlit Configuration
CONFIG_DIR = ".streamlit"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)

with open(CONFIG_FILE, "w") as f:
    f.write("""
[theme]
base="dark"
primaryColor="#5c6ac4"
backgroundColor="#0d0d12"
secondaryBackgroundColor="#16161e"
textColor="#e4e4e7"
font="sans serif"
    """)

# 2. Page Setup
st.set_page_config(
    page_title="Poznań Rent Radar",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. Custom CSS
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }

    footer {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
    }

    [data-testid="column"] > div > div {
        gap: 0.2rem !important;
    }

    .stApp { 
        background-color: #0d0d12 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #272733 !important; 
        border-radius: 12px !important;
        background-color: #16161e !important;
        padding: 0.6rem 1rem !important;
    }

    .main-header {
        background-color: transparent;
        padding: 0.2rem 0.5rem 0.8rem 0.5rem;
        text-align: left;
    }
    .header-tag {
        color: #5c6ac4;
        font-family: monospace;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .header-title { 
        font-size: 2.3rem; 
        font-weight: 700; 
        color: #f8f8f2; 
        margin-bottom: 0.2rem; 
        letter-spacing: -0.5px;
    }
    .header-subtitle { 
        font-size: 1rem; 
        color: #a0a0ab; 
        font-weight: 500; 
    }

    .valuation-box {
        background-color: #1e1e29;
        border: 1px solid #2d2d3d;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: left;
        margin-top: 0.2rem;
    }
    .valuation-label {
        font-size: 0.9rem;
        color: #a0a0ab; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .valuation-price {
        font-size: 2.4rem;
        font-weight: 700;
        color: #f8f8f2;
        margin: 0.2rem 0;
    }
    .valuation-subtext {
        font-size: 0.9rem;
        color: #a0a0ab;
        line-height: 1.3;
        margin-top: 0.2rem;
    }

    .custom-info-box {
        background-color: #1e1e29;
        border: 1px solid #2d2d3d;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: #a0a0ab;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }

    div.stButton > button:first-child {
        background-color: #5c6ac4 !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        height: 2.8rem;
        font-size: 1.05rem !important;
        margin-top: 0.4rem !important;
        transition: background-color 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #6d7ad8 !important; 
    }

    .stSelectbox div[data-baseweb="select"], 
    .stNumberInput div[data-baseweb="input"] {
        border-color: #2d2d3d !important;
        background-color: #1e1e29 !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
    }

    div[data-baseweb="slider"] div[data-testid="stTickBar"] > div {
        background-color: #5c6ac4 !important;
    }

    *:focus {
        outline-color: #5c6ac4 !important;
    }

    h3 {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #e4e4e7 !important;
        padding-bottom: 0.4rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: #f8f8f2 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0ab !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stCheckbox"] label span {
        color: #a0a0ab !important;
        font-size: 0.95rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. App Header
st.markdown("""
    <div class="main-header">
        <div class="header-tag">For {data_scientists}</div>
        <div class="header-title">Poznań Rent Radar</div>
        <div class="header-subtitle">A tool for data-driven rental estimations.</div>
    </div>
""", unsafe_allow_html=True)

# 5. Application Layout
left_panel, right_panel = st.columns([1.2, 1], gap="medium")

with left_panel:
    with st.container(border=True):
        st.subheader("Apartment Attributes")

        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            area = st.slider("Living Area (sqm)", min_value=15, max_value=120, value=45, step=1)
        with row1_col2:
            floor_num = st.number_input("Floor Level", min_value=-1, max_value=12, value=1, step=1)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            rooms_num = st.selectbox("Rooms", options=[1, 2, 3, 4, 5, 6, 7], index=1)
        with row2_col2:
            location = st.selectbox("Location / District", options=[
                "Jeżyce", "Stare Miasto", "Centrum", "Wilda", "Grunwald",
                "Nowe Miasto", "Rataje", "Winogrady", "Łacina", "Naramowice",
                "Piątkowo", "Świerczewo", "Junikowo", "Kasztelanów", "Podolany"
            ])

    with st.container(border=True):
        st.subheader("Amenities & Features")
        col_c, col_d = st.columns(2)
        with col_c:
            has_ac = st.checkbox("Air Conditioning")
            has_balcony = st.checkbox("Balcony")
            has_terrace = st.checkbox("Terrace / Garden")
        with col_d:
            has_parking = st.checkbox("Parking Space")
            has_storage = st.checkbox("Storage Unit")
            is_secure = st.checkbox("Security / Surveillance")

    calculate_clicked = st.button("Calculate Rent Estimate", use_container_width=True)

with right_panel:
    with st.container(border=True):
        st.subheader("Model Information")
        st.markdown(
            "<span style='color: #a0a0ab; font-size: 0.95rem;'>This estimate uses current real estate data in Poznań.</span>",
            unsafe_allow_html=True)
        st.write("")

        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Model Margin of Error", value="± 337 PLN")
        kpi2.metric(label="Dataset Status", value="Synchronized")

    if not calculate_clicked:
        st.markdown("""
            <div class="custom-info-box">
                Fill out the apartment profile on the left and click <b>Calculate Rent Estimate</b> to display the value.
            </div>
        """, unsafe_allow_html=True)
    else:
        payload = {
            "area": float(area), "floor_num": int(floor_num), "rooms_num": int(rooms_num),
            "has_ac": bool(has_ac), "has_balcony": bool(has_balcony), "has_terrace": bool(has_terrace),
            "has_parking": bool(has_parking), "has_storage": bool(has_storage), "is_secure": bool(is_secure),
            "location": str(location)
        }

        BACKEND_HOST = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
        API_URL = f"{BACKEND_HOST}/predict"

        try:
            with st.spinner("Processing data..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_rent = result.get("predicted_fair_rent_pln")

                st.markdown(f"""
                    <div class="valuation-box">
                        <p class="valuation-label">Estimated Market Value</p>
                        <p class="valuation-price">{predicted_rent:,.0f} PLN</p>
                        <p class="valuation-subtext">
                            Average rent for this profile in <b>{location}</b>.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            else:
                st.error("Error processing the request. Please check your inputs.")

        except requests.exceptions.ConnectionError:
            st.error("API Unreachable: Cannot connect to the local backend service.")