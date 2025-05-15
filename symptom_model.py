# import joblib

# # Load the pipeline (vectorizer + model)
# pipeline = joblib.load('ml_model/symptom_pipeline.pkl')

# def predict_symptom(text):
#     if not text.strip():
#         return "No symptoms provided."

#     prediction = int(model.predict(features)[0])
    
#     if prediction == 1:
#         return "High risk of breast cancer. Please consult a specialist."
#     else:
#         return "Low risk detected. Continue regular monitoring."