FROM python:3.12.0a4-bullseye
WORKDIR /app
COPY . .
#CMD ["sh", "./python_setup.sh"] 
RUN pip install -r requirements.txt
CMD ["python","./bot.py"]
