from flask import Flask, render_template_string
from main import check_departures


app = Flask(__name__)

@app.route("/")
def index():
    departures = check_departures()

    platform1 = []
    platform2 = []

    for departure in departures:
        if departure["platform"] == "Platform 1":
            platform1.append(departure)
        else:
            platform2.append(departure)


    html = """
    <style>
        body { font-family: Poppins, sans-serif; background-color: lightgray; padding: 75px; color: cornflowerblue; }
        h2 { color: cornflowerblue; }
        .platform { background: lightgray; border-radius: 30px; padding: 50px, 50px, 50px, 50px; margin-bottom: 20px; box-shadow: 15px; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; border: none; }
        th, td { border: 1px solid black; padding: 8px; text-align: center; color: black; }
        th { background-color: cornflowerblue; color: white; }
        tr { background-color: white; }
    </style>

    <h1>Upcoming Departures</h1>

    <div class="platform">
        <h2>Platform 1</h2>
        <table>
            <tr><th>Destination</th><th>Departs in</th></tr>
            {% for departure in platform1 %}
                <tr><td>{{ departure["destination"] }}</td><td>{{ departure["departing_in"] }} min</td></tr>
            {% endfor %}
        </table>
    </div>

    <div class="platform">
        <h2>Platform 2</h2>
        <table>
            <tr><th>Destination</th><th>Departs in</th></tr>
            {% for departure in platform2 %}
                <tr><td>{{ departure["destination"] }}</td><td>{{ departure["departing_in"] }} min</td></tr>
            {% endfor %}
        </table>
    </div>
    """




    return render_template_string(html, departures=departures, platform1=platform1, platform2=platform2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)