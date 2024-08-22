import requests
from datetime import datetime

GENDER = "Male"
WEIGHT_KG = 63
HEIGHT_CM = 173
AGE = 18

APP_ID = "3ce81c2b"
API_KEY = "1fcf3ba5463eb86e2b43dc7a1e0539a0"
SHEETY_BEARER_TOKEN = "idncneijm39j9m2"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/820b15e25a785b92e62cf28922b5b8f7/workoutTracking/workouts"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
}

query = input("Tell me about today's workout: ")

parameters = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
else:
    try:
        result = response.json()
        today_date = datetime.now().strftime("%d/%m/%Y")
        now_time = datetime.now().strftime("%X")

        for exercise in result["exercises"]:
            sheet_inputs = {
                "workout": {
                    "date": today_date,
                    "time": now_time,
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"]
                }
            }

            sheet_headers = {
                "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}",
                "Content-Type": "application/json",
            }

            sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=sheet_headers)

            if sheet_response.status_code != 200:
                print(f"Error posting to sheet: {sheet_response.status_code}")
                print(sheet_response.text)
            else:
                print(sheet_response.text)
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON response.")
        print(response.text)
