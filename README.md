# test algolia

REST API that expose two endpoints :

* /1/queries/count/<DATE_PREFIX>
* /1/queries/popular/<DATE_PREFIX>?size=<SIZE>

use this [data file](https://www.dropbox.com/s/duv704waqjp3tu1/hn_logs.tsv.gz?dl=0) as the source

## how to use

Use python v3.6.5 and [pipenv](https://github.com/pypa/pipenv)

to run the API (I use port 5000) :
* pipenv install
* python3 app.py

to run the test against the API:
* python3 test.py
