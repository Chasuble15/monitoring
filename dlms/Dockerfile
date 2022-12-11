FROM python:3.9.13
WORKDIR /de
COPY . /de
RUN pip install -r requirements.txt
EXPOSE 9600
ENV NOM gap
CMD ["python", "dlms_exporter.py"]