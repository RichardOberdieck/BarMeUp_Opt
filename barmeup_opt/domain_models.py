from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    name: str
    cost: float = 1
    shelf_life: float = 1
    is_already_present: bool = False


@dataclass(frozen=True)
class Drink:
    name: str
    ingredients: [Ingredient]

    def __hash__(self):
        return self.name.__hash__() + len(self.ingredients) + sum(i.__hash__() for i in self.ingredients)

