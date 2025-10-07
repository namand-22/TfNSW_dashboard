from flask import Flask, render_template_string
from main import check_departures


app = Flask(__name__)

@app.route("/")
def index():
    departures = check_departures()

    html = """
    <h2>Upcoming departures:</h2>
    <ul>
    {% for departure in departures %}
        <li>{{departure["platform"]}}, {{departure["destination"]}}, {{departure["departing_in"]}}</li>
    {% endfor %}
    </ul>
    """

    return render_template_string(html, departures=departures)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)