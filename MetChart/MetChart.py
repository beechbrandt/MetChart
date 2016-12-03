from flask import Flask, request, Response, render_template, redirect, url_for
from MetData import MetData

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

import logging

#logging.basicConfig(setLevel=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

met_data = None
app = Flask(__name__)

class HelloWorld(object):
    def index(self):
        return "Hello World"
    index.exposed = True

@app.route("/plots", methods=['GET'])
def plot_var(**kwargs):

    names = request.args.get('cities', "London").split(",")
    var = request.args.get('var', "tmax")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.title("{}".format(var))

    for name in names:
        logger.debug("Plotting {}".format(name))
        x_data, y_data = met_data.get_timeseries(name=name, var=var)
        ax.plot(x_data, y_data, label=name)

    plt.xlabel("Date")
    if var in [ 'tmax', 'tmin', 'tavg' ]: 
        plt.ylabel("Temperature [C]")
    plt.legend()

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    plt.xticks(rotation='vertical')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return Response(buf.getvalue(), mimetype="image/png")

@app.route('/')
def front_page(**kwargs):

    cities = request.args.get('cities')
    if (cities == None):
        return redirect(url_for('front_page', cities=
                                "London,Paris,Birmingham,Amberg,Bitz"))
    return render_template("layout.html", cities=request.args.get('cities'))


def main():
    global met_data
    met_data = MetData()
    app.run(host="0.0.0.0", port=9000, debug=False)

if __name__ == "__main__":
    main()

