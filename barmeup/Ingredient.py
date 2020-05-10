from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Ingredient:
    name: str
    cost: float = 1
    availability: Availability = Availability.HIGH
    usage_speed: float = 1
    is_already_present: bool = False


@dataclass(frozen=True)
class Drink:
    name: str
    ingredients: [Ingredient]
    tools: [Tool]


class Availability(Enum):
    HIGH = 1,
    MEDIUM = 2,
    LOW = 3


class Tool(Enum):
    SHAKER = 1
