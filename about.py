import streamlit as st

st.set_page_config(page_title="PulmoInsight - Documentation", page_icon="📄", layout="wide")

st.title("📄 About PulmoInsight Architecture")

st.markdown("""
### Model Specifications & Training
This neural network was engineered using TensorFlow/Keras to assist oncology teams with fast triage workflows. 

| Metric Component | Value Specification |
| :--- | :--- |
| **Base Architecture** | Deep Convolutional Neural Network (CNN) |
| **Input Matrix Dimensions** | $224 \times 224 \times 3$ (RGB) |
| **Target Dataset Source** | LC25000 Lung & Colon Histopathology |
| **Optimization Weights Format** | Native Keras Serialization (`model.keras`) |

---

### Understanding the Diagnostic Classifications
* **Adenocarcinoma:** Glandular cancer formations that typically develop in peripheral areas of the lung tissue framework.
* **Squamous Cell Carcinoma:** Flat cell structures arising centrally within the major airway passages.
* **Benign:** Microscopic tissue displaying uniform cellular profiles, intact cell margins, and normal mitotic counts.

### Institutional Support
For system integration requests, DICOM connection configurations, or to report edge-case errors, please reach out to the medical informatics systems administrator.
""")