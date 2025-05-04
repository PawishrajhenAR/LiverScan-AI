# Liver Tumor Segmentation Tool

A deep learning-based web application for automated liver tumor segmentation using CapsNet architecture.

## Description

This project implements a web-based tool for liver tumor segmentation using a Capsule Neural Network (CapsNet) architecture. It can process both standard image formats (PNG, JPG, JPEG) and medical imaging formats (NIfTI: .nii, .nii.gz) to detect and segment liver tumors.

## Features

- Interactive web interface for image upload
- Support for multiple image formats:
  - Standard formats: PNG, JPG, JPEG
  - Medical imaging formats: NIfTI (.nii, .nii.gz)
- Real-time segmentation processing
- Visualization options:
  - Original image
  - Segmentation mask
  - Overlay view with tumor regions highlighted
- Maximum file size limit: 16MB
- Automatic image preprocessing:
  - Resizing to 128x128
  - RGB conversion
  - Pixel normalization

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Deep Learning**: TensorFlow
- **Image Processing**: OpenCV
- **Medical Image Processing**: NiBabel
- **Model**: CapsNet (Capsule Neural Network)

## Prerequisites

- Python 3.x
- GPU support (recommended for faster processing)
- Sufficient RAM for processing medical images

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd liver-segmentation
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Required Dependencies

```
flask==2.0.1
tensorflow==2.8.0
numpy==1.21.0
Pillow==8.3.1
opencv-python==4.5.3.56
nibabel==5.1.0
```

## Project Structure

```
├── app.py                          # Main Flask application
├── capsnet_liver_segmentation.h5   # Pre-trained CapsNet model
├── requirements.txt                # Python dependencies
├── static/                         # Static files
│   ├── script.js                   # Frontend JavaScript
│   ├── style.css                   # CSS styles
│   └── uploads/                    # Upload directory for images
├── templates/                      # HTML templates
│   └── index.html                  # Main webpage template
└── Testing Images/                 # Sample test images
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload an image using the web interface:
   - Drag and drop an image or click to select
   - Supported formats: PNG, JPG, JPEG, NIfTI (.nii, .nii.gz)

4. View the results:
   - Original image
   - Segmentation mask
   - Overlay showing tumor regions

## Model Information

The project uses a pre-trained CapsNet (Capsule Neural Network) model stored in `capsnet_liver_segmentation.h5`. The model:
- Takes input images of size 128x128
- Processes them through capsule layers
- Outputs binary segmentation masks
- Uses dynamic routing between capsules for better feature representation.

## Development Mode

The application runs in debug mode by default, making it suitable for development and testing. For production deployment, make sure to disable debug mode and implement appropriate security measures.

## Sample Images

The repository includes test images in the `Testing Images/` directory that can be used to validate the system's functionality.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
