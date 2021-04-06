from flask import Flask, render_template
import os

app = Flask(__name__)

@app.context_processor
def add_staticfile():
    def staticfile_cp(fname):
        path = os.path.join(app.root_path, 'static', fname)
        mtime =  str(int(os.stat(path).st_mtime))
        return '/static/' + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)

@app.route('/')
def hello():
    name = "Hello World"
    return render_template('index.html', title="Y'sBAR")

@app.route('/gin')
def menu():
    return render_template('gin.html', title="gin")

if __name__ == "__main__":
    app.run(debug=True)