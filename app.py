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

    name = request.form.get("name", "")
    subject = request.form.get("Subject", "Portfolio Contact Form")
    email = request.form.get("_replyto", "")
    message = request.form.get("message", "")

    # For local testing in VS Code
    yourEmail = os.getenv("EMAIL_USER")
    yourPassword = os.getenv("EMAIL_PASSWORD")
   

    if not yourEmail or not yourPassword:
        return "Missing email credentials", 500

    server = None

    try:
        # Create email
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = yourEmail
        msg["To"] = yourEmail
        msg["Reply-To"] = email

        msg.set_content(
            f"""
Name: {name}
Email: {email}

Message:
{message}
"""
        )

        print("Connecting to Gmail SMTP...")

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()

        print("Logging in...")

        server.login(yourEmail, yourPassword)

        print("Sending email...")

        server.send_message(msg)

        print("✅ Email sent successfully!")

        return redirect("/")

    except Exception as e:
        print("❌ Error:", str(e))
        return f"Error sending email: {str(e)}", 500

    finally:
        if server:
            try:
                server.quit()
            except:
                pass


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)