* QQuick start

1. build docker image
   docker build -t colocation:development .
   docker run -p 5000:5000 colocation:development
   curl -X POST -F csv=@"/path/to/my/file/test.csv" http://localhost:5000/api/colocation

* Development

1. pip install -r requirements.txt
2. setup environment
   export FLASK_APP=app.py
   export PYTHONPATH=`pwd`
   export DATAFILE= ... your datafile ...
3. load data
   flask data init
   flask data load $DATAFILE
4. serve
   flask run
5. ui
   cd ui; npm start
