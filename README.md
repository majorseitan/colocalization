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
