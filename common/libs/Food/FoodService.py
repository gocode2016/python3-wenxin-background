from common.models.food.Food import Food


def getFoodInfo(food_id):
    return Food.query.filter_by(id=food_id).first()