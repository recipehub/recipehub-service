import unittest
import db
from data import new_recipe, fork_recipe, update_recipe

def clean():
    db.session.close()
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)

class NewRecipe(unittest.TestCase):
    def setUp(self):
        clean()

    def test_new_recipe(self):
        recipie = new_recipe(**sunny_side_up)
        self.assertEqual(db.session.query(db.Recipie).count(), 1)
        self.assertEqual(db.session.query(db.RecipieData).count(), 1)

class ForkRecipe(unittest.TestCase):
    def setUp(self):
        clean()

    def test_recipe_fork(self):
        recipie = new_recipe(**sunny_side_up)
        fork = fork_recipe(2, recipie.id)
        self.assertEqual(db.session.query(db.Recipie).count(), 2)
        self.assertEqual(db.session.query(db.RecipieData).count(), 1)

class UpdateRecipe(unittest.TestCase):
    def setUp(self):
        clean()

    def test_update_recipe(self):
        recipie = new_recipe(**sunny_side_up)
        update_recipe(recipie.id, ingredients=sunny_side_up_v2['ingredients'], steps=sunny_side_up_v2['steps'])
        self.assertEqual(db.session.query(db.Recipie).count(), 1)
        self.assertEqual(db.session.query(db.RecipieData).count(), 2)
        recipe = db.session.query(db.Recipie).first()
        self.assertIn("cheese", recipie.data.ingredients)

    def test_parent_data(self):
        recipie = new_recipe(**sunny_side_up)
        old_data_id = recipie.data.id
        update_recipe(recipie.id, ingredients=sunny_side_up_v2['ingredients'], steps=sunny_side_up_v2['steps'])
        self.assertEquals(recipie.data.parent.id, old_data_id)



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

if __name__ == '__main__':
    unittest.main()
