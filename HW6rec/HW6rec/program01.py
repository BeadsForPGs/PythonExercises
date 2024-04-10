# -*- coding: utf-8 -*-
'''
The Caponians, an alien strain coming from an unspecified planet in
the galaxy, have been planning for quite a while the invasion of the
planet Earth. To do this, they have created and installed in various
points of the planet "mind bending machines". This machinery reduces
the intelligence of humans through the telephone network [1].

Once the phase of reducing human intelligence is over, the next
step towards the conquest of the Earth will be the landing on our
planet, which will happen as soon as the Caponians will find some
areas where they can land with their spaceships.

A spaceship (seen from above) can be represented as a rectangle of
dimensions W (width) and H (height). When considering the necessary
space for landing, a spaceship will open hatches on the 4 sides of
the rectangle. These gates are one per side.

The areas protrude by the same amount D, in order to allow to open on
each side a landing hatch. Each hatch is therefore as wide as the side
of the spaceship on which it is located and long as D, whatever side
it is on.

The Caponians would like to land with their spaceships in some of our
cities by looking at the city map. A city can be represented as a black
rectangular image, in which every building is represented as a colored
rectangle (each building has a color that uniquely identifies it).

In order to define the final details of the landing plan, the Caponians
need an algorithm which, given a map of a city and a
list of spaceships, confirms or not if
each spaceship has enough space to land in that city.
To land, a spaceship has to open its 4 hatches. Spaceships do not land
in the city at the same time, so they must be evaluated separately
from each other.

(1) So, given a black image (city) filled with solid colored
rectangles (buildings), where each building has its own unique color,
it is necessary:

- determine position, size and color of each rectangle
- save in a text file one rectangle per line
- in the file, each rectangle is represented with a sequence of 7 values:
     x, y, w, h, r, g, b
  separated by commas, in order of decreasing y-coordinate (the row
  nunber). In case of equal y, in order of increasing x (row-pixel number).

(2) Next, we are given a text file containing N triple of
integers. Each triple is separated internally and from the other
triples by a variable number of spaces, tabs or carriage returns. Each
triple represents width W, height H and minimum distance D (see below)
of a spaceship that you would like to land in a city at step (1):

- So we have to return a list of N Boolean values: the i-th value in
the list is True if there is enough space in the image to
insert the i-th spaceship.

- a rectangle can be inserted in the image if there exists at least
one position in the image where there is enough space (i.e., an area
consisting entirely of black pixels) to hold the i-th spaceship.
A spaceship can land if contains the rectangle itself, plus the 4
"extensions" of the rectangle, i.e. the 4 hatches of the spaceship.

For example, if a spaceship has 2 pixels of width and 3 of height and
D = 2, we will have to look for an area in the image to contain the
following figure:

                              **
                              **
                            **++**
                            **++**
                            **++**
                              **
                              **

where the + symbols are the pixels of the 2x3 rectangle/spaceship and the *
are the pixels of the 4 extensions/hatches.

Example:
Given the following image represented with one character for each
pixel, where "." is a black pixel and characters other than "." are
colored pixels (*=red, +=green):

**....
**....
......
......
....++
....++

The file with the found rectangles  must contain the lines:
4,4,2,2,0,255,0
0,0,2,2,255,0,0

and given the following spaceships:

(3, 3, 0)
(2, 2, 4)
(1, 1, 3)
(4, 2, 1)
(2, 4, 1)

the returned list will be: [True, False, False, False, False].
In fact only the first spaceship can land for example in the zone marked by
'X' (it has no doors, in fact D = 0)

**.XXX
**.XXX
...XXX
......
....++
....++

while the others don't enter in the map because, even if they have a point
in which they can land, they cannot open all the hatches.


[1] https://en.wikipedia.org/wiki/Zak_McKracken_and_the_Alien_Mindbenders)
'''

from pngmatrix import load_png8


def ex(image_path, spacecraft_data, output_path):
    # Load the city map image
    city_map = load_png8(image_path)

    # Detect and catalog buildings within the city map
    building_info = detect_buildings(city_map)

    # Document detected buildings into a specified file
    document_buildings(building_info, output_path)

    # Load spacecraft dimensions and requirements
    spacecraft_specs = load_spacecraft_specs(spacecraft_data)

    # Determine feasible landing zones for each spacecraft
    landing_feasibility = assess_landing_zones(city_map, spacecraft_specs)

    return landing_feasibility


def detect_buildings(image):
    buildings = []
    img_height, img_width = len(image), len(image[0])
    seen_pixels = [[False for _ in range(img_width)] for _ in range(img_height)]

    for row in range(img_height):
        for col in range(img_width):
            if not seen_pixels[row][col] and image[row][col] != (0, 0, 0):
                current_color = image[row][col]
                width, height = 1, 1

                # Expand to the right
                while col + width < img_width and image[row][col + width] == current_color:
                    width += 1
                # Expand downwards
                while row + height < img_height and all(
                        image[row + height][col + offset] == current_color for offset in range(width)):
                    height += 1

                # Mark pixels as seen
                for dy in range(height):
                    for dx in range(width):
                        seen_pixels[row + dy][col + dx] = True

                buildings.append((col, row, width, height, current_color[0], current_color[1], current_color[2]))

    return buildings


def document_buildings(building_data, file_path):
    # Sort buildings for output consistency
    sorted_buildings = sorted(building_data, key=lambda b: (-b[1], b[0]))

    with open(file_path, 'w') as file:
        for building in sorted_buildings:
            file.write(','.join(map(str, building)) + '\n')


def load_spacecraft_specs(file_path):
    spacecraft_list = []
    with open(file_path, 'r') as file:
        data = file.read().split()

    # Convert data to integer triples
    specs = [int(value) for value in data if value.isdigit()]

    for i in range(0, len(specs), 3):
        if i + 2 < len(specs):
            spacecraft_list.append((specs[i], specs[i + 1], specs[i + 2]))

    return spacecraft_list


def assess_landing_zones(image, spacecrafts):
    possible_landings = []
    for craft in spacecrafts:
        craft_width, craft_height, hatch_extension = craft
        landing_matrix = create_landing_matrix(craft_height, craft_width, hatch_extension)
        extended_width = craft_width + 2 * hatch_extension
        extended_height = craft_height + 2 * hatch_extension

        for row in range(len(image) - extended_height + 1):
            for col in range(len(image[0]) - extended_width + 1):
                if check_landing_space(image, col, row, craft_width, craft_height, hatch_extension, landing_matrix):
                    possible_landings.append(True)
                    break
            else:
                continue
            break
        else:
            possible_landings.append(False)

    return possible_landings


def create_landing_matrix(height, width, extension):
    hatch_row = " " * extension + "*" * width + " " * extension
    core_row = "*" * (width + 2 * extension)
    matrix = [hatch_row] * extension + [core_row] * height + [hatch_row] * extension
    return matrix


def check_landing_space(image, x, y, width, height, extension, matrix):
    img_height, img_width = len(image), len(image[0])
    for dy in range(y, y + height + 2 * extension):
        for dx in range(x, x + width + 2 * extension):
            if image[dy][dx] != (0, 0, 0) and matrix[dy - y][dx - x] != " ":
                return False
    return True


if __name__ == "__main__":
    print(ex("HW6rec/images/image9.png", "HW6rec/rectangles/rectangles9.txt", "output.txt"))


