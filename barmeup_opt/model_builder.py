from .model_container import ModelContainer


class ModelBuilder:
    """
    Building the model to solve this problem.
    """
    def __init__(self, drinks, n):
        self.drinks = drinks
        self.ingredients = set(i for d in drinks for i in d.ingredients)
        self.n = n
        self.model = ModelContainer(self.ingredients, self.drinks)

    def _create_variables(self):
        """
        Creating the variables
        """
        self.model.create_drink_available_variable()
        self.model.create_ingredient_already_present_variable()
        self.model.create_ingredient_available_variable()
        self.model.create_ingredient_purchase_variable()

    def _add_constraints(self):
        """
        Adding the constraints
        """
        for d in self.drinks:
            self.model.enforce_ingredients_in_drink(d)

        for i in self.ingredients:
            self.model.enforce_ingredients_purchase_available_link(i)
            self.model.enforce_existing_ingredients(i)

        self.model.enforce_number_of_drinks_makeable(self.n)

    def solve(self):
        """
        Solving the problem
        """
        self._create_variables()
        self._add_constraints()

        self.model.set_objective()
        return self.model.solve()
