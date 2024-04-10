import images


def count_divisions(image, left, top, right, bottom, background, hierarchy):
    left_freq = {}
    right_freq = {}
    top_freq = {}
    bottom_freq = {}

    for x in range(left, right):
        pixel_color = image[top][x]
        pixel_color1 = image[bottom - 1][x]
        if pixel_color != background:
            top_freq[pixel_color] = top_freq.get(pixel_color, (0, None))[0] + 1, x
        if pixel_color1 != background:
            bottom_freq[pixel_color1] = bottom_freq.get(pixel_color1, (0, None))[0] + 1, x

    for y in range(top, bottom):
        pixel_color = image[y][left]
        pixel_color1 = image[y][right - 1]
        if pixel_color != background:
            left_freq[pixel_color] = left_freq.get(pixel_color, (0, None))[0] + 1, y
        if pixel_color1 != background:
            right_freq[pixel_color1] = right_freq.get(pixel_color1, (0, None))[0] + 1, y



    dominant_color = None
    division_x, division_y = None, None
    for color, (count, coord) in left_freq.items():
        if count == 1 and right_freq.get(color, (0, None))[0] == 1:
            if top_freq.get(color, (0, None))[0] == 1 and bottom_freq.get(color, (0, None))[0] == 1:
                if right_freq[color][1] == coord and top_freq[color][1] == bottom_freq[color][1]:
                    dominant_color = color
                    division_x = top_freq[color][1]
                    division_y = coord
                    break

    if not dominant_color:
        return 1

    patch_count = 0
    hierarchy.append(dominant_color)

    sub_regions = [(division_x + 1, division_y + 1, right, bottom), (left, division_y + 1, division_x, bottom),
                   (division_x + 1, top, right, division_y), (left, top, division_x, division_y)]

    for sub_left, sub_top, sub_right, sub_bottom in sub_regions:
        patch_count += count_divisions(image, sub_left, sub_top, sub_right, sub_bottom, background, hierarchy)

    return patch_count


def ex1(input_path, output_path):
    image = images.load(input_path)
    background_color = image[-1][-1]
    answer_list = []
    num_patches = count_divisions(image, 0, 0, len(image[0]), len(image), background_color, answer_list)
    answer_image = [[background_color] + list(answer_list)]
    images.save(answer_image, output_path)

    return num_patches


if __name__ == '__main__':
    print(ex1('HW8rec/puzzles/medium02.in.png', 'output.png'))
