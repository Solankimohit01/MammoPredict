# MammoPredict - Breast Cancer Prediction Web App

MammoPredict is a full-stack web application that helps users detect early signs of breast cancer using machine learning. It provides symptom-based prediction, report upload analysis, and personal user dashboards with reports and recommendations.

---

## 🔍 Features

### 1. *User Management*
- User Registration with password hashing
- Secure Login with session handling
- User Dashboard with personalized data
- Account Settings: Change Email, Password

### 2. *Breast Cancer Prediction*
- Uses a trained machine learning model (RandomForestClassifier)
- Model trained on [Breast Cancer Dataset](https://www.kaggle.com/datasets/merishnasuwal/breast-cancer-prediction-dataset)
- Input via:
  - Symptom-based form
  - Uploaded diagnostic report (Planned)

### 3. *Symptom Checker*
- Intuitive form with dropdowns for symptoms like:
  - Lump in breast
  - Breast pain
  - Skin dimpling
  - Nipple discharge
  - Swelling
- Instant prediction result (Malignant / Benign) using ML model
- User-friendly layout and no manual "Analyze" button required

### 4. *Dashboard*
- Displays Prediction History
- Access to Reports
- Settings & Help section

### 5. *Tech Stack*
- *Frontend*: HTML, CSS, JavaScript (Fetch API)
- *Backend*: Python, Flask
- *ML Libraries*: pandas, scikit-learn, joblib
- *Database*: MySQL
- *Session Handling*: Flask-Session

---

## 📂 Project Structure

MammoPredict/ ├── static/ │   └── style.css ├── templates/ │   ├── index.html │   ├── login.html │   ├── register.html │   ├── dashboard.html │   ├── symptom_checker.html ├── app.py ├── train_model.py ├── model/ │   └── breast_cancer_model.pkl ├── data/ │   └── data.csv ├── requirements.txt └── README.md

---

## ⚙ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MammoPredict.git
   cd MammoPredict

2. Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install required packages:

pip install -r requirements.txt


4. Run the app:

python app.py




---

📊 Dataset

Source: Kaggle - Breast Cancer Prediction Dataset

Format: data.csv

Contains features such as:

Age

Tumor size

Texture, Area, Smoothness

Diagnosis label (Malignant / Benign)




---

🔐 Security Notes

Passwords are securely hashed

User sessions are managed securely using Flask-Session

Input data is validated on both client and server sides



---

📌 Next Steps

Add Report Upload & Parsing functionality

Admin panel for data analysis

Improve mobile responsiveness

Deploy to a cloud platform (e.g., Render, Heroku, or AWS)



---

🧑‍💻 Developed By

Mohit Solanki – MCA Student & Developer

Tools used: VS Code, MySQL, Python, Flask



---

License

This project is for educational purposes only. All rights to the dataset belong to the original authors on Kaggle.

---
