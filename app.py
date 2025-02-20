import os
import time
import hmac
import hashlib
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

def generate_sign(path, partner_id, timestamp, partner_key):
    """Shopee APIの署名を生成"""
    base_string = f"{partner_id}{path}{timestamp}"
    return hmac.new(
        partner_key.encode('utf-8'),
        base_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

@app.route("/get_shop_info", methods=["GET"])
def get_shop_info():
    shop_id = request.args.get("shop_id")
    country = request.args.get("country")

    # ✅ 環境変数から API 認証情報を取得
    partner_id = os.getenv("SHOPEE_PARTNER_ID")
    partner_key = os.getenv("SHOPEE_PARTNER_KEY")

    # ✅ 環境変数の値をログに出力（デバッグ用）
    print(f"Loaded partner_id from env: {partner_id}")
    print(f"Loaded partner_key from env: {partner_key}")

    if not shop_id or not country or not partner_id or not partner_key:
        return jsonify({"error": "error_param", "message": "Missing required parameters"}), 400

    # ✅ 指定された国のエンドポイントを取得
    api_url = SHOPEE_API_ENDPOINTS.get(country.lower())
    api_path = "/api/v2/shop/get_shop_info"

    if not api_url:
        return jsonify({"error": "invalid_country", "message": "Unsupported country code"}), 400

    # ✅ 署名を生成
    timestamp = int(time.time())
    sign = generate_sign(api_path, partner_id, timestamp, partner_key)

    # APIリクエスト用のパラメータ
    params = {
        "partner_id": int(partner_id),
        "shop_id": int(shop_id),
        "timestamp": timestamp,
        "sign": sign
    }

    # ✅ APIリクエスト時の partner_id をログに出力（デバッグ用）
    print(f"Sending API request with partner_id: {params['partner_id']}")

    # Shopee APIへリクエスト
    response = requests.get(api_url, params=params)

    return response.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
