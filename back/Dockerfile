FROM python:3.12-slim
WORKDIR /app
#(the . here means copy it into the current working directory )
COPY requirements.txt .
#(-r means read the file LOL)
RUN pip install -r requirements.txt
COPY . . 
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
