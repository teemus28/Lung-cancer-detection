import streamlit as st
import requests

# =====================================================
# CONFIG
# =====================================================

BACKEND_URL = "https://lung-cancer-detection-2rzx.onrender.com"

CLASS_LABELS = {
    "lung_adenocarcinomas": "Lung Adenocarcinoma",
    "lung_benign_tissue": "Benign Lung Tissue",
    "lung_squamous_cell_carcinomas": "Lung Squamous Cell Carcinoma",
}

st.set_page_config(
    page_title="Lung Cancer Detection",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CUSTOM CSS (white + green, clinical style)
# =====================================================

CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #FFFFFF;
    }
    #MainMenu, footer {visibility: hidden;}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: #F5FBF7;
        border-right: 1px solid #DFF3E6;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* ---- Brand header ---- */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.2rem;
    }
    .brand-logo {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #1E8449, #27AE60);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .brand-title {
        font-size: 21px;
        font-weight: 800;
        color: #14532D;
        margin: 0;
        line-height: 1.1;
    }
    .brand-subtitle {
        font-size: 12px;
        color: #6B8F7A;
        margin: 0;
    }

    /* ---- Hero header ---- */
    .hero-icon {
        width: 64px;
        height: 64px;
        border-radius: 18px;
        background: linear-gradient(135deg, #1E8449, #27AE60);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin: 0 auto 14px auto;
        box-shadow: 0 8px 20px rgba(30, 132, 73, 0.22);
    }
    .hero-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #14532D;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        text-align: center;
        color: #6B8F7A;
        font-size: 16px;
        margin-bottom: 26px;
    }

    /* ---- Cards ---- */
    .lc-card {
        background: #FFFFFF;
        border: 1px solid #E3F3E9;
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 4px 14px rgba(20, 83, 45, 0.05);
    }

    /* ---- Result banners ---- */
    .result-banner-benign {
        background: #E9F9EF;
        border: 1px solid #A9E3BE;
        border-radius: 14px;
        padding: 18px 22px;
        color: #14532D;
    }
    .result-banner-malignant {
        background: #FDEEEE;
        border: 1px solid #F3B9B9;
        border-radius: 14px;
        padding: 18px 22px;
        color: #7A1F1F;
    }
    .result-label {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 2px;
    }
    .result-confidence {
        font-size: 14px;
        opacity: 0.85;
    }

    /* ---- Probability bars ---- */
    .prob-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 8px 0;
    }
    .prob-name {
        width: 230px;
        font-size: 14px;
        color: #1B1B1B;
        font-weight: 600;
    }
    .prob-bar-bg {
        flex: 1;
        background: #EAF6EE;
        border-radius: 8px;
        height: 14px;
        overflow: hidden;
    }
    .prob-bar-fill {
        background: linear-gradient(90deg, #27AE60, #1E8449);
        height: 100%;
        border-radius: 8px;
    }
    .prob-value {
        width: 50px;
        text-align: right;
        font-size: 13px;
        color: #14532D;
        font-weight: 700;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background-color: #1E8449;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.5rem;
        font-weight: 700;
    }
    .stButton > button:hover {
        background-color: #166B3A;
        color: white;
    }

    /* ---- Uploader ---- */
    div[data-testid="stFileUploader"] section {
        border: 1.5px dashed #A9E3BE;
        border-radius: 14px;
        background: #F7FDF9;
    }

    /* ---- Disclaimer ---- */
    .disclaimer-box {
        background: #FFF9E6;
        border: 1px solid #F5E3A0;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 13px;
        color: #6B5B10;
        margin-top: 14px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-logo">🫁</div>
            <div>
                <p class="brand-title">LungScan AI</p>
                <p class="brand-subtitle">Histopathology Classifier</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Classifies lung histopathological images into adenocarcinoma, "
        "benign tissue, or squamous cell carcinoma using a EfficientNetB3 model."
    )

    st.divider()
    st.caption("Model classes")
    for key, display in CLASS_LABELS.items():
        st.markdown(f"- {display}")

    st.divider()
    st.caption("Backend")
    st.code(BACKEND_URL, language=None)

    with st.expander("⚙️ Settings"):
        backend_input = st.text_input("Backend URL", value=BACKEND_URL)
        if backend_input:
            BACKEND_URL = backend_input

    st.divider()
    if st.button("🧹 Clear result", use_container_width=True):
        st.session_state.prediction_result = None
        st.rerun()
        
    LINKEDIN_URL = "https://www.linkedin.com/in/sumeet-sahu-529557291/"
    GITHUB_URL = "https://github.com/teemus28"
    st.divider()
    st.caption("Connect with me")
    st.markdown(
        f"""
        <div style="display:flex; gap:10px; margin-top:4px;">
            <a href="{LINKEDIN_URL}" target="_blank" style="text-decoration:none;">
                <div style="display:flex; align-items:center; gap:6px;
                            background:#F0F0FA; padding:8px 14px; border-radius:10px;
                            color:#1E1E2D; font-weight:600; font-size:14px;">
                    🔗 LinkedIn
                </div>
            </a>
            <a href="{GITHUB_URL}" target="_blank" style="text-decoration:none;">
                <div style="display:flex; align-items:center; gap:6px;
                            background:#F0F0FA; padding:8px 14px; border-radius:10px;
                            color:#1E1E2D; font-weight:600; font-size:14px;">
                    🐙 GitHub
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        """
        <div style="font-size:12px; color:#6B8F7A;">
            Built for research & educational demonstration purposes only.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================
# HERO HEADER
# =====================================================

st.markdown('<div class="hero-icon">🫁</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Lung Cancer Detection</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Upload a histopathological image to classify tissue type using AI.</div>',
    unsafe_allow_html=True,
)

# =====================================================
# MAIN CARD - UPLOAD & PREDICT
# =====================================================

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="lc-card">', unsafe_allow_html=True)
    st.markdown("##### 🔬 Upload Histopathology Image")
    st.caption("Supported formats: JPG, JPEG, PNG")

    uploaded_image = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="lc_image_uploader",
    )

    if uploaded_image is not None:
        st.image(uploaded_image, caption=uploaded_image.name, use_container_width=True)

    predict_clicked = st.button("🧪 Analyze Image", use_container_width=True)

    if predict_clicked:
        if uploaded_image is None:
            st.warning("Please upload an image first.")
        else:
            with st.spinner("Analyzing tissue sample..."):
                try:
                    files = {
                        "file": (uploaded_image.name, uploaded_image.getvalue())
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/predict",
                        files=files,
                        timeout=120,
                    )

                    if response.status_code == 200:
                        st.session_state.prediction_result = response.json()
                    else:
                        st.session_state.prediction_result = None
                        try:
                            detail = response.json().get("detail", response.text)
                        except Exception:
                            detail = response.text
                        st.error(f"Error {response.status_code}: {detail}")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to backend. Is the FastAPI server running?")
                except Exception as e:
                    st.error(f"⚠️ Something went wrong: {e}")

    st.markdown(
        """
        <div class="disclaimer-box">
            ⚠️ This tool is for research and educational demonstration only.
            It is not a certified medical device and must not be used for
            clinical diagnosis. Always consult a qualified pathologist.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# RESULT CARD
# =====================================================

with col_right:
    st.markdown('<div class="lc-card">', unsafe_allow_html=True)
    st.markdown("##### 📊 Prediction Result")

    result = st.session_state.prediction_result

    if result is None:
        st.info("Upload an image and click **Analyze Image** to see results here.")
    else:
        prediction = result.get("prediction", {})
        metadata = result.get("metadata", {})
        all_probs = result.get("all_probabilities", {})

        label_raw = prediction.get("label", "Unknown")
        label_display = CLASS_LABELS.get(label_raw, label_raw)
        confidence = prediction.get("confidence", 0.0)
        high_confidence = prediction.get("high_confidence_alert", False)

        is_benign = label_raw == "lung_benign_tissue"
        banner_class = "result-banner-benign" if is_benign else "result-banner-malignant"
        status_icon = "✅" if is_benign else "🔴"

        st.markdown(
            f"""
            <div class="{banner_class}">
                <div class="result-label">{status_icon} {label_display}</div>
                <div class="result-confidence">Confidence: {confidence * 100:.0f}%
                {"— High confidence" if high_confidence else "— Low confidence, review recommended"}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        st.markdown("**Class probabilities**")

        for class_key, prob in all_probs.items():
            display_name = CLASS_LABELS.get(class_key, class_key)
            pct = max(0.0, min(1.0, float(prob))) * 100
            st.markdown(
                f"""
                <div class="prob-row">
                    <div class="prob-name">{display_name}</div>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill" style="width:{pct}%;"></div>
                    </div>
                    <div class="prob-value">{pct:.0f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        with st.expander("📁 Scan metadata"):
            st.markdown(f"**Filename:** {metadata.get('filename', 'N/A')}")
            st.markdown(f"**Timestamp (UTC):** {metadata.get('timestamp', 'N/A')}")
            st.markdown(f"**Model version:** {metadata.get('model_version', 'N/A')}")

        if not high_confidence:
            st.warning(
                "The model's confidence is below the 70% threshold. "
                "Consider re-scanning the sample or reviewing manually."
            )

    st.markdown('</div>', unsafe_allow_html=True)
