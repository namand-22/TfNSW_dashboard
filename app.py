from flask import Flask
from main import check_departures

app = Flask(__name__)

@app.route("/")
def index():
    return "<html><p>Hello, World</p></html>"

if __name__ == "__main__":
    check_departures()
    app.run(host="0.0.0.0", port=80)