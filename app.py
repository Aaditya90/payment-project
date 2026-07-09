"""
Secure Payment Gateway Project (Flask + Razorpay)
---------------------------------------------------
Supports: Credit/Debit Card, UPI (Google Pay, PhonePe, Paytm), Netbanking, Wallets
Earning flow: User pays -> money goes to YOUR Razorpay account -> withdraw to bank anytime.

SETUP:
1. pip install flask razorpay python-dotenv
2. Create a free account at https://razorpay.com
3. Get API Key + Secret from Dashboard > Settings > API Keys (use TEST keys first)
4. Create a .env file (see .env.example) with your keys
5. Run: python app.py
"""

import os
import razorpay
import hmac
import hashlib
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route("/")
def home():
    """Product/checkout page"""
    return render_template("index.html", key_id=RAZORPAY_KEY_ID)


@app.route("/create-order", methods=["POST"])
def create_order():
    """
    Step 1: Create an order on Razorpay's server before showing checkout.
    Amount is in paise (₹1 = 100 paise) — always calculate price on the
    SERVER, never trust the amount sent from frontend, to prevent tampering.
    """
    data = request.get_json()
    product_id = data.get("product_id")

    # Server-side price list (never trust client-sent price)
    PRICES = {
        "resume_tool_monthly": 49900,   # ₹499.00
        "resume_tool_onetime": 9900,    # ₹99.00
    }

    amount = PRICES.get(product_id)
    if not amount:
        return jsonify({"error": "Invalid product"}), 400

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1  # auto-capture payment
    })

    return jsonify({
        "order_id": order["id"],
        "amount": amount,
        "currency": "INR",
        "key_id": RAZORPAY_KEY_ID
    })


@app.route("/verify-payment", methods=["POST"])
def verify_payment():
    """
    Step 2: After user pays, Razorpay sends back payment_id, order_id, signature.
    We MUST verify the signature server-side to confirm the payment is genuine
    and wasn't faked by someone calling this endpoint directly.
    """
    data = request.get_json()

    params = {
        "razorpay_order_id": data.get("razorpay_order_id"),
        "razorpay_payment_id": data.get("razorpay_payment_id"),
        "razorpay_signature": data.get("razorpay_signature"),
    }

    try:
        client.utility.verify_payment_signature(params)
        # ✅ Payment genuine — unlock product / send email / activate subscription here
        return jsonify({"status": "success", "message": "Payment verified. Access granted!"})
    except razorpay.errors.SignatureVerificationError:
        # ❌ Payment fake/tampered — do NOT give access
        return jsonify({"status": "failed", "message": "Payment verification failed"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
