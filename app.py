import os
import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# 各国の Shopee API エンドポイント
SHOPEE_API_ENDPOINTS = {
    "sg": "https://partner.shopeemobile.com/api/v2/",
    "th": "https://partner.shopeemobile.com/api/v2/",
    "my": "https://partner.shopeemobile.com/api/v2/",
    "ph": "https://partner.shopeemobile.com/api/v2/",
    "vn": "https://partner.shopeemobile.com/api/v2/",
    "tw": "https://partner.shopeemobile.com/api/v2/"
}

@app.route("/get_shop_info")
def get_shop_info():
    shop_id = request.args.get("shop_id")
    country_code = request.args.get("country", "sg")  # デフォルトはシンガポール
    
    if not shop_id:
        return jsonify({"error": "error_param", "message": "There is no shop_id in query."}), 400
    
    if country_code not in SHOPEE_API_ENDPOINTS:
        return jsonify({"error": "invalid_country", "message": "Invalid country code."}), 400
    
    # APIエンドポイントの選択
    base_url = SHOPEE_API_ENDPOINTS[country_code]
    url = f"{base_url}shop/get_shop_info"
    
    # 必要なパラメータを追加
    params = {
        "partner_id": os.getenv("SHOPEE_PARTNER_ID"),
        "shop_id": shop_id,
        "timestamp": int(time.time())
    }
    
    response = requests.get(url, params=params)
    
    return response.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
