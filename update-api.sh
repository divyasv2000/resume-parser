git pull
pm2 delete 0
pm2 start "uvicorn api:app --host 0.0.0.0 --port 8000"
