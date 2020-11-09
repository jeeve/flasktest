# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:26:02 2020

@author: JV
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world !"

if __name__ == "__main__":
    app.run()