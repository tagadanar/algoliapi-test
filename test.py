#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

queries = [
	('http://localhost:5000/1/queries/count/2015', { "count": 573697 }),
	('http://localhost:5000/1/queries/count/2015-08', { "count": 573697 }),
	('http://localhost:5000/1/queries/count/2015-08-03', { "count": 198117 }),
	('http://localhost:5000/1/queries/count/2015-08-01 00:04', { "count": 617 }),
	('http://localhost:5000/1/queries/popular/2015?size=3', { "queries": [
        { "query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 6675 },
        { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 4652 },
        { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 3100 }
    ]}),
	('http://localhost:5000/1/queries/popular/2015-08-02?size=5', { "queries": [
        { "query": "http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice", "count": 2283 },
        { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045", "count": 1943 },
        { "query": "http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1", "count": 1358 },
        { "query": "http%3A%2F%2Fjamonkey.com%2F50-organizing-ideas-for-every-room-in-your-house%2F", "count": 890 },
        { "query": "http%3A%2F%2Fsharingis.cool%2F1000-musicians-played-foo-fighters-learn-to-fly-and-it-was-epic", "count": 701 }
    ]}),
]

for test in queries:
	r = requests.get(test[0])
	try:
		json_result = r.json()
	except json.JSONDecodeError as e:
		print("{} {}".format(test[0], "NOK"))
		continue
	is_equal = json.dumps(json_result, sort_keys=True) == json.dumps(test[1], sort_keys=True)
	if not is_equal:
		print(json.dumps(json_result, sort_keys=True))
		print(json.dumps(test[1], sort_keys=True))
	result = "OK" if is_equal else "NOK"
	print("{} {}".format(result, test[0]))
