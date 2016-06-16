import os
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from cjapp.forms import JobForm


app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

@app.route("/")
def load_page():
    return(render_template("index.html", form=JobForm))

if __name__ == "__main__":
    app.run()