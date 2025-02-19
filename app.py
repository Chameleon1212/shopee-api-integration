import os
import requests  # ← ここに追加！
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Railway!"

@app.route("/get-ip")  # ← 新しいルートを追加！
def get_ip():
    ip = requests.get("https://api64.ipify.org").text
    return f"My public IP address is: {ip}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # PORT環境変数を取得
    app.run(host="0.0.0.0", port=port)
