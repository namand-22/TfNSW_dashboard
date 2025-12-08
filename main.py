from flask import Flask, render_template_string, request, jsonify
from departures import check_departures
from collections import defaultdict

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    station_id = request.form.get("station_id", "206710")  # Default to Chatswood

    result = check_departures(station_id=station_id)
    if isinstance(result, dict) and "error" in result:
        error_message = result["error"]
        return render_template_string("""
        <h2 style='font-family:sans-serif; padding:2em;'>{{ error_message }}</h2>
        <form method="POST" style='padding:2em;'>
            <label for="station_id">Enter Station ID:</label>
            <input type="text" id="station_id" name="station_id" value="{{ station_id }}">
            <button type="submit">Submit</button>
        </form>
        """, error_message=error_message, station_id=station_id)

    departures = result

    platform_side = {"1": "right", "2": "right", "3": "left", "4": "left"}
    lines = defaultdict(lambda: {"left": [], "right": []})
    for dep in departures:
        platform_number = dep["platform"].split()[-1]
        side = platform_side.get(platform_number, "right")
        lines[dep["train_line"]][side].append(dep)

    for line, sides in lines.items():
        sides["left"], sides["right"] = sides["left"][:4], sides["right"][:4]

    html = """
    <head>
        <meta http-equiv="Refresh" content="60" />
    </head>
    <style>
        .half { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; border-right: 2px solid }
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
        .form-container { padding: 1em; border-bottom: 2px solid black; }
    </style>

    <div class="form-container">
        <form method="POST">
            <label for="station_id">Enter Station ID:</label>
            <input type="text" id="station_id" name="station_id" value="{{ station_id }}">
            <button type="submit">Submit</button>
        </form>
    </div>

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

    return render_template_string(html, lines=lines, station_id=station_id)

@app.route("/api/departures")
def departures():
    station_id = request.args.get("station_id", "2154392")
    result = check_departures(station_id=station_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)