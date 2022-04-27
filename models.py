from datetime import datetime
from config import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = 'directors'

    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    gender= db.Column(db.Integer)
    uid= db.Column(db.Integer)
    department= db.Column(db.Text)

    movies = db.relationship(    #Person.notes
        'Movie',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='asc(Movie.movie_id)'
    )

    # def __str__(self):
    #     return f'{self.person_id} {self.fname} {self.lname} {self.timestamp}'

class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'))
    original_title = db.Column(db.Text)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Text)
    revenue = db.Column(db.Integer)
    title = db.Column(db.Text)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.Text)
    tagline = db.Column(db.Text)
    uid = db.Column(db.Integer)
    

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        # sqla_session = db.session
        load_instance = True

    movies = fields.Nested('DirectorMovieSchema', default=[], many=True)

class DirectorMovieSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    movie_id = fields.Int()
    director_id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    

class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        # sqla_session = db.session
        load_instance = True

    directors = fields.Nested("MovieDirectorSchema", default=None)


class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    director_id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()