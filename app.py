from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import base64
import datetime
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'gfitir65e$#4fhgkjkj@!#yuytra!@3'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'solankimohit@01_'
app.config['MYSQL_DB'] = 'mammo_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return "User already exists. Try logging in.", 400

        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                    (name, email, hashed_pw))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_email'] = email
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", "danger")
            return redirect('/login')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, email, registration_date FROM users WHERE id = %s", (session['user_id'],))
    result = cursor.fetchone()
    cursor.close()

    user = {
        'name': result[0],
        'email': result[1],
        'registration_date': result[2].strftime('%Y-%m-%d') if result[2] else ''
    }
    return render_template('dashboard.html', user=user)

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'})

    data = request.get_json()
    current_password = data['current_password']
    new_password = data['new_password']
    confirm_password = data['confirm_password']

    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'New passwords do not match'})

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
    user = cur.fetchone()

    if not user or not check_password_hash(user[0], current_password):
        cur.close()
        return jsonify({'success': False, 'message': 'Current password is incorrect'})

    hashed_new_pw = generate_password_hash(new_password)
    cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_new_pw, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'success': True, 'message': 'Password updated successfully'})

@app.route('/update_email', methods=['POST'])
def update_email():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'})

    new_email = request.json['email']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET email=%s WHERE id=%s", (new_email, session['user_id']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'success': True, 'message': 'Email updated successfully'})

@app.route('/myreports')
def myreports():
    if 'user_id' not in session:
        return redirect('/login')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, filename FROM report WHERE user_id = %s", (session['user_id'],))
    reports = cursor.fetchall()
    cursor.close()

    return render_template('myreports.html', reports=reports)

@app.route('/view_report/<int:report_id>')
def view_report(report_id):
    if 'user_id' not in session:
        return redirect('/login')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT filename, filedata FROM report WHERE id = %s AND user_id = %s", (report_id, session['user_id']))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return "Report not found", 404

    filename, filedata = result
    from flask import send_file
    from io import BytesIO
    return send_file(BytesIO(filedata), download_name=filename, as_attachment=False)

@app.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    if 'user_id' not in session:
        return redirect('/login')

    cursor = mysql.connection.cursor()
    # Delete only if it belongs to the current user
    cursor.execute("DELETE FROM report WHERE id = %s AND user_id = %s", (report_id, session['user_id']))
    mysql.connection.commit()
    cursor.close()

    flash('Report deleted successfully.')
    return redirect('/myreports')

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('reports.html')


@app.route('/upload_report', methods=['POST'])
def upload_report():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    file = request.files.get('reportFile')
    captured_image = request.form.get('capturedImage')

    cursor = mysql.connection.cursor()

    if file and file.filename != '':
        filename = file.filename
        file_data = file.read()
        cursor.execute("INSERT INTO report (user_id, filename, filedata) VALUES (%s, %s, %s)",
                       (user_id, filename, file_data))
        mysql.connection.commit()
        flash("File uploaded successfully!")

    elif captured_image:
        header, encoded = captured_image.split(",", 1)
        binary_data = base64.b64decode(encoded)
        cursor.execute("INSERT INTO report (user_id, filename, filedata) VALUES (%s, %s, %s)",
                       (user_id, 'captured_image.png', binary_data))
        mysql.connection.commit()
        flash("Photo captured and uploaded successfully!")

    else:
        flash("No file or image provided.")

    cursor.close()
    return redirect('/reports')

# @app.route('/symptoms')
# def symptoms():
#     if 'user_id' not in session:
#         return redirect('/login')
#     return render_template('symptoms.html')

# from flask import Flask, render_template, request, jsonify
# import joblib

# app = Flask(_name_)

# Load the trained model once
model = joblib.load('symptom_model.pkl')

@app.route('/symptoms', methods=['GET'])
def symptoms():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('symptoms.html')

@app.route('/symptom-checker', methods=['GET'])
def symptom_checker():
    return render_template('symptoms.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    try:
        feature_names = [
    'uniformity_cell_size',
    'uniformity_cell_shape',
    'marginal_adhesion',
    'single_epithelial_cell_size',
    'bare_nuclei',
    'bland_chromatin',
    'normal_nucleoli',
    'mitoses',
    'clump_thickness'
    ]

        features = [float(request.form.get(f)) for f in feature_names]
        input_data = np.array(features).reshape(1, -1)
        prediction = model.predict(input_data)[0]

        # input_data = np.array(features).reshape(1, -1)
        # prediction = model.predict([input_data])[0]
        result = "Benign" if prediction == 0 else "Malignant"
        return render_template('symptoms.html', prediction=result)
    except Exception as e:
        return render_template('symptoms.html', prediction=f"Error: {e}")

# @app.route('/predict_symptoms', methods=['POST'])
# def predict_symptoms():
#     data = request.get_json()
    
#     try:
#         # Extract values from the incoming JSON
#         clump = int(data['clump'])
#         shape = int(data['shape'])
#         nuclei = int(data['nuclei'])

#         # Make prediction using your ML model
#         input_features = np.array([[clump, shape, nuclei]])
#         prediction = model.predict(input_features)[0]

#         # Convert numeric output to readable label
#         result = "Benign" if prediction == 2 else "Malignant"
#         return jsonify({'prediction': result})
    
#     except Exception as e:
#         print("Prediction Error:", e)
#         return jsonify({'prediction': 'Error in prediction'})
    
# @app.route('/predict_bc', methods=['POST'])
# def predict_bc():
#     if 'user_id' not in session:
#         return jsonify({'error': 'User not logged in'}), 403

#     try:
#         data = request.get_json()
#         features = data.get('features')

#         if not features or len(features) != 9:
#             return jsonify({'error': 'Invalid input: exactly 9 features are required'}), 400

#         features = np.array(features).reshape(1, -1)
#         prediction = model.predict(features)[0]

#         result = 'Malignant' if prediction == 4 else 'Benign'
#         return jsonify({'prediction': result})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @app.route('/predict_symptoms', methods=['POST'])
# def predict_symptoms():
#     data = request.get_json()
#     symptoms_input = data.get('symptoms', '')

#     if not symptoms_input.strip():
#         return jsonify({'error': 'No symptoms provided.'}), 400

#     # Predict
#     prediction = model.predict([symptoms_input])[0]
#     result = "Malignant (High Risk)" if prediction == 1 else "Benign (Low Risk)"
#     return jsonify({'result': result})

# @app.route('/analyze_symptoms', methods=['POST'])
# def analyze_symptoms():
#     if 'user_id' not in session:
#         return jsonify({'prediction': 'Please log in first.'})

#     data = request.get_json()
#     symptoms_text = data.get('symptoms', '')
    
#     from symptom_model import predict_symptom
#     prediction = predict_symptom(symptoms_text)
    
#     return jsonify({'prediction': prediction})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)