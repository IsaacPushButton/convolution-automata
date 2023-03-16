import inspect
from dataclasses import dataclass
import random
from math import sqrt
from typing import List, Optional, Callable

from const import Vec2


@dataclass
class ConvolutionFilter:
    """
    The offsets of the cells we want to use in the convolution and the values used for mulitplying them
    Must be the same length and in the same order
    """
    convolution_values: List[float]
    convolution_offsets: List[Vec2]




def make_3x1():
    return [random_float(1), random_float(1), random_float(1)]

def make_diamond_filter(width: int, hollow: int = 0):
    assert width % 2 != 0, "Width must be odd"
    offsets = []
    weights = []
    side_len = int((width - 1) / 2)
    y_rows = [i for i in range(-side_len, side_len+1)]
    y = 0
    row_length_idx = 1
    pairs = {}

    def make_diamond_row(y: int, width: int, hollow: int, weights=False) -> List[Vec2]:
        assert width % 2 != 0, "Width must be odd"
        if width == 1:
            return [(0, y)] if not weights else [generate_weight(0, y)]
        row = []
        side_len = int((width - 1) / 2)
        for i in range(-side_len, side_len + 1):
            if round(sqrt(i**2+y**2),0) < hollow:
                continue
            if weights:
                row.append(generate_weight(i, y))
            else:
                row.append((i, y))
        return row

    def new_weight(key: tuple):
        new_weight = ((random.random() - 0.5) * 2)
        pairs[key] = new_weight
        return new_weight

    def generate_weight(x, y):
        key = tuple(sorted([abs(x),abs(y)]))
        if v := pairs.get(key):
            return v
        return new_weight(key)

    while y != width - 1:
        offsets.extend(make_diamond_row(y_rows[y], row_length_idx, hollow))
        weights.extend(make_diamond_row(y_rows[y], row_length_idx, hollow, True))
        if y == width - 1:
            break
        y += 1
        row_length_idx += 2 if y <= side_len else -2
    return ConvolutionFilter(
        weights, offsets
    )

#
# def make_diamond_offset(width: int):
#     assert width % 2 != 0, "Width must be odd"
#     offsets = []
#     side_len = int((width - 1) / 2)
#     y_rows = [i for i in range(-side_len, side_len+1)]
#     row_count_idx = 0
#     row_length_idx = 1
#     while True:
#         offsets.extend(make_diamond_row(y_rows[row_count_idx], row_length_idx))
#         if row_count_idx == width - 1:
#             break
#         row_count_idx += 1
#         row_length_idx += 2 if row_count_idx <= side_len else -2
#     return offsets



OFFSET_CIRCLE_SMALL = [
        (-1, -2), (0, -2), (1, -2),
    (-2, -1),                (2, -1),
    (-2, 0),                 (2, 0),
    (-2, 1),                 (2, 1),
        (-1, 2), (0, 2), (1, 2)
]
OFFSET_CIRCLE_MID = [
              (-1, -3), (0, -3), (1,-3),
        (-2, -2),                    (2, -2),
    (-3, -1),                           (3, -1),
    (-3, 0),                            (3, 0),
    (-3, 1),                            (3, 1),
        (-2, 2),                      (2, 2),
               (-1, 3), (0, 3), (1, 3)

]

OFFSET_BULLSEYE_SMALL = [
        (-1, -2), (0, -2), (1, -2),
    (-2, -1),                (2, -1),
    (-2, 0),      (0,0),         (2, 0),
    (-2, 1),                 (2, 1),
        (-1, 2), (0, 2), (1, 2)
]
OFFSET_BULLSEYE_MID = [
              (-1, -3), (0, -3), (1,-3),
        (-2, -2),                    (2, -2),
    (-3, -1),                           (3, -1),
    (-3, 0),          (0,0),               (3, 0),
    (-3, 1),                            (3, 1),
        (-2, 2),                      (2, 2),
               (-1, 3), (0, 3), (1, 3)

]

OFFSETS_3x3 = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),  (0, 0),  (1, 0),
    (-1, 1),  (0, 1),  ( 1, 1)
]

OFFSETS_DIAMOND_OOPS = [
    (0,-2),
    (-1, -1), (0, -1), (1, -1),
    (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
    (-1, 1), (0, 1), (1, 1),
    (2, 0)
]

OFFSETS_DIAMOND_5 = make_diamond_filter(5)
OFFSETS_DIAMOND_7 = make_diamond_filter(7)
OFFSETS_DIAMOND_9 = make_diamond_filter(9)



FILTER_SIZE_CHART = {
    9 : OFFSETS_3x3,
    12: OFFSET_CIRCLE_SMALL,
    13: OFFSETS_DIAMOND_5,
    16: OFFSET_CIRCLE_MID,
    17: OFFSET_BULLSEYE_MID,
    25: OFFSETS_DIAMOND_7
}
print()











def random_float(abs_max: float) -> float:
    return ((random.random() - 0.5) * 2) * abs_max

def random_symetric_3x3(abs_max: float) -> ConvolutionFilter:
    c = random_float(abs_max)
    t = random_float(abs_max)
    m = random_float(abs_max)
    return symmetric_filter_3x3(c, t, m)

def random_symetric_diamond(abs_max: float) -> ConvolutionFilter:
    p = random_float(abs_max)
    t = random_float(abs_max)
    i = random_float(abs_max)
    m = random_float(abs_max)

    return symmetric_filter_diamond(p, t, i, m)

def random_symetric_small_circle(abs_max: float) -> ConvolutionFilter:
    p = random_float(abs_max)
    t = random_float(abs_max)
    i = random_float(abs_max)
    return symmetric_filter_small_circle(p, t, i)

def random_symetric_small_bullseye(abs_max: float) -> ConvolutionFilter:
    p = random_float(abs_max)
    t = random_float(abs_max)
    i = random_float(abs_max)
    m = random_float(abs_max)
    return symmetric_filter_small_bullseye(p, t, i, m)

def random_symetric_medium_circle(abs_max: float) -> ConvolutionFilter:
    p = random_float(abs_max)
    t = random_float(abs_max)
    i = random_float(abs_max)
    m = random_float(abs_max)
    return symmetric_filter_medium_circle(p, t, i, m)

def random_symetric_medium_bullseye(abs_max: float) -> ConvolutionFilter:
    p = random_float(abs_max)
    t = random_float(abs_max)
    i = random_float(abs_max)
    m = random_float(abs_max)
    c = random_float(abs_max)
    return symmetric_filter_medium_bullseye(p, t, i, m, c)



def random_filter(n_squares: int = 9) -> ConvolutionFilter:
    return build_filter([random_float(1) for i in range(n_squares)])

def build_filter(vals: List[float], offset: Optional[List[Vec2]] = None):
    n_squares = len(vals)
    return ConvolutionFilter(
        convolution_values=vals,
        convolution_offsets=FILTER_SIZE_CHART[n_squares] if not offset else offset
    )

def set_kwargs_default_random_float(fn):
    fn_kwargs = [p.name for p in inspect.signature(fn).parameters.values() if p.kind >= inspect.Parameter.POSITIONAL_OR_KEYWORD]
    def wrapped(*args, **kwargs):
        tmp = {k: random_float(1) for k in fn_kwargs}
        tmp.update(kwargs)
        return fn(**tmp)
    return wrapped


@set_kwargs_default_random_float
def symmetric_filter_3x3(corner: float, top: float, mid: float):
    return build_filter([
        corner,top,corner,
        top,mid,top,
        corner,top,corner
    ])

@set_kwargs_default_random_float
def symmetric_filter_diamond(point, edge, inner, mid):
    return build_filter([
        point,
        edge,inner,edge,
        point,inner,mid,inner,point,
        edge,inner,edge,
        point
    ])

@set_kwargs_default_random_float
def symmetric_filter_medium_circle(twelve, one, two, three):
    return build_filter([
         one, twelve, one,
        two,           two,
    three,               three,
    twelve,              twelve,
    three,               three,
        two,           two,
          one, twelve, one

    ])
@set_kwargs_default_random_float
def symmetric_filter_medium_bullseye(twelve, one, two, three, centre):
    return build_filter([
         one, twelve, one,
        two,           two,
    three,              three,
    twelve,   centre,  twelve,
    three,              three,
        two,           two,
          one, twelve, one

    ])

@set_kwargs_default_random_float
def symmetric_filter_small_circle(twelve, one, two):
    return build_filter([
        one, twelve, one,
        two, two,
        twelve, twelve,
        two, two,
        one, twelve, one

    ])
@set_kwargs_default_random_float
def symmetric_filter_small_bullseye(twelve, one, two, centre):
    return build_filter([
        one, twelve,    one,
        two,            two,
        twelve, centre, twelve,
        two,            two,
        one, twelve,    one

    ])