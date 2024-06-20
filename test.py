from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.theaccessbox.com/api/v1/UserAccount/createCharge"
ZIP_CODE = "10001"  # Constant zip code
# Your predefined Bearer token for the external API request
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS50aGVhY2Nlc3Nib3guY29tL2FwaS92MS9sb2dpbiIsImlhdCI6MTcxODg2NjUyMCwibmJmIjoxNzE4ODY2NTIwLCJqdGkiOiJrWE83ZWJxMnhwMzQ1QWhYIiwic3ViIjoiNzEiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.sARiJkMVJDq4PMYKPFH9nbSxfBJ5lJMLXRzbBByfiFQ"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Content-Type': "application/json",
  'origin': "https://theaccessbox.com",
  'referer': "https://theaccessbox.com/",
  'authorization': f"Bearer {BEARER_TOKEN}"
}

@app.route('/HRK', methods=['GET'])
def process_request():
    api_key = request.args.get('API')
    cc_info = request.args.get('CC')
    
    # Validate the provided API key
    if api_key != "SK_LIVE_LULLI_LELO":
        return jsonify({"error": "Invalid API key"}), 403
    
    if not cc_info:
        return jsonify({"error": "Missing CC information"}), 400
    
    try:
        # Split the card information
        card_number, expiry_month, expiry_year, cvv = cc_info.split("|")
    except ValueError:
        return jsonify({"error": "Invalid CC format. Expected format: number|MM|YYYY|CVV"}), 400
    
    # Construct payload
    payload = {
        "number": card_number,
        "expiry_date": f"{expiry_month}/{expiry_year}",
        "cvv": cvv,
        "zip_code": ZIP_CODE
    }
    
    # Send POST request
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # Log response to a file
    with open('resp.txt', 'a') as resp_file:
        resp_file.write(f"Card Information Used: {cc_info}\n")
        resp_file.write(f"Response: {response.text}\n")
        resp_file.write("-" * 50 + "\n")  # Separator
    
    return jsonify({
        "card_info": cc_info,
        "response": response.json()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
