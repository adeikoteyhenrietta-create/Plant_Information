from plant import Plant
from flower import Flower


def print_list(my_garden):
    """Print every Plant or Flower in the list using its own print_info()."""
    for i, plant in enumerate(my_garden, start=1):
        print(f'Plant {i} Information:')
        plant.print_info()
        print()


def create_plant(line):
    """Turn one input line into a Plant or Flower. Raises ValueError if the line is invalid."""
    tokens = line.split()
    plant_type = tokens[0].lower()

    if plant_type == 'plant':
        if len(tokens) != 3:
            raise ValueError('A plant needs: plant <name> <cost>')
    elif plant_type == 'flower':
        if len(tokens) != 5:
            raise ValueError(
                'A flower needs: flower <name> <cost> <annual> <color>')
    else:
        raise ValueError(
            f"Unknown type '{tokens[0]}'. Use 'plant' or 'flower'.")

    name = tokens[1]
    try:
        cost = int(tokens[2])
    except ValueError:
        raise ValueError(f"Cost must be a whole number, got '{tokens[2]}'.")
    if cost < 0:
        raise ValueError('Cost cannot be negative.')

    if plant_type == 'plant':
        return Plant(name, cost)

    is_annual = tokens[3].lower()
    if is_annual not in ('true', 'false'):
        raise ValueError("Annual must be 'true' or 'false'.")
    return Flower(name, cost, is_annual, tokens[4])


def main():
    my_garden = []

    while True:
        try:
            user_input = input().strip()
        except EOFError:              # input ended without -1
            break

        if user_input == '-1':
            break
        if user_input == '':          # skip blank lines
            continue

        try:
            my_garden.append(create_plant(user_input))
        except ValueError as error:
            print(f'Error: {error}')

    print_list(my_garden)


if __name__ == '__main__':
    main()
