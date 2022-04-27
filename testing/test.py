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
            "movie_id : 43598",
            "original_title : Outlander"
            "budget : 938000000"
            "popularity : 223"
            "release_date : 1998-06-12"
            "revenue : 961000003"
            "title : Outlander"
            "vote_average : 8.9"
            "vote_count : 3456"
            "tagline : Best romance series ever"
            "overview : Time traveller"
            "uid : 4823"      
    }
    
    def test_1_get_all_movies(self):
        r = requests.get(ApiTest.MOVIES_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
        
    def test_2_add_new_movie(self):
        r = requests.post(ApiTest.MOVIES_URL, json=ApiTest.movie)
        self.assertEqual(r.status_code, 201)
        
    def test_3_get_new_movie(self):
        movie_id = 43598
        r = requests.get("{}/{}".format(ApiTest.MOVIES_URL, movie_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.movie)
        
    def test_6_delete_movie(self):
        movie_id = 43598
        r = requests.delete()

if __name__ == '__main__':
    unittest.main()