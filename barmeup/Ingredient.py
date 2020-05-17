from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    name: str
    cost: float = 1
    usage_speed: float = 1
    is_already_present: bool = False


@dataclass(frozen=True)
class Drink:
    name: str
    ingredients: [Ingredient]