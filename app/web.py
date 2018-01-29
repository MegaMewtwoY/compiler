from flask import Flask, render_template, redirect, url_for, request, jsonify, json
from compiler import *
import global_var

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you cannot guess this key'



@app.route('/output/', methods=['POST'])
def get_data():
    data = request.get_json()
    code = data['data']
    if code:
        output = action(code, language)
        global_var.set_global("")
        return jsonify({'ok': output})

    return jsonify({'ok': "null"})


@app.route('/input/', methods=['POST'])
def get_input():
    data = request.get_json()
    user_input = data['data']
    global_var.set_global(user_input)
    if user_input:
        return jsonify({'ok': user_input})
    else:
        return jsonify({'ok': "null"})


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('c'))


@app.route('/c/', methods=['GET'])
def c():
    global language
    language = 'c'
    default_code = '''#include<stdio.h>
int main(){
    printf("test\\n");
    return 0;
}'''
    return render_template('index.html', default_code=default_code, lang='c')


@app.route('/cpp/', methods=['GET'])
def cpp():
    global language
    language = 'cpp'
    default_code = '''#include<iostream>
using namespace std;
int main(){
    cout<<"test"<<endl;
    return 0;
}'''
    return render_template('index.html', default_code=default_code, lang='cpp')


@app.route('/python2/', methods=['GET'])
def python2():
    global language
    language = "python2"
    default_code = '''#!/usr/bin/python
# -*- coding: utf-8 -*-
print "test"
'''
    return render_template(
        'index.html', default_code=default_code, lang='python2')


@app.route('/python3/', methods=['GET'])
def python3():
    global language
    language = "python3"
    default_code = '''#!/usr/bin/python3
# -*- coding: utf-8 -*-
print("test")
'''
    return render_template(
        'index.html', default_code=default_code, lang='python3')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
