from flask import Flask, render_template, request, url_for, redirect 
from email.mime.text import MIMEText 
import smtplib 
from email.message import EmailMessage 
app = Flask(__name__) 

@app.route("/") 
def index(): 
	return render_template("index.html") 

@app.route("/sendemail/", methods=['POST'])
def sendemail():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']

        # Set your credentials
        yourEmail = "suraj@geeksforgeeks.org"
        yourPassword = "########"

        # Logging in to our email account
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(yourEmail, yourPassword)

            # Sender's and Receiver's email address
            msg = EmailMessage()
            msg.set_content(f"First Name : {name}\nEmail : {email}\nSubject : {subject}\nMessage : {message}")
            msg['To'] = yourEmail  # Send the email to yourself
            msg['From'] = yourEmail
            msg['Subject'] = subject

            # Send the message via our own SMTP server.
            server.send_message(msg)
            print("Email Sent")
            server.quit()
        except Exception as e:
            print(f"Failed to Send Email: {e}")
            
    return redirect('/')

if __name__ == "__main__": 
	app.run(debug=True)
