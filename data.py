import db
import json

def new_recipe(title, user_id, ingredients, steps, id=None, fork_of=None):
    data = db.RecipieData(ingredients=ingredients, steps=steps)
    db.session.add(data)
    db.session.flush()
    recipie = db.Recipie(title=title, user_id=user_id, data=data)
    db.session.add(recipie)
    db.session.flush()
    return recipie

def fork_recipe(user_id, recipe_id):
    recipe = db.session.query(db.Recipie).get(recipe_id)
    fork = db.Recipie(title=recipe.title, user_id=user_id, data=recipe.data)
    db.session.add(fork)
    db.session.flush()
    return fork

def update_recipe(recipe_id, ingredients=None, steps=None):
    recipe = db.session.query(db.Recipie).get(recipe_id)
    data = db.RecipieData(ingredients=ingredients, steps=steps, parent_id=recipe.data.id)
    db.session.add(data)
    db.session.flush()
    db.session.query(db.Recipie).filter_by(id=recipe_id).update({"data_id": data.id})
    db.session.flush()

def get_versions(recipe_id):
    pass
