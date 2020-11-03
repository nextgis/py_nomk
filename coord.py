# -*- coding: utf-8 -*-
################################################################################
# Project:  Topomaps nomenclature utility
# Purpose:  Transform coordinates to nomenclature and vice versa
# Author:   Dmitry Barishnikov, dmitry.baryshnikov@nextgis.ru
# Version: 0.1
################################################################################
# Copyright (C) 2020, NextGIS <info@nextgis.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import math
import util


def get_1m(x, y):
    col = int(math.floor(x / 6.0))
    min_x = col * 6.0
    row = int(math.floor(y / 4.0))
    min_y = math.floor(row * 4.0)

    return col + 31, row, min_x, min_y

def coords_to_1m(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)

    if abs_y >= 88.0:
        return 'Z', -180.0, 180.0, 88.0 * mult, 90.0 * mult

    row = int(math.floor(abs(y) / 4.0))
    min_y = math.floor(row * 4.0)

    col_str = ''
    
    max_y = min_y + 4.0
    min_x = max_x = 0.0

    if abs_y < 88.0 and abs_y > 76.0: # Create quad sheets
        new_x = x + 180
        col = int(math.floor(new_x / 24.0))
        min_x = col * 24.0 - 180.0
        col = col * 4
        max_x = min_x

        for i in range(4):
            if col_str == '':
                col_str = '{}'.format(col + 1 + i)
            else: 
                col_str = col_str + ',{}'.format(col + 1 + i)
            max_x = max_x + 6.0

    elif abs_y < 76.0 and abs_y > 60.0: # Create double sheets    
        new_x = x + 180    
        col = int(math.floor(new_x / 12.0))
        min_x = col * 12.0 - 180.0
        col = col * 2
        max_x = min_x

        for i in range(2):
            if col_str == '':
                col_str = '{}'.format(col + 1 + i)
            else: 
                col_str = col_str + ',{}'.format(col + 1 + i)
            max_x = max_x + 6.0

    else:
        col = int(math.floor(x / 6.0))
        min_x = col * 6.0
        col_str = '{}'.format(col + 31)
        max_x = min_x + 6.0

    nomk_str = u'{}-{}'.format(util.letters[row], col_str)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y * mult, max_y * mult

def coords_to_500k(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)
    col, row, min_x, min_y = get_1m(x, abs_y)
    letter = ''
    col_str = u''

    if abs_y > 88.0:
        raise Exception('Unsupported latitude ({:.6f}) for this scale'.format(y))
    elif abs_y > 76.0: # Create quad sheets
        if abs_y > min_y + 2.0:
            letter = util.get_row_ru(1, y < 0)
            min_y + 2.0
        else: 
            letter = util.get_row_ru(0, y < 0)

        if col % 2 == 0:
            col_str = u'{}-{},{}-{}'.format(col - 1, letter, col, letter)
            min_x -= 6
        else:
            col_str = u'{}-{},{}-{}'.format(col, letter, col + 1, letter)
        max_x = min_x + 12.0
        
    elif abs_y < 76.0 and abs_y > 60.0: # Create double sheets    
        if abs_y > min_y + 2.0:
            letter = util.get_row_ru(1, y < 0)
            min_y + 2.0
        else: 
            letter = util.get_row_ru(0, y < 0)
        max_x = min_x + 6.0
        col_str = u'{}={}'.format(col, letter)
    else:
        local_col = int(math.floor(abs(x - min_x) / 3.0))
        local_row = int(math.floor((abs_y - min_y) / 2.0))
        letter = util.get_letter_ru(local_col, local_row, y < 0)

        min_x = min_x + local_col * 3.0
        min_y = min_y + local_row * 2.0

        max_x = min_x + 3.0

        col_str = u'{}-{}'.format(col, letter)

    max_y = min_y + 2.0

    nomk_str = u'{}-{}'.format(util.letters[row], col_str)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y * mult, max_y * mult

def coords_to_200k(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)
    col, row, min_x, min_y = get_1m(x, abs_y)
    letter = ''
    size_x = 6.0 / 6
    size_y = 4.0 / 6

    row_200k = int(math.floor((abs_y - min_y) / size_y))
    col_200k = int(math.floor(abs(x - min_x) / size_x))

    if abs_y > 88.0:
        raise Exception('Unsupported latitude ({:.6f}) for this scale'.format(y))
    elif abs_y > 76.0: # Create triple sheets
        begin_col = math.floor(col_200k / 3) * 3
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(3):
            if letter == '':
                letter = util.get_letter_roman(begin_col + i, row_200k, y < 0)
            else: 
                letter = letter + ',{}'.format(util.get_letter_roman(begin_col + i, row_200k, y < 0))
            max_x = max_x + size_x

    elif abs_y > 60.0 and abs_y <= 76.0: # Create double sheets
        begin_col = math.floor(col_200k / 2) * 2
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(2):
            if letter == '':
                letter = util.get_letter_roman(begin_col + i, row_200k, y < 0)
            else: 
                letter = letter + ',{}'.format(util.get_letter_roman(begin_col + i, row_200k, y < 0))
            max_x = max_x + size_x
    else:
        letter = util.get_letter_roman(col_200k, row_200k, y < 0)

        min_x = min_x + col_200k
        min_y = min_y + row_200k * size_y
    
        max_x = min_x + size_x

    max_y = min_y + size_y

    nomk_str = u'{}-{}-{}'.format(util.letters[row], col, letter)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y * mult, max_y * mult

def coords_to_100k_simple(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)

    col, row, min_x, min_y = get_1m(x, abs_y)
    row_100k, col_100k, size_x, size_y, min_x, max_x, min_y, max_y = util.get_grid_pos(x, abs_y, min_x, min_y, 12, y < 0)
    letter = util.letters[row]
    last_num = util.get_letter_num(col_100k, row_100k, y < 0)
    return letter, col, last_num, min_x, min_y * mult

def coords_to_50k_simple(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)
    
    letter, number, last_number, min_x, min_y = coords_to_100k_simple(x, y)
    row_50k, col_50k, size_x_50k, size_y_50k, min_x_50k, max_x_50k, min_y_50k, max_y_50k = util.get_grid_pos(x, abs_y, min_x, min_y, 24, y < 0)

    letter_str = util.get_letter_ru(col_50k, row_50k, y < 0)
    return letter, number, last_number, letter_str, min_x_50k, min_y_50k * mult

def coords_to_100k(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)
    col, row, min_x, min_y = get_1m(x, abs_y)

    row_100k, col_100k, size_x, size_y, min_x, max_x, min_y, max_y = util.get_grid_pos(x, abs_y, min_x, min_y, 12, y < 0)

    letter_str = ''

    if abs_y > 88.0:
        raise Exception('Unsupported latitude ({:.6f}) for this scale'.format(y))
    elif abs_y > 76.0: # Create quad sheets
        begin_col = math.floor(col_100k / 4) * 4
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(4):
            if letter_str == '':
                letter_str = '{:03d}'.format(util.get_letter_num(begin_col + i, row_100k, y < 0))
            else: 
                letter_str = letter_str + ',{:03d}'.format(util.get_letter_num(begin_col + i, row_100k, y < 0))
            max_x = max_x + size_x
    elif abs_y > 60.0 and abs_y <= 76.0: # Create double sheets
        begin_col = math.floor(col_100k / 2) * 2
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(2):
            if letter_str == '':
                letter_str = '{:03d}'.format(util.get_letter_num(begin_col + i, row_100k, y < 0))
            else: 
                letter_str = letter_str + ',{:03d}'.format(util.get_letter_num(begin_col + i, row_100k, y < 0))
            max_x = max_x + size_x
    else:
        letter_str = '{:03d}'.format(util.get_letter_num(col_100k, row_100k, y < 0))

    nomk_str = u'{}-{}-{}'.format(util.letters[row], col, letter_str)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y * mult, max_y * mult

def coords_to_50k(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)
    
    letter, number, last_number, min_x, min_y = coords_to_100k_simple(x, y)
    row_50k, col_50k, size_x_50k, size_y_50k, min_x_50k, max_x_50k, min_y_50k, max_y_50k = util.get_grid_pos(x, abs_y, min_x, min_y, 24, y < 0)

    col_str = ''
    min_x = min_x_50k
    max_x = max_x_50k

    if abs_y > 88.0:
        raise Exception('Unsupported latitude ({:.6f}) for this scale'.format(y))
    elif abs_y > 76.0: # Create quad sheets
        letter_str = util.get_row_ru(row_50k, y < 0)
        if last_number % 2 == 0:
            col_str = u'{:03d}-{},{:03d}-{}'.format(last_number - 1, letter_str, last_number, letter_str)
            min_x -= size_x_50k * 2
        else:
            col_str = u'{:03d}-{},{:03d}-{}'.format(last_number, letter_str, last_number + 1, letter_str)
        max_x = min_x + size_x_50k * 4
    elif abs_y > 60.0 and abs_y <= 76.0: # Create double sheets
        letter_str = util.get_row_ru(row_50k, y < 0)
        col_str = u'{:03d}-{}'.format(last_number, letter_str)
        max_x = min_x + size_x_50k * 2
    else:
        letter_str = util.get_letter_ru(col_50k, row_50k, y < 0)
        col_str = u'{:03d}-{}'.format(last_number, letter_str)

    nomk_str = u'{}-{}-{}'.format(letter, number, col_str)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y_50k * mult, max_y_50k * mult

def coords_to_25k(x, y):
    mult = 1
    if y < 0:
        mult = -1

    abs_y = abs(y)

    letter, number, last_number, last_letter, min_x, min_y = coords_to_50k_simple(x, y)
    row_25k, col_25k, size_x_25k, size_y_25k, min_x_25k, max_x_25k, min_y_25k, max_y_25k = util.get_grid_pos(x, abs_y, min_x, min_y, 48, y < 0)

    pos_x, pos_y = util.get_pos_ru(last_letter, y < 0)

    col_str = ''
    min_x = min_x_25k
    max_x = max_x_25k

    if abs_y > 88.0:
        raise Exception('Unsupported latitude ({:.6f}) for this scale'.format(y))
    elif abs_y > 76.0: # Create quad sheets
        letter_str = util.get_row_ru(row_25k, y < 0).lower()
        if pos_x % 2 == 0:
            last_letter1 = util.get_letter_ru(pos_x - 1, pos_y, y < 1)
            last_letter2 = util.get_letter_ru(pos_x, pos_y, y < 1)
            col_str = u'{}-{},{}-{}'.format(last_letter1, letter_str, last_letter2, letter_str)
            min_x -= size_x_25k * 2
        else:
            last_letter1 = util.get_letter_ru(pos_x, pos_y, y < 1)
            last_letter2 = util.get_letter_ru(pos_x + 1, pos_y, y < 1)
            col_str = u'{}-{},{}-{}'.format(last_letter1, letter_str, last_letter2, letter_str)
        max_x = min_x + size_x_25k * 4
    elif abs_y > 60.0 and abs_y <= 76.0: # Create double sheets
        letter_str = util.get_row_ru(row_25k, y < 0).lower()
        col_str = u'{}-{}'.format(last_letter, letter_str)
        max_x = min_x + size_x_25k * 2
    else:
        letter_str = util.get_letter_ru(col_25k, row_25k, y < 0).lower()
        col_str = u'{}-{}'.format(last_letter, letter_str)

    nomk_str = u'{}-{}-{:03d}-{}'.format(letter, number, last_number, col_str)
    if y < 0:
        nomk_str += util.south_suffix()
    return nomk_str, min_x, max_x, min_y_25k * mult, max_y_25k * mult