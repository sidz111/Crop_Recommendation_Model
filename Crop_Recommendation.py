from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load the dataset and train the model once when the application starts
file_path = "Crop_recommendation.csv"
df = pd.read_csv(file_path)

# Split the data into features (X) and labels (y)
X = df[['Nitrogen', 'Phosphorous', 'Potassium', 'Moisture']]
y = df['Crops']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Set feature names for RandomForestClassifier
feature_names = ['Nitrogen', 'Phosphorous', 'Potassium', 'Moisture']
X_train.columns = feature_names

# Initialize the model (Random Forest Classifier in this case)
trained_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
trained_model.fit(X_train, y_train)

def predict_crop(model, value_N, value_P, value_K, value_moisture):
    # Validate input values
    if not (0 <= value_N <= 100) or not (0 <= value_P <= 100) or not (0 <= value_K <= 100) or not (0 <= value_moisture <= 100):
        return {'predicted_crops': "Invalid input. Percentage values must be between 0 and 100."}

    # Use a 2D NumPy array directly for the new input
    new_input = [[value_N, value_P, value_K, value_moisture]]

    predicted_crops = model.predict(new_input)

    return {'predicted_crops': predicted_crops[0]}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    try:
        value_N = int(request.args.get('N'))
        value_P = int(request.args.get('P'))
        value_K = int(request.args.get('K'))
        value_moisture = int(request.args.get('humidity'))
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid integer values for N, P, K, and humidity.'})

    # Predict the crop using the loaded model
    result = predict_crop(trained_model, value_N, value_P, value_K, value_moisture)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
