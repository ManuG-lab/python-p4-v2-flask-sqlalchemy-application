# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# add views here 

@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>', 
        200
        )
    return response

@app.route('/pets/<int:id>')
def get_pet(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        respons_body = f'<p>{pet.name} {pet.species}</p>'
        response_status = 200
    else:
        respons_body = f'<p>Pet{id}not found</p>'
        response_status = 404
    response = make_response(respons_body, response_status)
    return response


@app.route('/pets/<string:species>')
def get_pets_by_species(species):
    pets = Pet.query.filter(Pet.species == species).all()
    size = len(pets)

    response_body = f'<p>There are {size} {species}:</p>'
    for pet in pets:
        response_body += f'<p>{pet.name}</p>'

    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
