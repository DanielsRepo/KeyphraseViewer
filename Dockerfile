FROM python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/boudinfl/pke.git && python -m nltk.downloader stopwords && python -m nltk.downloader universal_tagset

COPY . .

# COPY ./nltk_data /usr/local/nltk_data

EXPOSE 5000

# CMD ["python", "app.py"]