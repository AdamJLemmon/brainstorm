from flask import Flask, redirect, url_for, request
from flask import render_template
from storage import StorageManager

server = Flask(__name__)

ip = '192.168.0.23'
port = 27017
db = 'brainstorm'
sm = StorageManager(ip, port, db)

@server.route('/')
def homepage():
    return render_template('homepage.html')

@server.route('/contract')
def contract():
    return render_template('contract.html')

@server.route('/read_contract')
def read_contract_file():
    print("Reading contract file")
    f = open("contract.sol", "r")
    return f.read()
