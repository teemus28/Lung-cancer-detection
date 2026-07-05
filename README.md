# 🫁 Lung Cancer Detection using Deep Learning

An AI-powered web application for detecting lung cancer from CT scan images using a deep learning model built with **TensorFlow/Keras**. The project provides a user-friendly **Streamlit** frontend and a high-performance **FastAPI** backend for model inference.

## 🚀 Live Demo

Experience the application without any local setup:

🔗 **Live Demo:** ([https://lungscanai.onrender.com](https://lungscanai.onrender.com/))

> **Disclaimer:** This project is intended for educational and research purposes only. It is **not** a medical diagnostic tool and should not be used as a substitute for professional medical advice or diagnosis.

---

## 📌 Features

- 🔍 Upload lung CT scan images
- 🤖 Deep learning-based prediction using a trained Keras model
- ⚡ FastAPI backend for efficient inference
- 🎨 Interactive Streamlit user interface
- 📊 Displays prediction results with confidence score
- 🖥️ Easy deployment on Render or other cloud platforms

---

## 🏗️ Project Structure

```
Lung-cancer-detection/
│
├── model/
│   └── lung_cancer_model.keras
│
├── uploads/
│
├── .streamlit/
│
├── backend.py          # FastAPI backend
├── frontend.py         # Streamlit frontend
├── requirements.txt
└── README.md
```

---

## 🚀 Tech Stack

- Python
- TensorFlow / Keras
- FastAPI
- Streamlit
- Uvicorn
- NumPy
- Pillow

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/teemus28/Lung-cancer-detection.git
cd Lung-cancer-detection
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Backend

```bash
uvicorn backend:app --reload
```

The FastAPI server will start at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## ▶️ Running the Frontend

```bash
streamlit run frontend.py
```

The Streamlit application will open at:

```
http://localhost:8501
```

---

## 🧠 Model

The application uses a pre-trained **TensorFlow/Keras** model for binary classification of lung CT scan images.

### Prediction Classes

- ✅ Normal
- ⚠️ Lung Cancer Detected

---

## 📷 Workflow

1. Upload a CT scan image.
2. Image is preprocessed.
3. Backend loads the trained Keras model.
4. Model predicts the class.
5. Prediction and confidence score are displayed.

---

## 📦 Deployment

This project can be deployed on:

- Render
- Railway
- Hugging Face Spaces
- Azure App Service
- AWS
- Google Cloud Platform

---

## 📋 Requirements

- Python 3.11 (recommended)
- TensorFlow
- FastAPI
- Streamlit

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📸 Demo

Add screenshots of your application here.

Example:

```
screenshots/home.png
screenshots/result.png
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sumeet Sahu**

- GitHub: https://github.com/teemus28

---

⭐ If you found this project helpful, consider giving it a **star**!
