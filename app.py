from flask import Flask, render_template, request, redirect, url_for
import requests, os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# ---------- Load Config from .env ----------
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp-relay.brevo.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

# ---------- Brevo API Setup ----------
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER = app.config['MAIL_DEFAULT_SENDER']
BREVO_RECEIVER = os.getenv("MAIL_RECEIVER")

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')

    print(f"📦 New Order:\nName: {name}\nPhone: {phone}\nAddress: {address}")

    # Send email via Brevo API
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        payload = {
            "sender": {"name": "Glowhite Orders", "email": BREVO_SENDER},
            "to": [{"email": BREVO_RECEIVER}],
            "subject": f"New Order from {name}",
            "htmlContent": f"""
                <h2>New Order Received</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Phone:</strong> {phone}</p>
                <p><strong>Address:</strong> {address}</p>
                <p>Check WhatsApp for quick response.</p>
            """
        }
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("✅ Brevo email sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send Brevo email: {e}")

    return redirect(url_for('thankyou', name=name))


@app.route('/thank-you')
def thankyou():
    name = request.args.get('name', 'Customer')
    return render_template('thankyou.html', name=name)


# ---------- Test Email Route ----------
@app.route('/test-email')
def test_email():
    """Send a test email using Brevo API to verify configuration."""
    try:
        url = "https://api.brevo.com/v3/smtp/email"
        payload = {
            "sender": {"name": "Glowhite Test", "email": BREVO_SENDER},
            "to": [{"email": BREVO_RECEIVER}],
            "subject": "Test Email from Glowhite App",
            "htmlContent": """
                <h2>✅ Test Email Successful!</h2>
                <p>This message confirms your Brevo configuration is working.</p>
            """
        }
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return "✅ Test email sent successfully!"
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return f"❌ Failed to send test email: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
