from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__, template_folder='C:/Users/alexe/Documents/PyCharm Community Edition 2023.1.1/PROJECTS/vt6/templates')


@app.route('/')
def index():
    user_ip = request.remote_addr
    haveIP = 0
    with open('data/users/users.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            username, userip = user.strip().split()
            if userip == user_ip:
                haveIP += 1
                break
        file.close()
    if haveIP == 1:
        return render_template('dialog.html', username=username)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['user']
    user_ip = request.remote_addr
    with open('data/users/users.txt', 'a') as file:
        file.write(username + ' ' + user_ip + '\n')
        file.close()
    return render_template('dialog.html', username=username)


@app.route('/get_messages')
def get_messages():
    with open('data/messagesHistory/messageHistory.txt', 'r') as file:
        messages = file.readlines()
    return jsonify(messages=messages)


@app.route('/update_messages', methods=['POST'])
def update_messages():
    user_ip = request.remote_addr
    with open('data/users/users.txt', 'r') as file:
        users = file.readlines()
        for user in users:
            username, usernameandIP = user.strip().split()
            if usernameandIP == user_ip:
                break
        file.close()
    message = request.form['message']
    message = '(' + datetime.datetime.now().strftime("%H:%M") + ') ' + username + ': ' + message
    with open('data/messagesHistory/messageHistory.txt', 'a') as file:
        file.write(message + '\n')
    return jsonify(result="Message added successfully")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
