from flask import Flask, render_template, request, redirect
from email.message import EmailMessage
import smtplib
import ssl
import os

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- SEND EMAIL ----------------
@app.route("/sendemail/", methods=["POST"])
def sendemail():

    name = request.form.get("name", "").strip()
    subject = request.form.get("Subject", "Portfolio Contact Form").strip()
    sender_email = request.form.get("_replyto", "").strip()
    message = request.form.get("message", "").strip()

    # Render Environment Variables
    yourEmail = os.getenv("EMAIL_USER")
    yourPassword = os.getenv("EMAIL_PASSWORD")

    print("EMAIL_USER:", yourEmail)
    print("EMAIL_PASSWORD exists:", bool(yourPassword))

    if not yourEmail or not yourPassword:
        return "Missing email credentials. Check Render Environment Variables.", 500

    try:
        # Create Email
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = yourEmail
        msg["To"] = yourEmail
        msg["Reply-To"] = sender_email

        msg.set_content(
            f"""
New Portfolio Contact Form Submission

Name: {name}
Email: {sender_email}

Message:
{message}
"""
        )

        print("Connecting to Gmail SMTP...")

        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

            print("Logging into Gmail...")

            server.login(yourEmail, yourPassword)

            print("Sending email...")

            server.send_message(msg)

        print("✅ Email sent successfully!")

        return redirect("/")

    except Exception as e:
        print("❌ Error:", str(e))
        return f"Error sending email: {str(e)}", 500


# ---------------- TEST SMTP ----------------
@app.route("/smtp-test")
def smtp_test():
    try:
        import socket

        socket.create_connection(("smtp.gmail.com", 587), timeout=10)

        return "SMTP connection successful"

    except Exception as e:
        return f"SMTP failed: {str(e)}"


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)