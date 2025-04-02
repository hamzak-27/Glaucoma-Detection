"""
Glaucoma detection utility functions for the Django application.
These functions handle the AI model loading and prediction.
"""

import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input

from django.conf import settings

# Global variables
MODEL = None
CLASS_NAMES = ["Glaucoma Negative", "Glaucoma Positive"]

def load_glaucoma_model():
    """
    Load the trained glaucoma detection model.
    Returns the model or None if there was an error.
    """
    global MODEL
    
    # Only load the model if it hasn't been loaded yet
    if MODEL is None:
        try:
            model_path = os.path.join(settings.BASE_DIR, 'models', 'ResNet50_final.keras')
            MODEL = load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    return MODEL

def prepare_image(image_path):
    """
    Prepare an image for prediction.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed image array
    """
    # Load and resize image
    img = Image.open(image_path)
    img = img.resize((224, 224))
    
    # Convert to array and add batch dimension
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess for ResNet50
    img_array = preprocess_input(img_array)
    
    return img_array

def predict_glaucoma(image_path):
    """
    Make a prediction on a single image.
    
    Args:
        image_path: Path to the image
        
    Returns:
        Dictionary with prediction results
    """
    # Load model if needed
    model = load_glaucoma_model()
    if model is None:
        raise Exception("Failed to load model")
    
    # Measure processing time
    start_time = time.time()
    
    # Prepare image
    img_array = prepare_image(image_path)
    
    # Make prediction
    prediction = model.predict(img_array)[0][0]
    
    # Determine class
    is_glaucoma = prediction > 0.5
    predicted_class = CLASS_NAMES[1] if is_glaucoma else CLASS_NAMES[0]
    confidence = prediction if is_glaucoma else 1 - prediction
    
    # Calculate processing time
    processing_time = time.time() - start_time
    
    # Return results
    return {
        'is_glaucoma': is_glaucoma,
        'predicted_class': predicted_class,
        'raw_score': float(prediction),
        'confidence': float(confidence * 100),
        'processing_time': processing_time
    }

def generate_result_visualization(image_path, result):
    """
    Generate a visualization of the prediction result.
    
    Args:
        image_path: Path to the image
        result: Prediction result dictionary
        
    Returns:
        Path to the saved visualization image
    """
    # Load image
    img = Image.open(image_path)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot image
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title(f"Fundus Image")
    plt.axis('off')
    
    # Plot prediction
    plt.subplot(1, 2, 2)
    
    # Create a horizontal bar chart
    labels = CLASS_NAMES
    scores = [1 - result['raw_score'], result['raw_score']]
    colors = ['green', 'red']
    
    bars = plt.barh(labels, scores, color=colors)
    plt.xlim(0, 1)
    plt.title('Prediction Probabilities')
    plt.xlabel('Probability')
    
    # Add percentage labels inside the bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(max(0.05, width/2), bar.get_y() + bar.get_height()/2,
                f"{scores[i]*100:.1f}%", ha='center', va='center',
                color='white' if scores[i] > 0.3 else 'black', fontweight='bold')
    
    # Add result as text
    result_text = f"Prediction: {result['predicted_class']}\nConfidence: {result['confidence']:.1f}%"
    plt.figtext(0.5, 0.01, result_text, ha='center', fontsize=12, 
                bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})
    
    plt.tight_layout()
    
    # Save to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return buf