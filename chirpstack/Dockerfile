FROM python:3.9.13
WORKDIR /ch
COPY . /ch
RUN pip install prometheus-client
EXPOSE 9200
EXPOSE 9201
ENV NOM gap
CMD ["python", "chirpstack_exporter.py"]