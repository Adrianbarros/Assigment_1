from flask import Flask, render_template, request
import os
import json
import requests


data={}

r=requests.get('https://hunter-todo-api.herokuapp.com')

with open ('data.json') as f:
	data = json.load(f)
#pprint(data)
app=Flask(__name__)

@app.route('/')
def home():
	return render_template('mypage.html', todos=data)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    return (projectpath)

if __name__=="__main__":
	app.run(debug=True)
	port = int(os.environ.get("PORT", 5000))
