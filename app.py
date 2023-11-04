# from flask import Flask

# app = Flask(__name__)

# # Enable debug mode
# app.debug = True

# @app.route("/", methods=["GET"])
# def code():
#     return "Hello Flask app"

# if __name__ == '__main__':
#     # Run the app with the debugger enabled
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def code_input():
    return render_template("code_input.html")

if __name__ == '__main__':
    app.run(debug=True)
