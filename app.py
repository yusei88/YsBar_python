from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello World"
    return render_template('top.html', title="トップページ", name="SATO")

if __name__ == "__main__":
    app.run(debug=True)