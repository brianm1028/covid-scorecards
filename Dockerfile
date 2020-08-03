FROM python:3
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
ENV FLASK_APP wsgi.py
ENV FLASK_ENV development
ENV FLASK_DEBUG 1
EXPOSE 5000
CMD ["python", "-m", "flask", "run"]
