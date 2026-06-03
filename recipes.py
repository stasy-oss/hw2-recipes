class Ingredient: # === Реализация класса Ingredient ===
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, val):
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(val)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients else []

    def add_ingredient(self, ing):
        if not isinstance(ing, Ingredient):
            raise TypeError("ожидается объект Ingredient")
        for exist in self.ingredients:
            if exist == ing:
                exist.quantity += ing.quantity
                return
        self.ingredients.append(ing)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("коэффициент должен быть числом больше нуля")
        new_ings = [Ingredient(i.name, i.quantity * ratio, i.unit) for i in self.ingredients]
        return Recipe(self.title, new_ings)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [f"рецепт: {self.title}"]
        for i in self.ingredients:
            lines.append(f" - {i}")
        return "\n".join(lines)


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title):
        self._items = [(ing, rt) for ing, rt in self._items if rt != title]

    def get_list(self):
        summary = {}
        for ing, _ in self._items:
            key = (ing.name, ing.unit)
            summary[key] = summary.get(key, 0) + ing.quantity
        result = [Ingredient(name, qty, unit) for (name, unit), qty in summary.items()]
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        merged = ShoppingList()
        merged._items = self._items + other._items
        return merged


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        parent_scaled = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, parent_scaled.ingredients)

    def __str__(self):
        base = super().__str__()
        return f"[{self.diet_type}] {self.title}\n" + "\n".join(base.split("\n")[1:])
