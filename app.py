from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
	return "Hello World!"
if __name__ == '__main__':
	app.run(debug=True)
