FROM python:3.11-slim-bookworm

RUN apt-get update && rm -rf /var/lib/apt/lists/*

ENV REPO_NAME=ai-investment-advisor

WORKDIR /testbed/${REPO_NAME}

COPY . /testbed/${REPO_NAME}

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and set minimum required permissions
RUN useradd -m appuser && \
    chown -R appuser:appuser /testbed/${REPO_NAME} && \
    chmod -R 755 /testbed/${REPO_NAME}

USER appuser

EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/investment_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
