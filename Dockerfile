FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
  git \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV REPO_URL=https://github.com/giantgenai/ai-investment-advisor.git
ENV REPO_NAME=ai-investment-advisor

WORKDIR /testbed/${REPO_NAME}

# Clone the mock_test branch
RUN git init && \
  git remote add origin ${REPO_URL} && \
  git fetch --depth 1 origin mock_test && \
  git checkout FETCH_HEAD && \
  git remote remove origin

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
