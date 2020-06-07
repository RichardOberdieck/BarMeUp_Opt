import mip
from .Ingredient import Drink, Ingredient


class ModelContainer:
    def __init__(self, ingredients, drinks):
        self.model = mip.Model("BarMeUp", solver_name=mip.CBC)
        self.ingredients = ingredients
        self.drinks = drinks

    def create_ingredient_purchase_variable(self):
        self.x = {i: self.model.add_var(var_type=mip.BINARY) for i in self.ingredients}

    def create_drink_available_variable(self):
        self.y = {d: self.model.add_var(var_type=mip.BINARY) for d in self.drinks}

    def create_ingredient_available_variable(self):
        self.z = {i: self.model.add_var(var_type=mip.BINARY) for i in self.ingredients}

    def create_ingredient_already_present_variable(self):
        self.p = {i: self.model.add_var(var_type=mip.BINARY) for i in self.ingredients}

    def set_objective(self):
        self.model.objective = mip.minimize(mip.xsum(self.x[i] for i in self.ingredients))

    def enforce_ingredients_in_drink(self, d: Drink):
        self.model.add_constr(mip.xsum(self.x[i] for i in d.ingredients) >= len(d.ingredients)*self.y[d],
                              name=f'Enforce ingredients present for drink {d.name}')

    def enforce_ingredients_purchase_available_link(self, i: Ingredient):
        self.model.add_constr(self.z[i] - self.x[i] - self.p[i] == 0,
                              name=f'Enforce ingredients are either purchased or available for {i.name}')

    def enforce_number_of_drinks_makeable(self, n):
        self.model.add_constr(mip.xsum(self.y[d] for d in self.drinks) >= n, name="Enforce number of drinks makeable")

    def enforce_existing_ingredients(self, i: Ingredient):
        self.model.add_constr(self.p[i] == i.is_already_present, name=f'Check whether ingredient {i.name} is present')

    def solve(self):
        self.model.optimize()
        drinks_available = [d for d in self.drinks if self.y[d].x > 0.5]
        ingredients_to_purchase = [i for i in self.ingredients if self.x[i].x > 0.5]
        return drinks_available, ingredients_to_purchase
