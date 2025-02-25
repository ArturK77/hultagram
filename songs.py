# app.py - COMPLETED VERSION
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Song Model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Song {self.title}>'

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    songs = Song.query.order_by(Song.date_added.desc()).all()
    total_songs = len(songs)
    favorite_songs = sum(1 for Song in songs if Song.favorite)
    return render_template('index.html', 
                          songs=songs,
                          total_songs=total_songs,
                          favorite_songs=favorite_songs)

@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        favorite = 'favorite' in request.form
        new_song = Song(title=title, artist=artist, favorite=favorite)
        db.session.add(new_song)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/toggle_favorite", methods=["POST"])
def toggle_favorite():
    data = request.json
    song_id = data.get("song_id")
    favorite = data.get("favorite")
    song = db.session.get(Song, song_id)  # Find the song in the database
    if song:
        song.favorite = favorite  # Update favorite status
        db.session.commit()  # Save changes to the database
        return jsonify({"success": True, "song_id": song_id, "favorite": favorite})
    return jsonify({"success": False, "error": "Song not found"}), 404

@app.route('/delete/<int:song_id>', methods=["POST"])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id) 
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
