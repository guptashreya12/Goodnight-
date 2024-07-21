from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load models
disorder_model = joblib.load('models/sleep_disorder_model.pkl')
quality_model = joblib.load('models/sleep_quality_duration_model.pkl')
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_page')
def predict_page():
    return render_template('index.html')

@app.route('/sleep_blogs')
def sleep_blogs_page():
    return render_template('sleep_blogs.html')





@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    gender_map = {'male': 1, 'female': 0}
    occupation_map = {'Accountant': 0, 'Doctor': 1, 'Engineer': 2, 'Lawyer': 3, 'Manager': 4, 'Nurse': 5, 'Sales Representative': 6, 'Salesperson': 7, 'Scientist': 8, 'Software Engineer': 9, 'Teacher': 10}
    bmi_map = {'Normal': 0, 'Obese': 2, 'Overweight': 3, 'Normal Weight': 4}

    features = [
    int(data.get('age')),
    gender_map[data.get('gender')],
    occupation_map[data.get('occupation')],
    int(data.get('physical_activity_level')),
    int(data.get('stress_levels')),
    bmi_map[data.get('bmi')],
    float(data.get('blood_pressure_upper')),
    float(data.get('blood_pressure_lower')),
    int(data.get('heart_rate')),
    int(data.get('daily_steps')),
    int(data.get('sleep_duration')),
    int(data.get('quality_of_sleep'))
]

    # Add feature names
    feature_names = [
        'Age', 'Gender', 'Occupation', 'Sleep Duration', 'Quality of Sleep',
        'Physical Activity Level', 'Stress Level', 'BMI Category',
        'Blood Pressure Upper', 'Blood Pressure Lower', 'Heart Rate', 'Daily Steps'
    ]

    feature_dict = {name: value for name, value in zip(feature_names, features)}

    disorder_prediction = disorder_model.predict([features])[0]
    quality_prediction = quality_model.predict([features])[0]

    return jsonify({
        'disorder_prediction': int(disorder_prediction),
        'quality_prediction': float(quality_prediction)
    })

if __name__ == '__main__':
    app.run(debug=True)













# from flask import Flask, request, jsonify, render_template
# import joblib
# import numpy as np

# app = Flask(__name__)

# # Load models
# disorder_model = joblib.load('models/sleep_disorder_model.pkl')
# quality_model = joblib.load('models/sleep_quality_duration_model.pkl')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()

#     gender_map = {'male': 1, 'female': 0}
#     occupation_map = {'Accountant': 0, 'Doctor': 1, 'Engineer': 2, 'Lawyer': 3, 'Manager': 4, 'Nurse': 5, 'Sales Representative': 6, 'Salesperson': 7, 'Scientist': 8, 'Software Engineer': 9, 'Teacher': 10}
#     bmi_map = {'Normal': 0, 'Obese': 2, 'Overweight': 3, 'Normal Weight': 4}

#     try:
#         features = [
#             int(data.get('age')),
#             gender_map[data.get('gender')],
#             occupation_map[data.get('occupation')],
#             float(data.get('sleep_duration')),
#             int(data.get('quality_of_sleep')),
#             int(data.get('physical_activity_level')),
#             int(data.get('stress_levels')),
#             bmi_map[data.get('bmi')],
#             float(data.get('blood_pressure_upper')),
#             float(data.get('blood_pressure_lower')),
#             int(data.get('heart_rate')),
#             int(data.get('daily_steps')),
#         ]
        
#         disorder_prediction = disorder_model.predict([features])[0]
#         quality_prediction = quality_model.predict([features])[0]

#         return jsonify({
#             'disorder_prediction': int(disorder_prediction),
#             'quality_prediction': float(quality_prediction)
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)
