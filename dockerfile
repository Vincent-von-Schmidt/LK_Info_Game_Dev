FROM python:3.10.9

COPY requirements.txt ./
RUN pip install --no-cache-dir - requirements.txt

COPY . .

CMD [ "python", "./src/main.py" ]
