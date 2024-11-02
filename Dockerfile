FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY .env .env
RUN mkdir logs/

# For Global (Sync all guilds)
# CMD ["python", "src/bot.py", "--global"]

# For debugging (Sync guild only)
CMD ["python", "src/bot.py"]