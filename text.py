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

import coord
import util

def text_to_1m(letter, number, is_south):
    min_x = 6.0 * (number - 31)
    min_y = 4.0 * util.letters.index(letter)

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [6 x 4]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_1m(min_x + 3.0, (min_y + 2.0) * mult)
    return '1m', min_x, max_x, min_y, max_y

def text_to_500k(letter, number, last_letter, is_south):
    col, row = util.get_pos_ru(last_letter, is_south)
    
    min_x = 6.0 * (number - 31)
    min_x += 3.0 * col
    
    min_y = 4.0 * util.letters.index(letter)
    min_y += 2.0 * row

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [3 x 2]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_500k(min_x + 1.5, (min_y + 1.0) * mult)
    return '500k', min_x, max_x, min_y, max_y

def text_to_200k(letter, number, last_letter, is_south):
    col, row = util.get_pos_roman(last_letter, is_south)

    min_x = 6.0 * (number - 31)
    min_x += 1.0 * col

    min_y = 4.0 * util.letters.index(letter)
    min_y += 4.0 / 6 * row

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [1 x 0.6666]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_200k(min_x + 0.5, (min_y + 0.3) * mult)
    return '200k', min_x, max_x, min_y, max_y

def text_to_100k(letter, number, last_letter, is_south):
    col, row = util.get_pos_num(last_letter, is_south)

    min_x = 6.0 * (number - 31)
    min_x += 0.5 * col

    min_y = 4.0 * util.letters.index(letter)
    min_y += 4.0 / 12 * row

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [0.5 x 0.3333]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_100k(min_x + 0.25, (min_y + 0.16) * mult)
    return '100k', min_x, max_x, min_y, max_y

def text_to_50k(letter, number, last_number, last_letter, is_south):
    col, row = util.get_pos_num(last_number, is_south)

    min_x = 6.0 * (number - 31)
    min_x += 0.5 * col

    min_y = 4.0 * util.letters.index(letter)
    min_y += 4.0 / 12 * row

    col_50k, row_50k = util.get_pos_ru(last_letter, is_south)

    min_x += 0.25 * col_50k
    min_y += 4.0 / 24 * row_50k

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [0.25 x 0.1666]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_50k(min_x + 0.125, (min_y + 0.083) * mult)
    return '50k', min_x, max_x, min_y, max_y


def text_to_25k(letter, number, number2, letter2, last_letter, is_south):
    col, row = util.get_pos_num(number2, is_south)

    min_x = 6.0 * (number - 31)
    min_x += 0.5 * col

    min_y = 4.0 * util.letters.index(letter)
    min_y += 4.0 / 12 * row

    col_50k, row_50k = util.get_pos_ru(letter2, is_south)

    min_x += 0.25 * col_50k
    min_y += 4.0 / 24 * row_50k

    col_25k, row_25k = util.get_pos_ru(last_letter.upper(), is_south)

    min_x += 0.125 * col_25k
    min_y += 4.0 / 48 * row_25k

    mult = 1
    if is_south:
        mult = -1

    # Get bbox by some point in sheet [0.125 x 0.0833]
    nomk, min_x, max_x, min_y, max_y = coord.coords_to_25k(min_x + 0.0625, (min_y + 0.042) * mult)
    return '25k', min_x, max_x, min_y, max_y
