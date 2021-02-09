from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
from flask_bootstrap import Bootstrap
import json
import os.path

app = Flask(__name__)
app.secret_key = '2kyjGM%V?6AT5N&'

bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html',codes=session.keys())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls= {}
        if os.path.exists('urls.json'):
            with open('urls.json')as url_file:
                urls = json.load(url_file)
        if request.form['code'] in urls.keys():
                flash('Hey there, sorry, this already exists.  Please choose another name.')
                return redirect(url_for('index'))
        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]=True
        flash('That worked, added your shortcut!')
        return render_template('your_url.html', code=request.form['code'])
    else:
        flash('Hey there, sorry, cannot enter directly.  Please use the form to generate your shortcut.')
        return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json')as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
    return abort(404)

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
