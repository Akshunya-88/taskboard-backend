import requests

api_key = "AIzaSyAtZ8xXxr8_UNMp41pNhL6RfBKWTHhstk4"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    data = response.json()
    
    if 'models' in data:
        print("Available Models:")
        for model in data['models']:
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"- {model['name']}")
    else:
        print(f"Error: {data}")

except Exception as e:
    print(f"Connection Error: {e}")
