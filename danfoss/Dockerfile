FROM python:3.9.13
WORKDIR /de
COPY . /de
RUN pip install requests
RUN pip install prometheus-client
EXPOSE 9500
ENV NOM gap
CMD ["python", "danfoss_exporter.py"]