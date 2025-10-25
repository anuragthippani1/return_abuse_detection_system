# 🛡️ Return Abuse Detection System

An AI-powered web application for detecting and analyzing return fraud patterns in e-commerce platforms. Built with Flask (Python) and React.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18.3-61dafb)
![MongoDB](https://img.shields.io/badge/MongoDB-Local-green)
![Flask](https://img.shields.io/badge/Flask-2.0-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Functionality

- **AI-Powered Risk Scoring**: Machine learning algorithms analyze return patterns
- **Real-Time Analytics**: Instant insights into return trends and statistics
- **Interactive Dashboard**: Filter and analyze cases by risk level, category, and action
- **Data Visualization**: Charts and graphs for risk distribution
- **Case Management**: Create, read, update, and delete return cases
- **Bulk Upload**: Process CSV/JSON files for batch analysis

### 🎨 UI/UX

- **Modern Design**: Material-UI components with custom gradient themes
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Color-Coded Risk Levels**: Visual indicators for high, medium, and low risk
- **Interactive Filters**: Dynamic filtering with sliders and dropdowns
- **Smooth Animations**: Professional transitions and hover effects

---

## 🛠️ Tech Stack

### Backend

- **Framework**: Flask (Python)
- **Database**: MongoDB
- **Libraries**:
  - pymongo (MongoDB driver)
  - Flask-CORS (Cross-origin requests)
  - pandas (Data processing)
  - scikit-learn (ML models)
  - XGBoost (Risk scoring)
  - spaCy (NLP analysis)

### Frontend

- **Framework**: React 18.3
- **UI Library**: Material-UI (MUI) 5
- **Routing**: React Router 6
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Styling**: Emotion (CSS-in-JS)

---

## 📸 Screenshots

### Home Page

Beautiful landing page with hero section, statistics, and feature highlights.

### Dashboard

Interactive analytics dashboard with real-time data, filters, and visualizations.

---

## 🚀 Installation

### Prerequisites

- Python 3.10+ installed
- Node.js 16+ and npm installed
- MongoDB installed and running locally
- Git installed

### Clone Repository

```bash
git clone https://github.com/yourusername/return-abuse-detection.git
cd return-abuse-detection
```

### Backend Setup

1. Navigate to backend directory:

```bash
cd backend
```

2. Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure MongoDB is running:

```bash
# Check if MongoDB is running
ps aux | grep mongod

# If not running, start it (macOS with Homebrew):
brew services start mongodb-community

# Or manually:
mongod --config /opt/homebrew/etc/mongod.conf
```

### Frontend Setup

1. Navigate to frontend directory:

```bash
cd ../frontend
```

2. Install dependencies:

```bash
npm install
```

---

## 💻 Usage

### Starting the Application

#### 1. Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
python run.py
```

Backend will run on: `http://localhost:5001`

#### 2. Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

Frontend will run on: `http://localhost:3000`

### Accessing the Application

- **Home Page**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard
- **API Documentation**: http://localhost:5001/api
- **Health Check**: http://localhost:5001/health

### Stopping the Application

```bash
# Stop backend
lsof -ti:5001 | xargs kill -9

# Stop frontend
lsof -ti:3000 | xargs kill -9
```

---

## 🔌 API Endpoints

### Base URL: `http://localhost:5001`

| Endpoint                       | Method | Description                        |
| ------------------------------ | ------ | ---------------------------------- |
| `/api`                         | GET    | API documentation & endpoints list |
| `/health`                      | GET    | Health check                       |
| `/api/get-return-cases`        | GET    | Fetch all return cases             |
| `/api/save-return-case`        | POST   | Create new return case             |
| `/api/return-case-statistics`  | GET    | Get analytics statistics           |
| `/api/get-return-case/<id>`    | GET    | Get specific case by ID            |
| `/api/update-return-case/<id>` | PUT    | Update existing case               |
| `/api/delete-return-case/<id>` | DELETE | Delete case                        |
| `/api/upload-data`             | POST   | Bulk upload CSV/JSON               |

### Example API Usage

#### Get All Cases

```bash
curl http://localhost:5001/api/get-return-cases
```

#### Create New Case

```bash
curl -X POST http://localhost:5001/api/save-return-case \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "return_reason": "Product damaged",
    "risk_score": 45,
    "suspicion_score": 50,
    "refund_method_type": "Original Payment",
    "action_taken": "Approved",
    "product_category": "Electronics"
  }'
```

#### Get Statistics

```bash
curl http://localhost:5001/api/return-case-statistics
```

---

## 📁 Project Structure

```
return-abuse-detection/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── config/
│   │   │   ├── config.py        # Configuration
│   │   │   └── mongodb.py       # MongoDB connection
│   │   ├── models/
│   │   │   ├── return_case.py   # Return case model
│   │   │   ├── risk_scoring.py  # ML risk scoring
│   │   │   ├── nlp_analyzer.py  # NLP text analysis
│   │   │   └── visual_inspector.py # Visual inspection
│   │   └── services/
│   │       └── return_case_service.py # Business logic
│   ├── data/                     # Sample data files
│   ├── uploads/                  # File uploads directory
│   ├── requirements.txt          # Python dependencies
│   ├── run.py                    # Application entry point
│   └── venv/                     # Virtual environment
│
├── frontend/
│   ├── public/                   # Static files
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js        # Navigation bar
│   │   │   ├── Home.js          # Home page
│   │   │   ├── Dashboard.js     # Analytics dashboard
│   │   │   └── Footer.js        # Footer component
│   │   ├── App.js               # Main app component
│   │   ├── index.js             # React entry point
│   │   └── App.css              # Global styles
│   ├── package.json             # Node dependencies
│   └── node_modules/            # Node packages
│
├── README.md                     # This file
└── PROJECT_SUMMARY.md           # Detailed project summary
```

---

## 🎨 Customization

### Changing Theme Colors

Edit `frontend/src/App.js`:

```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: "#667eea", // Change this
    },
    secondary: {
      main: "#764ba2", // Change this
    },
  },
});
```

### Modifying Risk Thresholds

Edit `backend/app/models/risk_scoring.py` to adjust risk calculation logic.

### Adding New Features

1. Backend: Add routes in `backend/app/api/routes.py`
2. Frontend: Create components in `frontend/src/components/`
3. Update routing in `frontend/src/App.js`

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Anurag Thippani**

- GitHub: [@anuragthippani1](https://github.com/anuragthippani1)

---

## 🙏 Acknowledgments

- Material-UI for the beautiful component library
- MongoDB for reliable database solution
- React community for excellent documentation
- Flask community for the lightweight framework

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/return-abuse-detection/issues) page
2. Review the `PROJECT_SUMMARY.md` for detailed documentation
3. Check logs:
   - Backend: `backend/backend.log`
   - Frontend: `frontend/frontend.log`

---

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced ML models for better accuracy
- [ ] Real-time notifications for high-risk cases
- [ ] CSV/PDF export functionality
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Comprehensive test coverage
- [ ] API rate limiting

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

---

**Made with ❤️ for fraud detection and e-commerce security**
