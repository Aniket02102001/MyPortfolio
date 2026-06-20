from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sendemail/", methods=["POST"])
def sendemail():

    name = request.form.get("name", "").strip()
    subject = request.form.get("Subject", "Portfolio Contact Form").strip()
    sender_email = request.form.get("_replyto", "").strip()
    message = request.form.get("message", "").strip()

    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    if not RESEND_API_KEY:
        return "RESEND_API_KEY not found", 500

    try:

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "Portfolio <onboarding@resend.dev>",
                "to": ["aniketsahu02102001@gmail.com"],   # replace with your email
                "subject": subject,
                "reply_to": sender_email,
                "html": f"""
                <h2>New Portfolio Contact</h2>

                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {sender_email}</p>

                <p><strong>Message:</strong></p>
                <p>{message}</p>
                """
            }
        )

        print(response.status_code)
        print(response.text)

        if response.status_code in [200, 201]:
            return redirect("/")

        return f"Resend Error: {response.text}", 500

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)