#Тесты_для_всех_классов
import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_init():
    i = Ingredient("мука", 500, "г")
    assert i.name == "мука"
    assert i.quantity == 500.0
    assert i.unit == "г"

def test_ingredient_eq():
    i1 = Ingredient("сахар", 100, "г")
    i2 = Ingredient("сахар", 200, "г")
    i3 = Ingredient("соль", 100, "г")
    assert i1 == i2
    assert i1 != i3

def test_ingredient_negative():
    with pytest.raises(ValueError):
        Ingredient("вода", -5, "мл")

def test_recipe_add_merge():
    r = Recipe("тест")
    r.add_ingredient(Ingredient("яйцо", 2, "шт"))
    r.add_ingredient(Ingredient("яйцо", 3, "шт"))
    assert len(r.ingredients) == 1
    assert r.ingredients[0].quantity == 5

def test_recipe_scale():
    r = Recipe("пирог", [Ingredient("мука", 100, "г")])
    r2 = r.scale(2)
    assert r2.ingredients[0].quantity == 200.0
    assert r.ingredients[0].quantity == 100.0

def test_shopping_sum():
    sl = ShoppingList()
    sl.add_recipe(Recipe("А", [Ingredient("мука", 100, "г")]), 1)
    sl.add_recipe(Recipe("Б", [Ingredient("мука", 50, "г")]), 2)
    res = sl.get_list()
    assert res[0].quantity == 200.0

def test_dietary_scale_type():
    dr = DietaryRecipe("салат", "веган", [Ingredient("огурец", 1, "шт")])
    dr2 = dr.scale(3)
    assert isinstance(dr2, DietaryRecipe)
    assert dr2.diet_type == "веган"
