## How to Add Tasks and Run the Queue

### Add a Task (Producer)
To add tasks run:

```bash
for i in {1..100}; do python3 producer.py "Call $i"; done
```

To process tasks from the queue, run:

```bash
python3 consumer.py
```