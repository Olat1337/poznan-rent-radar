import os
import streamlit as st
import requests

CONFIG_DIR = ".streamlit"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        f.write("""
[theme]
base="dark"
primaryColor="#38bdf8"
backgroundColor="#0f1116"
secondaryBackgroundColor="#1e293b"
textColor="#f8fafc"
font="sans serif"
        """)

st.set_page_config(
    page_title="Poznań Rent Radar | Valuation Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Dark Theme App Overrides */
    .stApp { background-color: transparent; }

    /* Main Header - Dark Gradient */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #1e293b;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .header-title { font-size: 2.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.2rem; }
    .header-subtitle { font-size: 1rem; color: #94a3b8; font-weight: 400; }

    /* Result Display (Neon Dark Mode Box) */
    .valuation-box {
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
        animation: fadeIn 0.5s ease-out;
    }
    .valuation-label {
        font-size: 0.85rem;
        color: #7dd3fc;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0;
    }
    .valuation-price {
        font-size: 3rem;
        font-weight: 900;
        color: #e0f2fe;
        margin: 0.5rem 0;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }
    .valuation-subtext {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.5;
        margin-top: 1rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <div class="header-title">⚡ Poznań Rent Radar</div>
        <div class="header-subtitle">Predictive Valuation Engine • Automated Machine Learning Infrastructure</div>
    </div>
""", unsafe_allow_html=True)

left_panel, right_panel = st.columns([1.2, 1], gap="large")

with left_panel:
    with st.container(border=True):
        st.subheader("📐 Structural Dimensions")

        # Row 1: Area Slider and Floor Number
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            area = st.slider("Total Living Area (sqm)", min_value=15, max_value=120, value=45, step=1)
        with row1_col2:
            floor_num = st.number_input("Floor Level (-1: Cellar)", min_value=-1, max_value=12, value=1, step=1)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            rooms_num = st.selectbox("Total Rooms", options=[1, 2, 3, 4, 5, 6, 7], index=1)
        with row2_col2:
            location = st.selectbox("Geographic Sector", options=[
                "Jeżyce", "Stare Miasto", "Centrum", "Wilda", "Grunwald",
                "Nowe Miasto", "Rataje", "Winogrady", "Łacina", "Naramowice",
                "Piątkowo", "Świerczewo", "Junikowo", "Kasztelanów", "Podolany"
            ])

    with st.container(border=True):
        st.subheader("✨ Premium Amenities")
        col_c, col_d = st.columns(2)
        with col_c:
            has_ac = st.checkbox("🔄 Air Conditioning")
            has_balcony = st.checkbox("🌅 Balcony Available")
            has_terrace = st.checkbox("🌿 Outdoor Terrace")
        with col_d:
            has_parking = st.checkbox("🚗 Dedicated Parking")
            has_storage = st.checkbox("📦 Secure Storage")
            is_secure = st.checkbox("🛡️ Secured Building")

    st.write("")  # Spacing
    calculate_clicked = st.button("RUN INFERENCE ENGINE", type="primary", use_container_width=True)

with right_panel:
    with st.container(border=True):
        st.subheader("📊 Model Diagnostics")
        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Algorithm", value="Random Forest")
        # Removed the delta tag entirely here:
        kpi2.metric(label="Validation MAE", value="397.91 PLN")

    st.write("")  # Spacing

    if not calculate_clicked:
        st.info(
            "💡 **System Ready:** Adjust the parameters on the left and trigger the inference engine to generate a localized market prediction.")
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
            with st.spinner("Analyzing market variances..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_rent = result.get("predicted_fair_rent_pln")

                st.markdown(f"""
                    <div class="valuation-box">
                        <p class="valuation-label">Estimated Fair Market Rent</p>
                        <p class="valuation-price">{predicted_rent:,.2f} PLN</p>
                        <p class="valuation-subtext">
                            Target price calculated via exponential inversion mapping. 
                            Anchored against the <b>{location}</b> premium sub-market tier.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                luxury_score = sum([has_ac, has_balcony, has_terrace, has_parking, has_storage, is_secure]) * 16.6
                st.write("")
                st.progress(int(luxury_score), text=f"Calculated Amenity Index Score: {int(luxury_score)}%")

            else:
                st.error(f"Inference Failure. API Error Code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ Connection Blocked: Could not reach the Backend API. Ensure uvicorn or the Docker backend is running.")