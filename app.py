import base64
import ast
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import secrets
import string

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles
from checkcorrectsyntax import check_syntax
from utils import take_screenshot_from_url

# You creating an instance of the Flask application

app = Flask(__name__)
# a function to  generate a secure random secret key for sessions 
def generate_secret_key():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(32))

app.secret_key = generate_secret_key()
# Default Values and Constants
PLACEHOLDER_CODE = "print('Hello, World!')"
DEFAULT_STYLE = "monokai"
NO_CODE_FALLBACK = "# No Code Entered"

# Route Definitions
@app.route("/", methods=["GET"])
def code():
    if session.get("code") is None:
        session["code"] = PLACEHOLDER_CODE
    lines = session["code"].split("\n")
    context = {
        "message": "Paste Your Code here!",
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    return render_template("code_input.html", **context)


@app.route("/save_code", methods=["POST"])
def save_code():
    user_code = request.form.get("code") or NO_CODE_FALLBACK
    
# Check syntax
    is_syntax_correct, error_message = check_syntax(user_code)

    if is_syntax_correct:
        session["code"] = user_code
        return redirect(url_for("code"))
    else:
        context = {
            "message": "Syntax Error",
            "error_message": error_message,
            "code": user_code,
        }
        return render_template("code_input.html", **context)



@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = PLACEHOLDER_CODE
    return redirect(url_for("code"))


@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE
    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select Your Style 🎨",
        "all_styles": list(get_all_styles()),
        "style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(
            session["code"], Python3Lexer(), formatter
        ),
    }
    return render_template("style_selection.html", **context)


@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code") or NO_CODE_FALLBACK
    return redirect(url_for("style"))


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

# check if code pasted follows python syntax 


