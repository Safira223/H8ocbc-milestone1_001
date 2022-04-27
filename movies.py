"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Director, Movie, MovieSchema


def read_all():
    """
    This function responds to a request for /api/people/notes
    with the complete list of notes, sorted by note timestamp
    :return:                json list of all notes for all people
    """
    # Query the database for all the notes
    movies = Movie.query.order_by(db.asc(Movie.movie_id)).limit(3).all()

    # Serialize the list of notes from our data
    movie_schema = MovieSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def read_one(director_id, movie_id):
    """
    This function responds to a request for
    /api/people/{person_id}/notes/{note_id}
    with one matching note for the associated person
    :param person_id:       Id of person the note is related to
    :param note_id:         Id of the note
    :return:                json string of note contents
    """
    # Query the database for the note
    movie = (
        Movie.query.join(Director, Director.director_id == Movie.director_id)
        .filter(Director.director_id == director_id)
        .filter(Movie.movie_id == movie_id)
        .one_or_none()
    )

    # Was a note found?
    if movie is not None:
        movie_schema = MovieSchema()
        data = movie_schema.dump(movie)
        return data

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def create(director_id, movie):
    """
    This function creates a new note related to the passed in person id.
    :param person_id:       Id of the person the note is related to
    :param note:            The JSON containing the note data
    :return:                201 on success
    """
    # get the parent person
    director = Director.query.filter(Director.director_id == director_id).one_or_none()

    # Was a person found?
    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    # Create a note schema instance
    schema = MovieSchema()
    new_movie = schema.load(movie, session=db.session)

    # Add the note to the person and database
    director.movies.append(new_movie)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_movie)

    return data, 201


def update(director_id, movie_id, movie):
    """
    This function updates an existing note related to the passed in
    person id.
    :param person_id:       Id of the person the note is related to
    :param note_id:         Id of the note to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_movie = (
        Movie.query.join(Director, Director.director_id == Movie.director_id)
        .filter(Director.director_id == director_id)
        .filter(Movie.movie_id == movie_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_movie is not None:

        # turn the passed in note into a db object
        schema = MovieSchema()
        update = schema.load(movie, session=db.session)

        # Set the id's to the note we want to update
        update.director_id = update_movie.director_id
        update.movie_id = update_movie.movie_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_movie)

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Note not found for Id: {movie_id}")


def delete(director_id, movie_id):
    """
    This function deletes a note from the note structure
    :param person_id:   Id of the person the note is related to
    :param note_id:     Id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    movie = (
        Movie.query.filter(Director.director_id == director_id)
        .filter(Movie.movie_id == movie_id)
        .one_or_none()
    )

    # did we find a note?
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {movie_id} deleted".format(movie_id=movie_id), 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Movie not found for Id: {movie_id}")