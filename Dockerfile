FROM python:3.9-slim
WORKDIR /app

# Copy files
COPY .streamlit/ .streamlit/
COPY requirements.txt .
COPY streamlit_app.py .

# Install dependencies
RUN pip install -r requirements.txt

# Run app
CMD ["streamlit", "run", "streamlit_app.py"]
