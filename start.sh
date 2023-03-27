#!/bin/bash


# Execute your command here
echo "PostgreSQL is up!"

# Run the first script
python3 app/tables.py &

# Wait for the first script to finish
wait

# Start the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
