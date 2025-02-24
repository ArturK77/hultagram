from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    lyrics = db.Column(db.String(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Song {self.title}>'
    
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    # Display a list of songs
    songs = Song.query.order_by(Song.date_added.desc()).all()
    render_template('index.html', song = songs)

@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        lyrics = request.form['lyrics']
        new_song = Song(title = title, artist = artist, lyrics = lyrics)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)