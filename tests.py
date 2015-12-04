import unittest
import db
import json
from datetime import datetime
from data import new_recipe, fork_recipe, update_recipe, get_versions
from api import app

test_client = app.test_client()

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean()


class TestWithData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        clean()
        insert_all()


def clean():
    db.session.close()
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)


class NewRecipe(Test):
    def test_new_recipe(self):
        recipe = new_recipe(**sunny_side_up)
        self.assertEqual(db.session.query(db.Recipe).count(), 1)
        self.assertEqual(db.session.query(db.RecipeData).count(), 1)


class ForkRecipe(Test):
    def test_recipe_fork(self):
        recipe = new_recipe(**sunny_side_up)
        fork = fork_recipe(2, recipe.id)
        self.assertEqual(db.session.query(db.Recipe).count(), 2)
        self.assertEqual(db.session.query(db.RecipeData).count(), 1)


class UpdateRecipe(Test):

    def test_update_recipe(self):
        recipe = new_recipe(**sunny_side_up)
        update_recipe(recipe.id, ingredients=sunny_side_up_v2['ingredients'], steps=sunny_side_up_v2['steps'])
        self.assertEqual(db.session.query(db.Recipe).count(), 1)
        self.assertEqual(db.session.query(db.RecipeData).count(), 2)
        recipe = db.session.query(db.Recipe).first()
        self.assertIn("cheese", recipe.data.ingredients)


class UpdateRecipeParent(Test):

    def test_parent_data(self):
        recipe = new_recipe(**sunny_side_up)
        old_data_id = recipe.data.id
        update_recipe(recipe.id, ingredients=sunny_side_up_v2['ingredients'], steps=sunny_side_up_v2['steps'])
        self.assertEquals(recipe.data.parent.id, old_data_id)


class GetVersions(TestWithData):

    def test_versions(self):
        recipe = db.session.query(db.Recipe).filter_by(title='Sunny side up').first()
        self.assertEqual(len(get_versions(recipe.id)), 2)

class CheckTimestamp(TestWithData):

    def test_recipe_timestamp(self):
        recipe = db.session.query(db.Recipe).filter_by(title='Sunny side up').first()
        self.assertEqual(recipe.created_at.date(), datetime.today().date())

    def test_recipe_data_timestamp(self):
        recipe = db.session.query(db.Recipe).filter_by(title='Sunny side up').first()
        self.assertEqual(recipe.data.created_at.date(), datetime.today().date())

# API!

class Ping(unittest.TestCase):
    def test_ping(self):
        resp = json.loads(test_client.get('/ping').data)
        self.assertIn("pong", resp)

class TestGetRecipe(TestWithData):
    pass


# Test Data

sunny_side_up = {
    # "id": 1,
    "title": "Sunny side up",
    "user_id": 1,
    "fork_of": None,
    "ingredients": {
        "canola_oil": 1,  # one tbsp oil
        "salt": None,     # to taste
        "eggs": 2,        # two eggs
        "hot_sauce": None # to taste
    },
    "steps": [
        "Heat oil in a pan",
        "Break eggs and put them",
        "Add salt and close the lid",
        "Once done serve in plate and put hot sauce"
    ]
}

sunny_side_up_v2 = {
    # "id": 1,
    "title": "Sunny side up",
    "user_id": 1,
    "fork_of": None,
    "ingredients": {
        "canola_oil": 1,  # one tbsp oil
        "salt": None,     # to taste
        "eggs": 2,        # two eggs
        "cheese": 2 # to taste
    },
    "steps": [
        "Heat oil in a pan",
        "Break eggs and put them in the pan",
        "sprinkle cheese on the eggs",
        "Add salt and close the lid",
        "Once done serve in plate"
    ]
}

begun_bhaja = {
    "title": "Begun Bhaja",
    "user_id": 1,
    "fork_of": None,
    "ingredients": {
        "egg_plant": 1,  # one tbsp oil
        "canola_oil": 2,        # two eggs
        "salt": None,     # to taste
        "chilli_powder": 2 # to taste
    },
    "steps": [
        "Slice egg plants",
        "Heat oil in a pan",
        "Place slices in the oil",
        "sprinkle salt and chilli powder",
        "Flip the slices and fry the other side",
        "Serve on a plate with paper towel"
    ]
}

def insert_all():
        recipe = new_recipe(**sunny_side_up)
        update_recipe(recipe.id, ingredients=sunny_side_up_v2['ingredients'], steps=sunny_side_up_v2['steps'])
        new_recipe(**begun_bhaja)

if __name__ == '__main__':
    unittest.main()
