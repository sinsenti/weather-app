FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .


# for production you can use 
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
