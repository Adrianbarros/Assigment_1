from flask import Flask, render_template, request,make_response, redirect, abort, url_for
import os
import json
import requests


data={}
#url
def _url(path):
    return 'https://hunter-todo-api.herokuapp.com/' + path

# r=requests.get('https://hunter-todo-api.herokuapp.com')

with open ('data.json') as f:
	data = json.load(f)
#pprint(data)
app=Flask(__name__)

#main page
@app.route('/')
def home():
	return render_template('mypage.html', todos=data)

#second page: login, register, etc
@app.route("/login")
def login():
    return render_template('login.html')

#todo list page request
@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    return (projectpath)


#first Regirster a new User

@app.route('/login/post', methods=['POST']) 
def register_user():
	newUsername = request.form['newUsername']
	if (newUsername ==""):
		return make_response("Please enter a username" '<a href ="/> Home</a>')
	requests.post(_url('user'), json= {'username' : newUsername})
	respo = make_response("You are now registered!" '<a href ="/> Home</a>')
	return respo




# 1e 2 Authenticate
@app.route("/auth", methods=['POST'])
def authenticate_user():
    authUser = request.form['authUser']
    if (authUser == ""):
        return make_response("Username is empty. Please try again. " '<br>' '<a href="/">Return Home</a>')
                             
    req = requests.post(_url('auth'), json={'username': authUser})
    json_data = req.json()
    try:
        token = json_data['token']
    except:
        token = ""
    if (token == ""):
        return make_response("Username not found. Please try again. "
                             '<a href="/loing">Home</a>')
    valid_responce= make_response("You are logged in! " '<br>' '<a href="/login""> Return Home</a>')

    resp = make_response(valid_responce)
    resp.set_cookie('sillyauth', value=token)
    return resp




#
@app.route("/create_item", methods=['POST'])
def create_item():
    cookies = request.cookies
    newItem = request.form['newItem']
    if (newItem == ""):
        return make_response("Input is empty. Please try again. "
                             '<a href="/login">Home</a>')
    requests.post(_url('todo-item'), cookies=cookies, json={'content': newItem})
    return make_response("Item successfully created. " '<a href="/login">Home</a>')
#shows all the items
@app.route("/get_items")
def get_items():
    cookies= request.cookies
    resp =requests.get(_url('todo-item'), cookies=cookies)
    #return render_template('list.html',resp=data)
    return resp.text


#changes an Item on the list
@app.route("/change_item", methods=['POST'])
def change_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    newItem = request.form['newItem']
    if (itemID == "" or newItem == ""):
        return make_response("Please try again.Input is empty "
                             '<a href="/login"> Go Back</a>')
    data = '{"content": "' + newItem + '"}'
    requests.put(_url('todo-item/') + itemID, cookies=cookies, data=data)
    return make_response("Item successfully changed. " '<a href="/login">Go Back</a>')
 
#6) Delete an item
@app.route("/delete_item", methods=['POST'])
def delete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Input is empty. Please try again. "
                             '<a href="/login">Home</a>')
    requests.delete(_url('todo-item/') + itemID, cookies=cookies)
    return make_response("Item successfully deleted. " '<a href="/login">Home</a>')


#7) Mark an item as completed
@app.route("/complete_item", methods=['POST'])
def complete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Input is empty. Please try again. "
                             '<a href="/">Home</a>')
    requests.put(
        _url('todo-item/') + itemID, cookies=cookies, json={'completed': True})
    return make_response("Item successfully marked as completed. "
                         '<a href="/">Home</a>')
# log out funtion
@app.route("/logout")
def logout():
    resp = make_response("You are OUT! " '<a href="/"> Go Home</a>')
    resp.set_cookie('sillyauth',  expires=0)
    return resp

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)
