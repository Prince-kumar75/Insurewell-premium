#use python 3.11 base image 
FROM python:3.11-slim
#set working dir 
WORKDIR /app
#copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy the rest of the application code
COPY . .

#expose port 
EXPOSE 8000

#command to run the application
CMD ["uvicorn", "appml:app", "--host", "0.0.0.0", "--port", "8000"]