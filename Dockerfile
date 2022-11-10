FROM python:3.8-slim
COPY . /app 
WORKDIR /app 
RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt
RUN python download.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]


