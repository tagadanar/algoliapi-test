#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import datetime
from functools import reduce
from time import time
from dictionnaries import Vividict, Counterdict

# Setting up Flask app
app = Flask(__name__)

# Setting up global logs dict
logs_minute = Vividict()
logs_hour = Vividict()
logs_day = Vividict()


# Utility functions
def load_logs(filename):
    print("loading, please wait...")
    start = time()
    with open(filename, 'r') as f:
        for line in f:
            splited = line.strip('\n').split('\t')
            date = datetime(*map(int, splited[0].replace(":", "-").replace(" ", "-").split("-")))
            url = splited[1]
            add_to_logs(date, url)
    end = time()
    print("loaded in : " + str(round(end - start, 3)) + "s")


def add_to_logs(date, url):
    """ Aggregate url counter on minute, hour and day step """
    # minutes
    counterdict = logs_minute[date.year][date.month][date.day][date.hour][date.minute]
    if not isinstance(counterdict, Counterdict):
        counterdict = logs_minute[date.year][date.month][date.day][date.hour][date.minute] = Counterdict()
    counterdict[url] += 1
    # hours
    counterdict = logs_hour[date.year][date.month][date.day][date.hour]
    if not isinstance(counterdict, Counterdict):
        counterdict = logs_hour[date.year][date.month][date.day][date.hour] = Counterdict()
    counterdict[url] += 1
    # days
    counterdict = logs_day[date.year][date.month][date.day]
    if not isinstance(counterdict, Counterdict):
        counterdict = logs_day[date.year][date.month][date.day] = Counterdict()
    counterdict[url] += 1


def recurse_iter(d):
    """ Generator that iterate over nested Vividict d and yield on Counterdict a (key, value) tuple """
    if isinstance(d, Vividict):
        for k in d:
            for rv in recurse_iter(d[k]):
                yield rv
    elif isinstance(d, Counterdict):
        for k, v in d.items():
            yield (k, v)


def get_nested_logs(date_str):
    """ Return nested Vividict in logs_xxx according to date_str """
    date_array = date_str.replace(":", "-").replace(" ", "-").split("-")
    date_map = map(int, date_array)
    if len(date_array) <=3: # request period is day or bigger
        nested = reduce(lambda a, b: a[b], date_map, logs_day)
    elif len(date_array) <= 4: # request period is hour or bigger
        nested = reduce(lambda a, b: a[b], date_map, logs_hour)
    else:
        nested = reduce(lambda a, b: a[b], date_map, logs_minute)
    return nested


def sum_nested_logs(nested):
    """ Sum aggregated url counter of the nested Vividict """
    result = Counterdict()
    for url, nb_hit in recurse_iter(nested):
        result[url] += nb_hit
    return result


def get_most_popular(d, n):
    """ Return the n most popular query inside nested dict d """
    return dict(sorted(d.items(), key=lambda e: e[1], reverse=True)[:n])


@app.route('/1/queries/count/<date_prefix>', methods=['GET'])
def count(date_prefix=None):
    nested_logs = get_nested_logs(date_prefix)
    summed_logs = sum_nested_logs(nested_logs)
    count = sum(1 for i in summed_logs)
    return jsonify({"count": count})


@app.route('/1/queries/popular/<date_prefix>', methods=['GET'])
def popular(date_prefix=None):
    size = request.args.get('size', type=int, default=3)
    nested_logs = get_nested_logs(date_prefix)
    summed_logs = sum_nested_logs(nested_logs)
    result = get_most_popular(summed_logs, size)
    json = {"queries": []}
    for query, count in result.items():
        json["queries"].append({"query": query, "count": count})

    return jsonify(json)


# LOADING LOGS
load_logs("hn_logs.tsv")
if __name__ == '__main__':
    # LAUNCHING REST API
    app.run(host='0.0.0.0', port=5000, debug=False)
