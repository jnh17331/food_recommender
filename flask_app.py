import os
import pymongo
from flask import Flask, render_template, jsonify, request
from bson import json_util

app = Flask(__name__)

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.preferences  = {}
        self.liked_recipes = []
        self.disliked_recipes = []

    def update_prefences(self, preferences):
        self.preferences.update(preferences)

    def add_liked_recipe(self, recipe_id):
        self.liked_recipes.append(recipe_id)

    def add_disliked_recipe(self, recipe_id):
        self.disliked_recipes.append(recipe_id)

class Recipe:
    def __init__(self, recipe_id, recipe_name, minutes, tags, ingredients, rating):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.minutes = minutes
        self.tags = tags
        self.ingredients = ingredients
        self.rating = rating
        

client = pymongo.MongoClient("localhost", 27017)
recipe_db = client.food_rec
recipe_collection = recipe_db.recipes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recipes', methods=['GET'])
def recipes():
    try:

        # Sets limit on call for production, change here and in recipe_list variable if needed
        default_limit = 100
        limit = int(request.args.get('limit', default_limit))

        recipe_list = json_util.dumps(list(recipe_collection.find().limit(limit)))

        return jsonify(recipe_list)
    
    except Exception as e:

        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)