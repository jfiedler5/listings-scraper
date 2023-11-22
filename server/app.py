from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DATABASE = {
    'drivername': 'postgres',
    'host': 'db',
    'port': '5432',
    'username': 'postgres',
    'password': 'postgres',
    'database': 'scrapy_db'
}

def get_data():
    conn = psycopg2.connect(
        dbname=DATABASE['database'],
        user=DATABASE['username'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port']
    )
    cur = conn.cursor()
    cur.execute("SELECT title, image_url FROM scrapy_table LIMIT 500")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items

@app.route('/')
def index():
    items = get_data()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
