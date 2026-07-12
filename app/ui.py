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
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
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
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
        <div>
            <div style="color: #5c6ac4; font-family: monospace; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.3rem; text-transform: uppercase; letter-spacing: 1px;">Pricing Engine</div>
            <div style="font-size: 2.4rem; font-weight: 700; color: #f8f8f2; margin-bottom: 0.2rem; letter-spacing: -0.5px;">Poznań Rent Radar</div>
            <div style="font-size: 1.05rem; color: #a0a0ab; font-weight: 500;">Find the fair market rent for any apartment in seconds.</div>
        </div>
        <div style="margin-top: 0.5rem;">
            <a href="https://github.com/Olat1337/poznan-rent-radar" target="_blank" style="color: #e4e4e7; text-decoration: none; font-weight: 600; font-size: 0.95rem; border: 1px solid #5c6ac4; padding: 10px 18px; border-radius: 8px; background-color: rgba(92, 106, 196, 0.1); transition: all 0.2s;">
                🔗 GitHub Repo
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. Application Layout
left_panel, right_panel = st.columns([1.2, 1], gap="medium")

with left_panel:
    with st.container(border=True):
        st.subheader("Apartment Details")

        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            area = st.slider("Living Area (sqm)", min_value=15, max_value=120, value=45, step=1)
        with row1_col2:
            floor_num = st.number_input("Floor Level", min_value=-1, max_value=12, value=1, step=1)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            rooms_num = st.selectbox("Rooms", options=[1, 2, 3, 4, 5, 6, 7], index=1)
        with row2_col2:
            location = st.selectbox("Neighborhood", options=[
                "Jeżyce", "Stare Miasto", "Centrum", "Wilda", "Grunwald",
                "Nowe Miasto", "Rataje", "Winogrady", "Łacina", "Naramowice",
                "Piątkowo", "Świerczewo", "Junikowo", "Kasztelanów", "Podolany"
            ])

    with st.container(border=True):
        st.subheader("Amenities")
        col_c, col_d = st.columns(2)
        with col_c:
            has_ac = st.checkbox("Air Conditioning")
            has_balcony = st.checkbox("Balcony")
            has_terrace = st.checkbox("Terrace / Garden")
        with col_d:
            has_parking = st.checkbox("Parking Space")
            has_storage = st.checkbox("Storage Unit")
            is_secure = st.checkbox("Security / Surveillance")

    calculate_clicked = st.button("Calculate Estimated Rent", use_container_width=True)

with right_panel:
    with st.container(border=True):
        st.subheader("Model Information")
        st.markdown(
            "<span style='color: #a0a0ab; font-size: 0.95rem;'>This tool uses real market data to generate estimates.</span>",
            unsafe_allow_html=True)
        st.write("")

        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Average Error Margin", value="± 307 PLN")
        kpi2.metric(label="Algorithm", value="CatBoost")

    if not calculate_clicked:
        st.markdown("""
            <div class="custom-info-box">
                Fill out the apartment profile on the left and click <b>Calculate Estimated Rent</b> to see the fair market price.
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
            with st.spinner("Analyzing market data..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_rent = result.get("predicted_fair_rent_pln")

                margin_of_error = 307
                lower_bound = max(0, predicted_rent - margin_of_error)
                upper_bound = predicted_rent + margin_of_error

                st.markdown(f"""
                    <div style="background-color: #1e1e29; border: 1px solid #2d2d3d; border-radius: 10px; padding: 1.5rem; text-align: center; margin-top: 0.2rem;">
                        <p style="font-size: 0.9rem; color: #a0a0ab; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin: 0;">Estimated Monthly Rent</p>
                        <p style="font-size: 2.8rem; font-weight: 700; color: #f8f8f2; margin: 0.2rem 0;">{predicted_rent:,.0f} <span style="font-size: 1.2rem; color: #a0a0ab;">PLN</span></p>
                        <div style="margin: 25px 10px 15px 10px;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #a0a0ab; font-weight: 500; margin-bottom: 8px;">
                                <span>{lower_bound:,.0f} PLN</span>
                                <span>{upper_bound:,.0f} PLN</span>
                            </div>
                            <div style="display: flex; width: 100%; height: 14px; background-color: #16161e; border-radius: 7px; overflow: hidden; border: 1px solid #2d2d3d;">
                                <div style="width: 49%; height: 100%; background: linear-gradient(90deg, #16161e, #5c6ac4);"></div>
                                <div style="width: 2%; height: 100%; background-color: #ffffff;"></div>
                                <div style="width: 49%; height: 100%; background: linear-gradient(90deg, #5c6ac4, #16161e);"></div>
                            </div>
                            <div style="text-align: center; font-size: 0.85rem; color: #6b6b7b; margin-top: 10px;">
                                Expected Range (± 307 PLN Margin)
                            </div>
                        </div>
                        <p style="font-size: 0.9rem; color: #a0a0ab; line-height: 1.4; margin-top: 1rem; border-top: 1px solid #2d2d3d; padding-top: 1rem;">
                            Based on current market trends for a {area} sqm apartment in <b>{location}</b>.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            else:
                st.error("Error processing the request. Please check your inputs.")

        except requests.exceptions.ConnectionError:
            st.error("API Unreachable: Cannot connect to the backend server.")