## 🏃‍♂️ How to Run

Open **Separate terminal windows** in the project directory.

### Terminal 1: Start Redis
Start the Redis container to handle the queue.
```bash
docker run -d -p 6379:6379 redis
```

### Terminal 2: Start the AI Worker
This process loads the heavy AI models and processes images. Note: We use --pool=solo to prevent memory crashes on macOS/Linux with PyTorch.
```bash
python3 -m celery -A tasks worker --loglevel=info --pool=solo
```

### Terminal 3: Start the AI Worker
python3 -m celery -A tasks worker --loglevel=info --pool=solo
```bash
python3 main.py
```

### Terminal 4: celery -A tasks flower
To visualize the queue and worker status, you can use Flower.
```bash
celery -A tasks flower
```