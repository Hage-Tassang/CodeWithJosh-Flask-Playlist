# importing necessary libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #ORM for database interactions with pure python code

# Initialize the Flask application
app = Flask(__name__)


# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_destinations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database
db = SQLAlchemy(app)

# Model is like row in the database table and it has column as attributes
# Define a model for the
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(200), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'country': self.country,
            'rating': self.rating
        }










# Routes
#root route eg: http://something.com/
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Travel Destinations API!"})

#Read method to get all destinations
#reading all destinations
# http://something.com/destinations
@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([dest.to_dict() for dest in destinations])

# http://something.com/destinations/<id>
@app.route('/destinations/<int:id>', methods=['GET'])
def get_destination(id):
    destination = Destination.query.get(id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination not found"}), 404
    

# POST method to add new destination
@app.route('/destinations', methods=['POST'])
def add_destination():
    data = request.get_json()
    new_destination = Destination(
        destination=data['destination'],
        country=data['country'],
        rating=data['rating'])
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict()),201

#PUT method to update existing destination
@app.route('/destinations/<int:id>', methods=['PUT'])
def update_destination(id):
    data = request.get_json()
    destination = Destination.query.get(id)
    if destination:
        destination.destination = data.get('destination', destination.destination)
        destination.country = data.get('country', destination.country)
        destination.rating = data.get('rating', destination.rating)
        db.session.commit()
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "Destination not found"}), 404
    

# DELETE method to delete a destination
@app.route('/destinations/<int:id>', methods=['DELETE'])
def delete_destination(id):
    destination = Destination.query.get(id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({"message": "Destination deleted"})
    else:
        return jsonify({"error": "Destination not found"}), 404

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    