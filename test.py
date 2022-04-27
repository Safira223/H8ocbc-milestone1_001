from unittest import result
from urllib import requests
from models import Movie
import unittest
import json
import app
from app import connex_app


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/api/ui/"
    MOVIES_URL = "{}/movies".format(API_URL)
    movie = {
            "movie_id : 43597",
            "original_title : Avatar"
            "budget : 237000000"
            "popularity : 150"
            "release_date : 2009-12-10"
            "revenue : 2787965087"
            "title : Avatar"
            "vote_average : 7.2"
            "vote_count : 11800",
            "overview : In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
            "tagline : Enter the World of Pandora."
            "uid : 19995"      
    }
    
    def test_1_get_all_movies(self):
        r = requests.get(ApiTest.MOVIES_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
        
    def test_2_add_new_movie(self):
        r = requests.post(ApiTest.MOVIES_URL, json=ApiTest.movie)
        self.assertEqual(r.status_code, 201)
        
    def test_3_get_new_movie(self):
        movie_id = 43597
        r = requests.get("{}/{}".format(ApiTest.MOVIES_URL, movie_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.movie)
        
    def test_6_delete_movie(self):
        movie_id = 43597
        r = requests.delete()

if __name__ == '__main__':
    unittest.main()