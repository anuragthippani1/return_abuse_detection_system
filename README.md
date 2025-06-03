<<<<<<< HEAD
# Amazon Return Abuse Detection System

An AI-powered system for detecting fraudulent return behavior in e-commerce operations.

## Features

- 🧠 Return Risk Scoring Engine

  - Machine learning model to predict return risk scores
  - Features include return frequency, timing, and behavior patterns
  - Built with XGBoost and scikit-learn

- 🗣️ NLP Module for Return Reason Analysis

  - Analyzes customer return justifications
  - Detects suspicious or scripted phrases
  - Uses spaCy and transformers for text analysis

- 🖼️ Visual Return Inspection

  - Compares returned items with original product images
  - Uses computer vision to detect inconsistencies
  - Implements multiple similarity metrics

- 🖥️ Backend API

  - RESTful API built with Flask
  - Endpoints for risk scoring, text analysis, and visual inspection
  - CORS enabled for frontend integration

- 🧑‍💻 Frontend Dashboard
  - Modern React.js interface with Material-UI
  - Real-time risk score visualization
  - Interactive case management system

## Tech Stack

### Backend

- Python 3.8+
- Flask
- scikit-learn
- XGBoost
- spaCy
- TensorFlow/Keras
- OpenCV

### Frontend

- React.js
- TypeScript
- Material-UI
- Axios
- Tailwind CSS

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd amazon-return-detection
```

2. Set up the backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Set up the frontend:

```bash
cd frontend
npm install
```

4. Start the development servers:

Backend:

```bash
cd backend
python app/api/app.py
```

Frontend:

```bash
cd frontend
npm start
```

## API Endpoints

### Risk Scoring

- `POST /api/predict-score`
  - Predicts risk score based on customer behavior data
  - Returns risk score (0-100)

### Text Analysis

- `POST /api/analyze-text`
  - Analyzes return reason text
  - Returns suspicion score and pattern matches

### Visual Inspection

- `POST /api/detect-visual-mismatch`
  - Compares original and returned item images
  - Returns similarity scores and mismatch detection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Amazon for the use case inspiration
- Open source community for the amazing tools and libraries
=======
# return_abuse_detection_system
>>>>>>> bc01a1d4e30c6f764913d11e67cd648fe3dc1b59
