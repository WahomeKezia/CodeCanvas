# app.py 
import os
from flask import (Flask,
          render_template ,
          session,
           redirect,
            request,
             url_for,)
# adding base64 for images
import base64
from utils import take_screenshot_from_url
import secrets
# importing pygments 
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
# to support other languages 
from pygments.lexers import get_lexer_by_name


app = Flask(__name__)

# # Generate a secure random secret key if the FLASK_SECRET_KEY environment variable is not set
# secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
secret_key = "anyrandomKey"

# Set the Flask app's secret key
app.secret_key = secret_key

# initializing PLACEHOLDER_CODE as a constant 
PLACEHOLDER_CODE = "print('Hello, World!')"
DEFAULT_STYLE = "lightbulb"
NO_CODE_FALLBACK = "# No Code Entered"


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

# adding save code view
@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("code"))

# resets the session to default
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))

# adding the add style view to pasted code 
@app.route("/style", methods=["GET"])
def style():
     # Seting a default code if "code" is not in the session
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE 

    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE
         # Get the "code" from the session or use the placeholder 
    selected_language = request.args.get("language", "python")  # Default to Python if not specified

    # Get the "code" from the session or use the placeholder
    lexer = get_lexer_by_name(selected_language)
    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select Your Style 🎨",
        "all_styles": list(get_all_styles()),
        "style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(
            session["code"],lexer, formatter ),
        "selected_language": selected_language,
        
    }
    return render_template("style_selection.html", **context)

# saving style choosen 
@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    selected_language = request.form.get("language", "python")  # Default to Python if not specified
    return redirect(url_for("style" ,language=selected_language))

# creating an image and downloading it view
@app.route("/image", methods=["GET"])
def image():
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style")
    image_bytes = take_screenshot_from_url(target_url, session_data)
    context = {
        "message": "Done! 🎉",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
    }
    return render_template("image.html", **context)

if __name__ == '__main__':
    app.run(debug=True)
