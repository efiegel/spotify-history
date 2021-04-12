from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

from flask import Flask, request,render_template
import psycopg2
try: 
    conn = psycopg2.connect(database=os.environ['HEROKU_DB_NAME'],
                            user=os.environ['HEROKU_DB_USER'],  
                            password=os.environ['HEROKU_DB_PASS'],
                            host=os.environ['HEROKU_DB_HOST'])
    cur = conn.cursor()
except:
    print ("cannot connect to database")

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/track_history')
def track_history():
    sql = \
        """
        select
            track_name,
            artist_name,
            album_name,
            played_at
        from track_history
        order by played_at desc;
        """
    cur.execute(sql)
    data = cur.fetchall()
    return render_template('track_history.html', data=data)

@app.route('/most_popular')
def most_popular():
    sql = \
        """
        select
            artist_name,
            count(played_at) track_listens,
            count(distinct(track_id)) unique_tracks,
            count(distinct(album_id)) albums
        from track_history
        group by artist_name
        order by track_listens desc
        limit 5;
        """
    cur.execute(sql)
    data = cur.fetchall()
    return render_template('most_popular.html', artist_data=data)

if __name__ == '__main__':
    app.run()
