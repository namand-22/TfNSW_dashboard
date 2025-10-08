from flask import Flask, render_template_string, jsonify
from departures import check_departures
from collections import defaultdict

app = Flask(__name__)

# formats the front end for the landing page
@app.route("/")
def index():
    departures = check_departures(station_id=206710) # station_id is for Chatswood station

    # Group departures by line and side
    platform_side = { "1": "right", "2": "right", "3": "left", "4": "left" }
    lines = defaultdict(lambda: {"left": [], "right": []})
    for dep in departures:
        platform_number = dep["platform"].split()[-1]
        side = platform_side.get(platform_number, "right")
        lines[dep["train_line"]][side].append(dep)

    # keep next 3 departures per side per line
    for line, sides in lines.items():
        sides["left"], sides["right"] = sides["left"][:3], sides["right"][:3]

    html = """
    <style>
        .half { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; border-right: 2px solid black }
        body { font-family: sans-serif; margin: 0; display: flex; flex-direction: column }
        .line-row { display: flex; flex: 1; border-bottom: 2px solid black }
        .main-time { font-size: 8vh; font-weight: bold; margin: 0.5vh }
        .line-destination { font-size: 2vh; margin-bottom: 0.5vh }
        .line-title { font-size: 2.5vh; margin-bottom: 0.5vh }
        .platform { font-size: 1.5vh; margin-top: 0.5vh }
        .arrow { font-size: 4vh; margin-bottom: 0.5vh }
        .line-row:last-child { border-bottom: none }
        .half:last-child { border: none }
        .other-times { font-size: 2vh }
    </style>

    {% for line, sides in lines.items() %}
        <div class="line-row">
            {% for side in ["left", "right"] %}
                {% set departures = sides[side] %}
                <div class="half">
                    {% if departures %}
                        <div class="arrow">{{ "←" if side == "left" else "→" }}</div>
                        <div class="line-title">{{ line }}</div>
                        <div class="line-destination">{{ departures[0].destination }}</div>
                        <div class="main-time">{{ departures[0].departing_in }} min</div>
                        <div class="other-times">
                            {% for dep in departures[1:] %}
                                {{ dep.departing_in }} min{{ ", " if not loop.last else "" }}
                            {% endfor %}
                        </div>
                        <div class="platform">{{ departures[0].platform }}</div>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
    {% endfor %}
    """

    return render_template_string(html, lines=lines)

# api for upcoming departures function
@app.route("/api/departures")
def departures():
    departures = check_departures(station_id=2154392) # station_id is for Hills Showground
    return jsonify(departures)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)