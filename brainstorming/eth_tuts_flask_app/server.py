from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/read_my_token")
def read_my_token():
    print("Reading contract file")
    f = open("contracts/MyToken.sol", "r")
    return f.read()


@app.route("/read_greeter")
def read_greeter():
    print("Reading contract file")
    f = open("contracts/Greeter.sol", "r")
    return f.read()

if __name__ == "__main__":
    app.run()