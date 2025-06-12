# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"


@app.route("/games", methods=["GET"])
def games():
    games = [
        game.to_dict(only=("title", "genre", "platform", "price"))
        for game in Game.query.all()
    ]
    
    return make_response(games, 200)


@app.route("/games/<int:id>", methods=["GET"])
def game_by_id(id):
    game = Game.query.filter_by(id=id).first()
    return make_response(
        game.to_dict(
            only=("title", "genre", "platform", "price")), 200)


@app.route("/games/users/<int:id>", methods=["GET"])
def game_users(id):
    game = Game.query.filter_by(id=id).first()
    users = [user.to_dict(only=("name",)) for user in game.users]
    return make_response(users, 200)
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)

