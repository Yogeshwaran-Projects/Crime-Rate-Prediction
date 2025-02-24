from flask import Flask, request, jsonify
import pickle
import math
from flask_cors import CORS

model = pickle.load(open('Model/model.pkl', 'rb'))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi',
    '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur',
    '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai',
    '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
    '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women',
    '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
}

population = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70,
    '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10,
    '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

@app.route('/predict', methods=['POST'])
def predict_result():
    try:
        data = request.form
        city_code = data.get("city")
        crime_code = data.get("crimeType")
        year = int(data.get("year"))

        print("Received request with data:", data)  # Log the incoming request data

        if city_code not in population or crime_code not in crimes_names:
            return jsonify({"error": "Invalid city or crime type"}), 400
        
        pop = population[city_code]
        year_diff = year - 2011
        pop = pop + 0.01 * year_diff * pop  # Assuming 1% growth rate
        
        crime_rate = model.predict([[year, int(city_code), pop, int(crime_code)]])[0]
        cases = math.ceil(crime_rate * pop)
        
        crime_status = "Very Low Crime Area" if crime_rate <= 1 else \
                        "Low Crime Area" if crime_rate <= 5 else \
                        "High Crime Area" if crime_rate <= 15 else "Very High Crime Area"

        response = {
            "city": city_names[city_code],
            "crimeType": crimes_names[crime_code],
            "year": year,
            "crimeRate": crime_rate,
            "crimeStatus": crime_status,
            "predictedCases": cases,
            "population": pop
        }

        print("Sending response:", response)  # Log the response being sent
        return jsonify(response)
    except Exception as e:
        print("Error occurred:", str(e))  # Log any errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
