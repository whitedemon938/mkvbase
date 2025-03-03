FROM python:3.14.0a5-bookworm

RUN apt update && apt install -y git mkvtoolnix

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN python3 -m venv mkvenv

COPY requirements.txt .
RUN mkvenv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]

