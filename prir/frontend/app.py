from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

ENGINE_URL = "http://engine:8000"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form['urls'].split()
        profile = request.form['profile']
        data = {'urls': urls, 'profile': profile}
        requests.post(f"{ENGINE_URL}/crawl", json=data)
        return redirect('/results')
    return render_template('index.html')

@app.route('/results')
def results():
    try:
        resp = requests.get(f"{ENGINE_URL}/results")
        data = resp.json()
    except Exception:
        data = []
    return render_template('results.html', results=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
