class Plant:
    """Base class: every plant has a name and a cost."""

    def __init__(self, plant_name, plant_cost):
        self.plant_name = plant_name
        self.plant_cost = plant_cost

    def print_info(self):
        print(f'   Plant name: {self.plant_name}')
        print(f'   Cost: {self.plant_cost}')
