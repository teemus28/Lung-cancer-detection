import io
import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
import tensorflow as tf
from PIL import Image
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Lung Cancer Classification API",
    description="An API to predict lung cancer types from histopathological images.",
    version="1.0"
)

# Load your trained Keras model
# Ensure 'model.keras' is in the same directory or provide the correct path
try:
    model = tf.keras.models.load_model("model/lung_cancer_vgg16.keras")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")

# Class mapping based on your training labels
CLASS_MAPPING = {
    0: "lung_adenocarcinomas",
    1: "lung_benign_tissue",
    2: "lung_squamous_cell_carcinomas"
}

def pre_process(image_bytes):
    """
    Replicates your exact testing pipeline.
    Reads bytes into a numpy array, decodes it via OpenCV, and resizes it.
    """
    # Convert raw bytes into a numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode image into OpenCV BGR format (matching your cv2.imread testing step)
    test_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if test_img is None:
        raise ValueError("Invalid image format.")

    # Apply your exact preprocessing steps
    # Note: Your test code had 'test_img = test_img/255' commented out. 
    # If your model requires normalization, uncomment the line below:
    # test_img = test_img / 255.0
    
    test_img = cv2.resize(test_img, (224, 224))
    return test_img


@app.get("/")
def home():
    return {
        "message": "Lung Cancer Detection System API Running"
    }
    
    
@app.post("/predict", summary="Predict lung cancer type from an image")
async def predict(file: UploadFile = File(...)):
    # 1. Validate file extension
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid image extension. Only JPG, JPEG, and PNG are allowed.")
    
    try:
        # 2. Read the uploaded file bytes
        image_bytes = await file.read()
        
        # 3. Preprocess the image
        processed_img = pre_process(image_bytes)
        
        # 4. Reshape for model input: (1, 224, 224, 3)
        test_input = np.expand_dims(processed_img, axis=0)
        # 5. Run inference
        predictions = model.predict(test_input)
        
        # 6. Extract and format results
        predicted_class_idx = int(np.argmax(predictions[0]))
        
        # Round the primary confidence score to 2 decimal places
        confidence = round(float(predictions[0][predicted_class_idx]), 2)
        label = CLASS_MAPPING.get(predicted_class_idx, "Unknown")
        
        # Create a dictionary of rounded probabilities for all classes
        all_probabilities = {
            CLASS_MAPPING[i]: round(float(predictions[0][i]), 2) 
            for i in range(len(CLASS_MAPPING))
        }
        
        # Define a basic threshold for a "high confidence" flag
        is_confident = confidence >= 0.70
        
        return {
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "model_version": "1.0.0",
                "filename": file.filename
            },
            "prediction": {
                "label": label,
                "confidence": confidence,
                "high_confidence_alert": is_confident
            },
            "all_probabilities": all_probabilities
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")
    except Exception as e:
        # Catch-all for internal processing/inference errors
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Lung Cancer Classification API is up and running!"}

# uvicorn backend:app --reload