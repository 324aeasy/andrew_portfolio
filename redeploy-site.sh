#!/bin/bash

PROJECT_DIR="/root/andrew_portfolio"
VENV_PATH="/root/andrew_portfolio/python3-virtualenv"

echo "Starting deployment..."

# 1. Kill all existing tmux sessions
tmux kill-server

# 2. cd into project folder, or exit with error if not found
cd $PROJECT_DIR || { echo "Directory $PROJECT_DIR not found"; exit 1; }

# 3. Fetch latest changes and reset
git fetch && git reset origin/main --hard

# 4. Enter Python venv and install dependencies
source VENV_PATH/bin/activate
pip install -r requirements.txt

# 5. Start new detached tmux session
tmux new-session -d -s flask-server 'source VENV_PATH/bin/activate && flask run --host=0.0.0.0 --port=80'

echo "Deployment complete!"
echo "Flask server running in tmux session: flask-server"
