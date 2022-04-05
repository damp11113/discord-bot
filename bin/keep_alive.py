# keep_alive.py
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def index():
    return 'I am alive!', 200

def run():
    app.run(host='0.0.0.0', port=8021)

def keepalive():
    t = Thread(target=run)
    t.start()
