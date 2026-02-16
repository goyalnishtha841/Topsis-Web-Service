from flask import Flask, render_template, request
import os
import re
from topsis import run_topsis
import smtplib
from email.message import EmailMessage
from flask import send_file
import threading   

app = Flask(__name__)
print("App starting...")

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template("index.html")


def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route('/process', methods=['POST'])
def process():

    try:   

        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        # validations
        if not valid_email(email):
            return "Invalid email format"

        weights_list = weights.split(',')
        impacts_list = impacts.split(',')

        if len(weights_list) != len(impacts_list):
            return "Weights and impacts must be same length"

        for i in impacts_list:
            if i not in ['+', '-']:
                return "Impacts must be + or -"

    
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        output_path = os.path.join(RESULT_FOLDER, "result.csv")

        # run topsis
        run_topsis(input_path, weights, impacts, output_path)

       
        threading.Thread(
            target=send_email,
            args=(email, output_path)
        ).start()

        return send_file(output_path, as_attachment=True)


    except Exception as e:
        print("PROCESS ERROR:", e)
        return f"Error occurred: {str(e)}"




def send_email(receiver, attachment):

    try:  

        sender = os.environ.get("EMAIL_USER")
        password = os.environ.get("EMAIL_PASS")

        if not sender or not password:
            print("Email credentials missing")
            return

        msg = EmailMessage()
        msg["Subject"] = "TOPSIS Result"
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content("Attached is your TOPSIS result.")

        with open(attachment, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename="result.csv"
            )

     
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print("EMAIL ERROR:", e)


if __name__ == "__main__":
    app.run()
