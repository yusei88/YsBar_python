from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return render_template('index.html', title="Y'sBAR")

@app.route('/gin')
def menu():
    return render_template('gin.html', title="gin")


if __name__ == "__main__":
    app.run(debug=True)