import os
from config import db
from models import Director, Movie

# Data to initialize database with
DIRECTORS = [
    {
        "name": "James Cameron",
        "gender": "2",
        "uid": "2710",
        "department": "Directing",
        "movies": [
            (
                "Avatar",
                "2009-12-10",
            ),
            (
                "Titanic",
                "1997-11-18",
            ),
        ],
    },
    {
        "name": "Gore Verbinski",
        "gender": "2",
        "uid": "1704",
        "department": "Directing",
        "movies": [
            (
                "Pirates of the Caribbean: At World's End",
                "2007-05-19",
            ),
            (
                "Pirates of the Caribbean: Dead Man's Chest",
                "2006-06-20",
            ),
            (
                "The Lone Ranger",
                "2013-07-03",
            ),
        ],
    },
    {
        "name": "Bryan Singer",
        "gender": "2",
        "uid": "9032",
        "department": "Directing",
        "movies": [
            (
                "Superman Returns",
                "2006-06-28",
            ),
            (
                "X-Men: Days of Future Past",
                "2014-05-15",
            ),
            (
                "Jack the Giant Slayer",
                "2013-02-27",
            ),
        ],
    },
]

# Delete database file if it exists currently
if os.path.exists('final_proj.db'):
    os.remove('final_proj.db')

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for director in DIRECTORS:
    d = Director(
        name=director.get("name"), 
        gender=director.get("gender"),
        uid=director.get("uid"),
        department =director.get("department")
    )

    # Add the notes for the person
    for movie in director.get("movies"):
        original_title, release_date = movie
        d.movies.append(
            Movie(
                original_title=original_title,
                release_date=release_date,
            )
        )
    db.session.add(d)

db.session.commit()