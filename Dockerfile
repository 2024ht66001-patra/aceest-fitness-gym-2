FROM python:3.11-slim
WORKDIR /app
COPY app /app/app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV FLASK_APP=app/ACEest_Fitness.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
