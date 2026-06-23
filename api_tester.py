import requests
import json

api_url = "https://nyz5y3cp2d.execute-api.af-south-1.amazonaws.com/submit-report"


# The data we are submitting to the API
data = {
    "location": "Cape Town, Main Road",
    "issueType": "water_leak",
    "urgency": "high"
}

response = requests.post(api_url, json=data)

print(f"Status code: {response.status_code}")
print(f"Response from Lambda: {response.text}")
