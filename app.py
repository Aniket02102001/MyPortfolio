from flask import Flask, render_template, request, redirect
from email.message import EmailMessage
import smtplib
import os

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- SEND EMAIL ----------------
@app.route("/sendemail/", methods=["POST"])
def sendemail():

    # Get form data safely
    name = request.form.get("name")
    subject = request.form.get("Subject")
    email = request.form.get("_replyto")
    message = request.form.get("message")

    # Get environment variables from Render
    yourEmail = os.getenv("EMAIL_USER")
    yourPassword = os.getenv("EMAIL_PASSWORD")

    # Check if credentials exist
    if not yourEmail or not yourPassword:
        print("❌ Missing EMAIL_USER or EMAIL_PASSWORD in environment variables")
        return redirect("/")

    try:
        # Create email message
        msg = EmailMessage()
        msg.set_content(
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Message: {message}"
        )

        msg["Subject"] = subject
        msg["From"] = yourEmail
        msg["To"] = yourEmail   # send to yourself

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()

        # Login
        server.login(yourEmail, yourPassword)

        # Send email
        server.send_message(msg)

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("❌ Failed to send email:", e)

    finally:
        try:
            server.quit()
        except:
            pass

    return redirect("/")


# ---------------- RUN APP (IMPORTANT FOR RENDER) ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))