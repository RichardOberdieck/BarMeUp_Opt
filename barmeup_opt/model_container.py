import mip
from .domain_models import Drink, Ingredient


class ModelContainer:
    """
    The container for all the optimization-specific items
    """
    def __init__(self):
        self.model = mip.Model("BarMeUp", solver_name=mip.CBC)

    def create_ingredient_purchase_variable(self, ingredients):
        """
        The variable identifying which ingredient should be bought.
        :param ingredients: The ingredients for the cocktail
        """
        self.x = {i: self.model.add_var(var_type=mip.BINARY) for i in ingredients}

    def create_drink_available_variable(self, drinks):
        """
        The variable identifying which drinks are available to be made.
        :param drinks: The drinks to be made
        """
        self.y = {d: self.model.add_var(var_type=mip.BINARY) for d in drinks}

    def create_ingredient_available_variable(self, ingredients):
        """
        The variable identifying which ingredients are available to be made.
        :param ingredients: The ingredients for the cocktail
        """
        self.z = {i: self.model.add_var(var_type=mip.BINARY) for i in ingredients}

    def create_ingredient_already_present_variable(self, ingredients):
        """
        The variable identifying which ingredients are already present
        :param ingredients: The ingredients for the cocktail
        """
        self.p = {i: self.model.add_var(var_type=mip.BINARY) for i in ingredients}

    def set_objective(self, ingredients):
        """
        The objective function
        :param ingredients: The ingredients for the cocktail
        """
        self.model.objective = mip.minimize(mip.xsum(self.x[i] for i in ingredients))

    def enforce_ingredients_in_drink(self, d: Drink):
        """
        Making sure that all ingredients are present for a drink d
        :param d: The drink for which the constraint is enforced
        """
        self.model.add_constr(mip.xsum(self.x[i] for i in d.ingredients) >= len(d.ingredients)*self.y[d],
                              name=f'Enforce ingredients present for drink {d.name}')

    def enforce_ingredients_purchase_available_link(self, i: Ingredient):
        """
        Ensuring that an ingredient needs to be either purchased or already present in order to be used for a drink
        :param i: The ingredient in question
        """
        self.model.add_constr(self.z[i] - self.x[i] - self.p[i] == 0,
                              name=f'Enforce ingredients are either purchased or available for {i.name}')

    def enforce_number_of_drinks_makeable(self, drinks, n):
        """
        Make sure that we can make the specified number of drinks
        :param drinks: All drinks considered
        :param n: The number of drinks to be made
        """
        self.model.add_constr(mip.xsum(self.y[d] for d in drinks) >= n, name="Enforce number of drinks makeable")

    def enforce_existing_ingredients(self, i: Ingredient):
        """
        Linking the information whether an ingredient is already present to the corresponding variable.
        :param i: The ingredient in question
        """
        self.model.add_constr(self.p[i] == i.is_already_present, name=f'Check whether ingredient {i.name} is present')

    def solve(self):
        """
        Solving the problem
        :return: List of drinks available to be made, List of ingredients needed to purchase
        """
        self.model.optimize()
        drinks_available = [d for d in self.y if self.y[d].x > 0.5]
        ingredients_to_purchase = [i for i in self.x if self.x[i].x > 0.5]
        return drinks_available, ingredients_to_purchase
