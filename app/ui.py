import streamlit as st
import requests

st.set_page_config(
    page_title="Poznań Rent Radar | Enterprise Valuation Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Global App Overrides */
    .stApp { background-color: #F8FAFC; }

    /* Typography & Custom Card Blocks */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        padding: 30px;
        border-radius: 16px;
        color: #FFFFFF;
        text-align: center;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
        margin-bottom: 30px;
    }
    .header-title { font-size: 38px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 5px; }
    .header-subtitle { font-size: 16px; color: #93C5FD; font-weight: 400; opacity: 0.9; }

    /* Result Display (WOW Box) */
    .valuation-box {
        background: radial-gradient(circle at top left, #EFF6FF, #DBEAFE);
        border: 2px solid #3B82F6;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.1);
        animation: fadeIn 0.6s ease-out;
    }
    .valuation-price {
        font-size: 48px;
        font-weight: 900;
        color: #1D4ED8;
        letter-spacing: -1px;
        margin: 10px 0;
    }

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

left_panel, right_panel = st.columns([3, 2], gap="large")

with left_panel:
    st.subheader("📐 Structural Dimension Metrics")
    col_a, col_b = st.columns(2)
    with col_a:
        area = st.slider("Total Living Area (sqm)", min_value=15, max_value=120, value=45, step=1)
        rooms_num = st.selectbox("Total Rooms Metric", options=[1, 2, 3, 4, 5, 6, 7], index=1)
    with col_b:
        floor_num = st.number_input("Floor Level (-1: Cellar, 0: Ground)", min_value=-1, max_value=12, value=1, step=1)
        location = st.selectbox("Geographic Market Sector", options=[
            "Jeżyce", "Stare Miasto", "Centrum", "Wilda", "Grunwald",
            "Nowe Miasto", "Rataje", "Winogrady", "Łacina", "Naramowice",
            "Piątkowo", "Świerczewo", "Junikowo", "Kasztelanów", "Podolany"
        ])

    st.subheader("✨ Premium Features & Amenities")
    col_c, col_d = st.columns(2)
    with col_c:
        has_ac = st.checkbox("🔄 Integrated Air Conditioning")
        has_balcony = st.checkbox("🌅 Balcony Profile Available")
        has_terrace = st.checkbox("🌿 Expanded Private Terrace")
    with col_d:
        has_parking = st.checkbox("🚗 Allocated Parking Infrastructure")
        has_storage = st.checkbox("📦 Secure Basement Storage Unit")
        is_secure = st.checkbox("🛡️ Secured Perimeter Access Controls")

    calculate_clicked = st.button("RUN PREDICTIVE INFERENCE ENGINE", type="primary", use_container_width=True)

with right_panel:
    st.subheader("📊 Live Model Analytics State")

    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Pipeline Target Model", value="Random Forest")
    kpi2.metric(label="Validation Baseline MAE", value="397.91 PLN", delta="-48.09 PLN", delta_color="inverse")

    st.divider()

    if not calculate_clicked:
        st.info(
            "💡 **Inference Ready:** Populate the apartment architectural features on the left configuration panel and trigger the execution button to calculate the optimized fair market rent index valuation.")
    else:
        payload = {
            "area": float(area), "floor_num": int(floor_num), "rooms_num": int(rooms_num),
            "has_ac": bool(has_ac), "has_balcony": bool(has_balcony), "has_terrace": bool(has_terrace),
            "has_parking": bool(has_parking), "has_storage": bool(has_storage), "is_secure": bool(is_secure),
            "location": str(location)
        }

        API_URL = "http://127.0.0.1:8000/predict"

        try:
            with st.spinner("Executing statistical variance weights..."):
                response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_rent = result.get("predicted_fair_rent_pln")

                st.markdown(f"""
                    <div class="valuation-box">
                        <p style="margin:0; font-size:14px; color:#1E40AF; font-weight:700; uppercase; letter-spacing: 1px;">FAIR MARKET VALUATION COMPLETE</p>
                        <p class="valuation-price">{predicted_rent:,.2f} PLN <span style="font-size:18px; font-weight:500; color:#4B5563;">/ month</span></p>
                        <p style="margin: 15px 0 0 0; font-size:13px; color:#4B5563; line-height: 1.4;">
                            Target price calculated via exponential inversion mapping of localized log distributions. 
                            Confidence intervals anchored against the <b>{location}</b> premium sub-market tier.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                luxury_score = sum([has_ac, has_balcony, has_terrace, has_parking, has_storage, is_secure]) * 16.6
                st.markdown("<br>", unsafe_allow_html=True)
                st.slider("Calculated Structural Amenity Index Score (%)", 0.0, 100.0, float(luxury_score),
                          disabled=True)

            else:
                st.error(f"Inference Failure. API Error Code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error(
                "Inference Connection Blocked: The UI component could not map a network connection to the Backend Service. Check that `uvicorn app.api:app` is initialized and monitoring port 8000.")