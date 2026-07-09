# Secure Payment Gateway Project (Card + UPI)

Yeh project Razorpay use karke ek secure checkout banata hai jisme log **Card, UPI (Google Pay, PhonePe, Paytm), Netbanking** — sab se pay kar sakte hain. Payment aapke Razorpay account mein aati hai, wahan se aap bank mein withdraw kar sakte ho.

## Files
- `app.py` — Flask backend (order create + payment verify)
- `templates/index.html` — Checkout page (frontend)
- `.env.example` — API keys ka template
- `requirements.txt` — Python dependencies

## Setup (5 steps)

### 1. Razorpay account banao (free)
https://razorpay.com pe signup karo. Business verification baad mein bhi kar sakte ho — pehle **Test Mode** mein kaam karo.

### 2. API Keys lo
Dashboard > Settings > API Keys > Generate Test Key
Aapko milega:
- Key ID (`rzp_test_...`)
- Key Secret

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. .env file banao
`.env.example` ko copy karke `.env` naam do, aur apni keys daal do:
```
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_secret_here
```

### 5. Run karo
```bash
python app.py
```
Browser mein kholo: `http://localhost:5000`

Test payment karne ke liye Razorpay ke **test card** use karo:
- Card number: `4111 1111 1111 1111`
- Koi bhi future expiry date, koi bhi CVV

## Live/Production pe jaane ke liye (real earning)
1. Razorpay dashboard mein KYC/business documents submit karo (PAN, bank account)
2. Approval ke baad **Live Keys** milengi (`rzp_live_...`)
3. `.env` mein test keys ko live keys se replace karo
4. App ko hosting pe deploy karo (Render/Railway free tier chal jayega)
5. Domain pe HTTPS zaroor ho (Render/Railway automatically deta hai)

## Security jo already handle hai isme
- Price hamesha server pe decide hoti hai, frontend se nahi (tampering se bachav)
- Payment signature verify hoti hai backend pe — fake payment accept nahi hoga
- Card details kabhi bhi aapke server pe store nahi hote — Razorpay khud PCI-DSS compliant hai

## Earning kaise milegi
- Har successful payment Razorpay mein aata hai (transaction fee ~2% katkar)
- Razorpay se bank account mein T+2 din mein auto-settle ho jata hai
