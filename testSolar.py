import time
from flask import Flask, render_template, Response

from postgres.postgress import fetchPower, fetchPowerToday

app = Flask(__name__)

@app.route("/stream")
def stream():
    def eventStream():
        while True:
            time.sleep(5)
            print("Power" + str(fetchPowerToday()))
            yield "data:{}\n\n".format(fetchPowerToday())
    return Response(eventStream(), mimetype="text/event-stream")

@app.route("/")
def render_weather():
    temperature = 10
    description = "lala"
    return render_template("testSolar.html",
                               temperature=temperature,
                               description=description)

if __name__ == "__main__":
    app.run()