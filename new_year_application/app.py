from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    new_year = datetime(datetime.now().year + 1, 1, 1)
    days_until_new_year = (new_year - datetime.now()).days
    return render_template('index.html', days=days_until_new_year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
