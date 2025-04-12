name: Notify on Commit

on:
  push:
    branches:
      - '*' 
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  notify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run commit notification script
        run: |
          python notify_commit.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
