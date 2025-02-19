import os
import time
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Shopee APIのエンドポイント（各国対応）
SHOPEE_API_ENDPOINTS = {
    "sg": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info",
    "th": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info",
    "my": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info",
    "ph": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info",
    "vn": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info",
    "tw": "https://partner.shopeemobile.com/api/v2/shop/get_shop_info"
}

@app.route("/get_shop_info", methods=["GET"])
def get_shop_info():
    shop_id = request.args.get("shop_id")
    country = request.args.get("country")

    # ✅ 環境変数から partner_id を取得
    partner_id = os.getenv("SHOPEE_PARTNER_ID")

    if not shop_id or not country or not partner_id:
        return jsonify({"error": "error_param", "message": "Missing required parameters"}), 400

    # ✅ 指定された国のエンドポイントを取得
    api_url = SHOPEE_API_ENDPOINTS.get(country.lower())

    if not api_url:
        return jsonify({"error": "invalid_country", "message": "Unsupported country code"}), 400

    # APIリクエスト用のパラメータ
    params = {
        "partner_id": int(partner_id),
        "shop_id": int(shop_id),
        "timestamp": int(time.time())
    }

    # Shopee APIへリクエスト
    response = requests.get(api_url, params=params)
    
    return response.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
