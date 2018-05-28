# test algolia

REST API that expose two endpoints :

* `/1/queries/count/<DATE_PREFIX>`
* `/1/queries/popular/<DATE_PREFIX>?size=<SIZE>`

use this [data file](https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=0) as the source

## how to use

Use python v3.6.5 and [pipenv](https://github.com/pypa/pipenv)

to run the API (I use port 5000) :
* pipenv install
* python3 app.py

to run the test against the API:
* python3 test.py

## Data structure choice

I take advantage of dictionnaries ability to quickly find a key in O(1) complexity.
Each part of the date become a key, until I reach minute where I aggregate results from each second.
I've chosen to make 3 levels of aggregation (day, hour, minute) to improve the perf, losing RAM instead of processor time.

## Limits

The `get_most_popular` function sort all the dictionnary, it can be quite slow when the dataset get's bigger.
I've tried other solutions for the `get_most_popular` function such as :
* `heapq.nlargest(n, d.items(), key=lambda i: i[1])`
* `Counter(d).most_common(n)`

but it doesn't perform better when I bench.
It could probably be improved with a good selection algorithm, witch is quite hard to implement.