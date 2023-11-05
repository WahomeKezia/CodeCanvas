# app.py 
import os
from flask import (Flask,
          render_template ,
          session,
           redirect,
            request,
             url_for, )

import secrets

app = Flask(__name__)

# Generate a secure random secret key if the FLASK_SECRET_KEY environment variable is not set
secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Set the Flask app's secret key
app.secret_key = secret_key

# initializing PLACEHOLDER_CODE as a constant 
PLACEHOLDER_CODE = "print('Hello, World!')"



@app.route("/", methods=["GET"])
def code():
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    lines = session["code"].split("\n")
    context = {
        "message": "Paste Your Python Code ",
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
         
    }
    return render_template("code_input.html", **context)

@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    return redirect(url_for("code"))

@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))

if __name__ == '__main__':
    app.run(debug=True)
