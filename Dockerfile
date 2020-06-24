FROM node:14.4.0-stretch AS NODE_BUILDER
ADD ui /opt/ui
RUN cd /opt/ui; npm run build

FROM python:3.8

COPY --from=NODE_BUILDER /opt/ui/build /app/static
COPY colocation /app/colocation
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt
ENV FLASK_APP=/app/app.py
ENV PYTHONPATH=/app
RUN flask data init

CMD [ "flask", "run", "--host=0.0.0.0" ]