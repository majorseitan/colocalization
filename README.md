* Quick start

  pull the container

  docker pull majorseitan/colocation:development

  start the docker container

  docker run -p 6666:8888 majorseitan/colocation:development

  this command loads the data and returns the number of rows loaded

  curl -X POST -F csv=@path/your/data/file http://localhost:8888/api/colocalization


* Build container
1. build docker image

   docker build -t colocalization:development .

   docker run -p 5000:5000 colocalization:development

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
