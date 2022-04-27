"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    directors = Director.query.order_by(Director.director_id).limit(3).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(directors)
    return data


def read_one(director_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people
    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    director = (
        Director.query.filter(Director.director_id == director_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    # Did we find a person?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {director_id}")


def create(director):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    name=director.get("name") 
    gender=director.get("gender")
    uid=director.get("uid")
    department=director.get("department")

    existing_director = (
        Director.query.filter(Director.name == name)
        .filter(Director.gender == gender)
        .filter(Director.uid == uid)
        .filter(Director.department == department)
        .one_or_none()
    )
    
    # print('#########', existing_director)
    # Can we insert this person?
    if existing_director is None:
        
        # Create a person instance using the schema and the passed in person
        schema = DirectorSchema()
        new_director = schema.load(director, session=db.session)

        # Add the person to the database
        db.session.add(new_director)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_director)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f"Director {name} {uid} exists already")


def update(director_id, director):
    """
    This function updates an existing person in the people structure
    :param person_id:   Id of the person to update in the people structure
    :param person:      person to update
    :return:            updated person structure
    """
    # Get the person requested from the db into session
    update_director = Director.query.filter(
        Director.director_id == director_id
    ).one_or_none()

    # Did we find an existing person?
    if update_director is not None:

        # turn the passed in person into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the person we want to update
        update.director_id = update_director.director_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {director_id}")


def delete(director_id):
    """
    This function deletes a person from the people structure
    :param person_id:   Id of the person to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the person requested
    director = Director.query.filter(Director.director_id == director_id).one_or_none()

    # Did we find a person?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {director_id} deleted", 200)

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {director_id}")