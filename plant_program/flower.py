from plant import Plant


class Flower(Plant):
    """Derived class: a Flower IS A Plant, plus annual status and flower color."""

    def __init__(self, plant_name, plant_cost, is_annual, color_of_flowers):
        super().__init__(plant_name, plant_cost)
        self.is_annual = is_annual
        self.color_of_flowers = color_of_flowers

    def print_info(self):
        super().print_info()
        print(f'   Annual: {self.is_annual}')
        print(f'   Color of flowers: {self.color_of_flowers}')
