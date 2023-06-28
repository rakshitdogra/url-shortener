from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='KJC635sjdbgh@#adkjf',
    database='url_shortener'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        shortened_url = generate_shortened_url()
        store_url(original_url, shortened_url)
        return render_template('shortened.html', shortened_url=shortened_url)
    return render_template('index.html')

@app.route('/<shortened_url>')
def redirect_url(shortened_url):
    original_url = get_original_url(shortened_url)
    if original_url:
        return redirect(original_url)
    else:
        return render_template('404.html'), 404

def generate_shortened_url():
    cursor = db.cursor()
    cursor.execute('SELECT LAST_INSERT_ID()')
    last_id = cursor.fetchone()[0]
    shortened_url = f'{last_id}'+"Here"
    cursor.close()
    return shortened_url

def store_url(original_url, shortened_url):
    cursor = db.cursor()
    query = 'INSERT INTO urls (original_url, shortened_url) VALUES (%s, %s)'
    cursor.execute(query, (original_url, shortened_url))
    db.commit()
    cursor.close()

def get_original_url(shortened_url):
    cursor = db.cursor()
    query = 'SELECT original_url FROM urls WHERE shortened_url = %s'
    cursor.execute(query, (shortened_url,))
    original_url = cursor.fetchone()
    cursor.close()
    if original_url:
        return original_url[0]
    return None

if __name__ == '__main__':
    app.run(debug=True)