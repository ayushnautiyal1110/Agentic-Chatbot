#Base Image
FROM python:3.13.4

#Working Directory 
WORKDIR /app


#Copy
COPY . /app

#Run
RUN pip install -r requirements.txt


#Port
EXPOSE 8501


# Main Command
CMD ["streamlit","run","app.py"]
