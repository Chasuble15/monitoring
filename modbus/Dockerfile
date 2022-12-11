FROM python:3.9.13
WORKDIR /me
COPY . /me
RUN pip install pyModbusTCP
RUN pip install prometheus-client
RUN pip install pyyaml
EXPOSE 9400
ENV NOM gap
CMD ["python", "modbus_exporter.py"]