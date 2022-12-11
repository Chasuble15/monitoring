FROM python:3.9.13
WORKDIR /se
COPY . /se
RUN pip install requests
RUN pip install prometheus-client
RUN pip install pyyaml
EXPOSE 9300
ENV NOM gap
CMD ["python", "shelly_exporter.py"]