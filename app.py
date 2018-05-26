# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import datetime
from functools import reduce
from time import time
from dictionnaries import Vividict, Counterdict

# setting up Flask app
app = Flask(__name__)
# setting up global logs dict
logs = Vividict()


# utility functions
def load_logs():
    print("loading... please wait.")
    start = time()
    with open("hn_logs.tsv", 'r') as f:
        for line in f:
            splited = line.strip('\n').split('\t')
            date = datetime(*map(int, splited[0].replace(":", "-").replace(" ", "-").split("-")))
            url = splited[1]
            add_to_logs(date, url)
    end = time()
    print( str(round(end - start, 3)) + "s")

def add_to_logs(date, url):
    counterdict = logs[date.year][date.month][date.day][date.hour][date.minute]
    if not isinstance(counterdict, Counterdict):
        counterdict = logs[date.year][date.month][date.day][date.hour][date.minute] = Counterdict()
    counterdict[url] += 1

def recurse_iter(d):
    if isinstance(d, Vividict):
        for k in d:
            for rv in recurse_iter(d[k]):
                yield rv
    elif isinstance(d, Counterdict):
        for k, v in d.items():
            yield (k, v)

def get_nested_logs(date_str):
    date_array = map(int, date_str.replace(":", "-").replace(" ", "-").split("-"))
    nested = reduce(lambda a,b: a[b], date_array, logs)
    return nested

def sum_nested_logs(nested):
    result = Counterdict()
    for url, nb_hit in recurse_iter(nested):
        result[url] += nb_hit
    return result

def get_most_popular(d, n):
    return dict(sorted(d.items(), key=lambda e: e[1], reverse=True)[:n])




@app.route('/1/queries/count/<date_prefix>', methods=['GET'])
def count(date_prefix=None):
    nested_logs = get_nested_logs(date_prefix)
    summed_logs = sum_nested_logs(nested_logs)
    count = sum(1 for i in summed_logs)
    return jsonify({ "count": count })

@app.route('/1/queries/popular/<date_prefix>', methods=['GET'])
def popular(date_prefix=None):
    size = request.args.get('size', type=int, default=3)
    nested_logs = get_nested_logs(date_prefix)
    summed_logs = sum_nested_logs(nested_logs)
    result = get_most_popular(summed_logs, size)
    json = { "queries": []}
    for query, count in result.items():
        json["queries"].append({"query":query, "count":count})

    return jsonify(json)


# LOADING LOGS
load_logs()
if __name__ == '__main__':
    # LAUNCHING REST API
    app.run(host='0.0.0.0', port=5000, debug=False)