from flask import Flask
from flask import render_template
from flask import request
from threading import Thread
from replit import db

app = Flask('')


@app.route('/')
def main():
    return "wow so fast pavel"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
