FROM python:3.10.9

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/main.py" ]
