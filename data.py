import db
import json

def get_recipe(recipe_id):
    return db.session.query(db.Recipe).get(recipe_id)

def get_recipes_for_user(user_id):
    return db.session.query(db.Recipe).filter(db.Recipe.user_id==user_id).order_by(db.Recipe.created_at.desc()).all()

def get_recipes_for_users(user_ids):
    return db.session.query(db.Recipe).filter(db.Recipe.user_id.in_(user_ids)).order_by(db.Recipe.created_at.desc()).all()

def new_recipe(title, user_id, ingredients, steps, id=None, fork_of=None):
    data = db.RecipeData(ingredients=ingredients, steps=steps)
    db.session.add(data)
    db.session.flush()
    recipe = db.Recipe(title=title, user_id=user_id, data=data)
    db.session.add(recipe)
    db.session.flush()
    return recipe

def fork_recipe(user_id, recipe_id):
    recipe = db.session.query(db.Recipe).get(recipe_id)
    fork = db.Recipe(title=recipe.title, user_id=user_id, data=recipe.data)
    db.session.add(fork)
    db.session.flush()
    return fork

def update_recipe(recipe_id, ingredients=None, steps=None):
    recipe = db.session.query(db.Recipe).get(recipe_id)
    data = db.RecipeData(ingredients=ingredients, steps=steps, parent_id=recipe.data.id)
    db.session.add(data)
    db.session.flush()
    db.session.query(db.Recipe).filter_by(id=recipe_id).update({"data_id": data.id})
    db.session.flush()
    return get_recipe(recipe.id)

def get_versions(recipe_id):
    data_tip_id = db.session.query(db.Recipe).get(recipe_id).data_id
    included_parts = db.session.query(db.RecipeData).\
                     filter(db.RecipeData.id==data_tip_id).\
                     cte(name='included_parts', recursive=True)

    incl_alias = db.aliased(included_parts, name="pr")
    parts_alias = db.aliased(db.RecipeData, name='p')
    included_parts = included_parts.union_all(
        db.session.query(parts_alias).filter(parts_alias.id==incl_alias.c.parent_id)
    )

    return db.session.query(included_parts).filter(db.RecipeData.id==data_tip_id).all()
