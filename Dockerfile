FROM python:3.10.4

ADD main.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]