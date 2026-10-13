"""Efficiency test for Plant Information.

This builds fake gardens (half plants, half flowers), then times how long
the program takes to read and print them. Printed output goes into
memory instead of the screen, so the screen does not slow the
measurement down. Each timing is the best of 3 runs.
"""

import contextlib
import io
import os
import random
import sys
import time
import tracemalloc


def load_program():
    """Add plant_program/ to Python's search path, then import from it.

    The imports are inside this function on purpose, so an auto-formatter
    cannot move them above the line that adds the folder to the path.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, 'plant_program'))
    from flower import Flower
    from main import create_plant, print_list
    return Flower, create_plant, print_list


Flower, create_plant, print_list = load_program()

SIZES = [1_000, 10_000, 100_000, 1_000_000]
RUNS = 3


def make_lines(n, seed=5010):
    """Fake input: every other line is a flower. Fixed seed = same data every run."""
    rng = random.Random(seed)
    lines = []
    for i in range(n):
        cost = rng.randint(1, 50)
        if i % 2:
            annual = rng.choice(['true', 'false'])
            lines.append(f'flower F{i} {cost} {annual} red')
        else:
            lines.append(f'plant P{i} {cost}')
    return lines


def best_time(task):
    """Run task() RUNS times and return the fastest time in seconds."""
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        task()
        times.append(time.perf_counter() - start)
    return min(times)


def quiet(task):
    """Run task() with its print output sent to memory, not the screen."""
    with contextlib.redirect_stdout(io.StringIO()):
        task()


# Three ways to print the same garden, for the comparison
def print_polymorphic(garden):
    print_list(garden)                     # the program's own design


def print_isinstance(garden):
    for i, p in enumerate(garden, start=1):
        print(f'Plant {i} Information:')
        print(f'   Plant name: {p.plant_name}')
        print(f'   Cost: {p.plant_cost}')
        if isinstance(p, Flower):
            print(f'   Annual: {p.is_annual}')
            print(f'   Color of flowers: {p.color_of_flowers}')
        print()


def print_one_string(garden):
    parts = []
    for i, p in enumerate(garden, start=1):
        parts.append(f'Plant {i} Information:\n'
                     f'   Plant name: {p.plant_name}\n'
                     f'   Cost: {p.plant_cost}\n')
        if isinstance(p, Flower):
            parts.append(f'   Annual: {p.is_annual}\n'
                         f'   Color of flowers: {p.color_of_flowers}\n')
        parts.append('\n')
    sys.stdout.write(''.join(parts))


def main():
    args = sys.argv[1:]

    if args and args[0] == '--sample':
        count = int(args[1]) if len(args) > 1 else 8
        for line in make_lines(count):
            print(line)
        return

    if args and args[0] == '--quick':
        SIZES[:] = [1_000, 10_000, 100_000]

    print(f'Python {sys.version.split()[0]}  ·  best of {RUNS} runs\n')
    print(f'{"Items N":>10} {"Read (s)":>10} {"Print (s)":>10} '
          f'{"µs per item":>12} {"bytes/object":>13}')

    garden = []
    for n in SIZES:
        lines = make_lines(n)
        garden = []

        def read():
            garden.clear()
            garden.extend(create_plant(line) for line in lines)

        read_s = best_time(read)
        print_s = best_time(lambda: quiet(lambda: print_list(garden)))

        tracemalloc.start()
        objects = [create_plant(line) for line in lines]
        used, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        del objects

        per_item = (read_s + print_s) / n * 1e6
        print(f'{n:>10,} {read_s:>10.4f} {print_s:>10.3f} '
              f'{per_item:>12.1f} {used / n:>13.0f}')

    print(f'\nPrinting {len(garden):,} items, three designs:')
    for label, design in [('Polymorphic print_info() (ours)', print_polymorphic),
                          ('isinstance() if/else', print_isinstance),
                          ('Build one string, write once', print_one_string)]:
        seconds = best_time(lambda: quiet(lambda: design(garden)))
        print(f'  {label:<34} {seconds:.2f} s')


if __name__ == '__main__':
    main()
