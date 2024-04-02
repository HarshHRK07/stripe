from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/token/lista', methods=['GET'])
def generate_token_with_cvc():
    cc_info = request.args.get('cc')
    pk = request.args.get('pk')

    if cc_info and pk:
        card_data = cc_info.split("|")

        payload = {
            "card[number]": card_data[0],
            "card[exp_month]": card_data[1],
            "card[exp_year]": card_data[2],
            "card[cvc]": card_data[3],
            "payment_user_agent": "stripe.js/35cbb2677a; stripe-js-v3/35cbb2677a; card-element",
            "key": pk,
            "pasted_fields": "number"
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'sec-ch-ua': "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            'dnt': "1",
            'sec-ch-ua-mobile': "?1",
            'sec-ch-ua-platform': "\"Android\"",
            'origin': "https://js.stripe.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://js.stripe.com/"
        }

        response = requests.post("https://api.stripe.com/v1/tokens", data=payload, headers=headers)
        token = response.json().get("id", "")

        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Missing 'cc' or 'pk' parameter"}), 400

@app.route('/tokens/lista', methods=['GET'])
def generate_token_ignore_cvc():
    cc_info = request.args.get('cc')
    pk = request.args.get('pk')

    if cc_info and pk:
        # Extracting card information excluding CVC
        cc_data = cc_info.split("|")

        payload = {
            "card[number]": cc_data[0],
            "card[exp_month]": cc_data[1],
            "card[exp_year]": cc_data[2],
            "payment_user_agent": "stripe.js/35cbb2677a; stripe-js-v3/35cbb2677a; card-element",
            "key": pk,
            "pasted_fields": "number"
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'sec-ch-ua': "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            'dnt': "1",
            'sec-ch-ua-mobile': "?1",
            'sec-ch-ua-platform': "\"Android\"",
            'origin': "https://js.stripe.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://js.stripe.com/"
        }

        response = requests.post("https://api.stripe.com/v1/tokens", data=payload, headers=headers)
        token = response.json().get("id", "")

        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Missing 'cc' or 'pk' parameter"}), 400

if __name__ == '__main__':
    app.run(debug=True)
    