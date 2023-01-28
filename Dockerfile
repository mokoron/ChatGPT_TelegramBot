FROM python:3.12.0a4-bullseye
WORKDIR /app
COPY . .
#CMD ["sh", "./python_setup.sh"] 
RUN sh ./python_setup.sh
CMD ["python","./bot.py"]
