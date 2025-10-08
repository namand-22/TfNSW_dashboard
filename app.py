from flask import Flask, render_template_string, jsonify
from departures import check_departures


app = Flask(__name__)

# formats the front end for the landing page
@app.route("/")
def index():
    departures = check_departures(station_id=206710) # station_id is for Chatswood station

    platform1, platform2, platform3, platform4 = [], [], [], []
    p1_counter, p2_counter, p3_counter, p4_counter = 0, 0, 0, 0

    # ensures only the next three departures of each platform are displayed
    for departure in departures:
        if departure["platform"] == "Platform 1" and p1_counter < 3:
            platform1.append(departure)
            p1_counter += 1
        elif departure["platform"] == "Platform 2" and p2_counter < 3:
            platform2.append(departure)
            p2_counter += 1
        elif departure["platform"] == "Platform 3" and p3_counter < 3:
            platform3.append(departure)
            p3_counter += 1
        elif departure["platform"] == "Platform 4" and p4_counter < 3:
            platform4.append(departure)
            p4_counter += 1


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

    <h1>
        Chatswood Station departures
    </h1>

    {% for platform_num, platform_data in [(1, platform1), (2, platform2), (3, platform3), (4, platform4)] %}
        <div class="platform">
            <h2>
                Platform {{platform_num}} 
            </h2>
            <table>
                <tr>
                    <th>
                        Train line
                    </th>
                    <th>
                        Destination
                    </th>
                    <th>
                        Departs in
                    </th>
                </tr>
                
                {% for departure in platform_data %}
                    <tr>
                        <td>
                            {{ departure["train_line"] }}
                        </td>
                        <td>
                            {{ departure["destination"] }}
                        </td>
                        <td>
                            {{ departure["departing_in"] }} min
                        </td>
                    </tr>
                {% endfor %}
            </table>
        </div>
    {% endfor %}
    """

    return render_template_string(html, platform1=platform1, platform2=platform2, platform3=platform3, platform4=platform4)

# api for upcoming departures function
@app.route("/api/departures")
def departures():
    departures = check_departures(station_id=2154392) # station_id is for Hills Showground
    return jsonify(departures)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)