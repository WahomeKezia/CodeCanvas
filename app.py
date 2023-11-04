from flask import Flask

app = Flask(__name__)

# Enable debug mode
app.debug = True

@app.route("/", methods=["GET"])
def code():
    return " Hello , Flask"

if __name__ == '__main__':
    app.run()
