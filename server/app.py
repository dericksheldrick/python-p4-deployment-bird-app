import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Bird

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Root route (for direct visits to /)
@app.route('/')
def index():
    return render_template("index.html")

# API Resource: /api/birds
class Birds(Resource):
    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)

    def post(self):
        data = request.get_json()
        new_bird = Bird(
            name=data.get('name'),
            species=data.get('species'),
            image=data.get('image'),
        )
        db.session.add(new_bird)
        db.session.commit()
        return make_response(new_bird.to_dict(), 201)

# API Resource: /api/birds/<id>
class BirdByID(Resource):
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first()
        if not bird:
            return make_response({"error": "Bird not found"}, 404)
        return make_response(bird.to_dict(), 200)

    def patch(self, id):
        bird = Bird.query.filter_by(id=id).first()
        if not bird:
            return make_response({"error": "Bird not found"}, 404)

        data = request.get_json()
        for attr in data:
            setattr(bird, attr, data[attr])
        db.session.commit()

        return make_response(bird.to_dict(), 200)

    def delete(self, id):
        bird = Bird.query.filter_by(id=id).first()
        if not bird:
            return make_response({"error": "Bird not found"}, 404)

        db.session.delete(bird)
        db.session.commit()
        return make_response('', 204)

# Register API routes
api.add_resource(Birds, '/api/birds')
api.add_resource(BirdByID, '/api/birds/<int:id>')

# Catch-all for React routes
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")
