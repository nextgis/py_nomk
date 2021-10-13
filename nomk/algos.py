from typing import Tuple, List

from . import parser
from . import text
from . import coord


nomk_parse_funcs = {
    '1m': parser.parse1m,
    '500k': parser.parse500k,
    '200k': parser.parse200k,
    '100k': parser.parse100k,
    '50k': parser.parse50k,
    '25k': parser.parse25k,
    '10k': parser.parse10k,
    '5k': parser.parse5k,
    '2k': parser.parse2k,
}

nomk_text_funcs = {
    '1m': text.text_to_1m,
    '500k': text.text_to_500k,
    '200k': text.text_to_200k,
    '100k': text.text_to_100k,
    '50k': text.text_to_50k,
    '25k': text.text_to_25k,
    '10k': text.text_to_10k,
    '5k': text.text_to_5k,
    '2k': text.text_to_2k,
}

coords_to_funcs = {
    '1m': coord.coords_to_1m,
    '500k': coord.coords_to_500k,
    '200k': coord.coords_to_200k,
    '100k': coord.coords_to_100k,
    '50k': coord.coords_to_50k,
    '25k': coord.coords_to_25k,
    '10k': coord.coords_to_10k,
    '5k': coord.coords_to_5k,
    '2k': coord.coords_to_2k,
}


def get_neighbors_for_nomk(nomk: str, scale: str = None) -> Tuple[str]:
    if scale is None:
        scale, parts, is_south = parser.parse(nomk)
    else:
        parts, is_south = nomk_parse_funcs[scale](nomk)

    _, min_x, max_x, min_y, max_y = nomk_text_funcs[scale](*parts, is_south)

    width = max_x - min_x
    height = max_y - min_y
    center_x = min_x + width / 2
    center_y = min_y + height / 2

    neighbor_centers = [
        (center_x - width, center_y - height),
        (center_x - width, center_y),
        (center_x - width, center_y + height),
        (center_x, center_y - height),
        (center_x, center_y + height),
        (center_x + width, center_y - height),
        (center_x + width, center_y),
        (center_x + width, center_y + height),
    ]

    nomks = []
    for x, y in neighbor_centers:
        nomen, _, _, _, _ = coords_to_funcs[scale](x, y)
        nomks.append(nomen)

    return tuple(nomks)


def get_neighbors(nomks: List[str], scale: str = None) -> Tuple[str]:
    neighbor_nomks = ()

    for nomk in nomks:
        neighbor_nomks += get_neighbors_for_nomk(nomk, scale)

    return tuple(set(neighbor_nomks).difference(nomks))
