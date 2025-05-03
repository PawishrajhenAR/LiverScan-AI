# app.py
import os
import numpy as np
import cv2
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'nii', 'nii.gz', 'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the pre-trained model
MODEL_PATH = 'capsnet_liver_segmentation.h5'
model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_keras_model():
    global model
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def preprocess_image(image):
    # Resize to 128x128
    image = cv2.resize(image, (128, 128))
    
    # Convert to RGB if grayscale
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    # Normalize pixel values
    image = image.astype(np.float32) / 255.0
    
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image based on file type
        if filename.endswith(('.nii', '.nii.gz')):
            try:
                import nibabel as nib
                img = nib.load(filepath)
                img_data = img.get_fdata()
                
                # Take a middle slice for demonstration
                slice_idx = img_data.shape[2] // 2
                slice_data = img_data[:, :, slice_idx]
                
                # Normalize and resize
                slice_data = cv2.normalize(slice_data, None, 0, 255, cv2.NORM_MINMAX)
                slice_data = slice_data.astype(np.uint8)
                
                # Save the original slice as PNG for display
                slice_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename.split('.')[0]}_slice.png")
                cv2.imwrite(slice_path, slice_data)
                
                # Prepare for prediction
                input_data = preprocess_image(slice_data)
            except Exception as e:
                return jsonify({'error': f'Error processing NIfTI file: {str(e)}'})
        else:
            try:
                # For regular image files
                img = cv2.imread(filepath)
                if img is None:
                    return jsonify({'error': 'Could not read image file'})
                
                # Save original for display
                slice_path = filepath
                
                # Prepare for prediction
                input_data = preprocess_image(img)
            except Exception as e:
                return jsonify({'error': f'Error processing image file: {str(e)}'})
        
        # Make prediction
        if model is None:
            if not load_keras_model():
                return jsonify({'error': 'Model could not be loaded'})
        
        try:
            prediction = model.predict(input_data)
            
            # Process prediction mask
            pred_mask = (prediction[0] > 0.5).astype(np.uint8) * 255
            
            # Resize mask back to original size for display
            original_img = cv2.imread(slice_path)
            original_size = (original_img.shape[1], original_img.shape[0])
            pred_mask = cv2.resize(pred_mask, original_size)
            
            # Save mask
            mask_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename.split('.')[0]}_mask.png")
            cv2.imwrite(mask_path, pred_mask)
            
            # Create colored mask for overlay
            colored_mask = np.zeros_like(original_img)
            colored_mask[:, :, 2] = pred_mask  # Red channel
            
            # Create overlay
            overlay = cv2.addWeighted(original_img, 0.7, colored_mask, 0.3, 0)
            overlay_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename.split('.')[0]}_overlay.png")
            cv2.imwrite(overlay_path, overlay)
            
            return jsonify({
                'success': True,
                'original': f"/static/uploads/{filename.split('.')[0]}_slice.png" if filename.endswith(('.nii', '.nii.gz')) else f"/static/uploads/{filename}",
                'mask': f"/static/uploads/{filename.split('.')[0]}_mask.png",
                'overlay': f"/static/uploads/{filename.split('.')[0]}_overlay.png"
            })
        
        except Exception as e:
            return jsonify({'error': f'Error during prediction: {str(e)}'})
    
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    load_keras_model()
    app.run(debug=True)
