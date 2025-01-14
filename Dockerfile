FROM python:3

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

ENTRYPOINT [ "python3", "bot.py" ]