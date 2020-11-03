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

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ru_letters = [u'А', u'Б', u'В', u'Г']
roman_figures = ['I', 'II', 'III', 'IV', 'V', 'VI', 
    'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
    'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII',
    'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV',
    'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX', 
    'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI']
        
ru_letters_small = [['ж', 'з', 'и'],
                    ['г', 'д', 'е'],
                    ['а', 'б', 'в']]

def south_suffix():
    return u'(ЮП)'

def get_pos_ru(letter, is_south):
    pos = ru_letters.index(letter)
    row = int(math.floor(pos / 2))
    col = pos - row * 2

    if not is_south:
        row = 1 - row
    return col, row

def get_row_ru(row, is_south):
    if is_south:
        if row == 0:
            return u'А,Б'
        else:
            return u'В,Г'
    else:
        if row == 0:
            return u'В,Г'
        else:
            return u'А,Б'

def get_letter_ru(col, row, is_south):
    if not is_south:
        row = 1 - row
    index = row * 2 + col
    return ru_letters[index]

def get_pos_roman(letter, is_south):
    pos = roman_figures.index(letter)
    row = int(math.floor(pos / 6))
    col = pos - row * 6

    if not is_south:
        row = 5 - row
    return col, row

def get_letter_roman(col, row, is_south):
    if not is_south:
        row = 5 - row
    index = row * 6 + col
    return roman_figures[index]

def get_pos_num(number, is_south):
    row = int(math.floor(number / 12))
    col = number - row * 12 - 1

    if not is_south:
        row = 11 - row
    return col, row

def get_letter_num(col, row, is_south):
    if not is_south:
        row = 11 - row
    index = row * 12 + col + 1 # index starts from 1
    return int(index)

def get_grid_pos(x, y, min_x, min_y, parts, is_south):
    size_x = 6.0 / parts
    size_y = 4.0 / parts

    row = int(math.floor((y - min_y) / size_y))
    col = int(math.floor(abs(x - min_x) / size_x))

    min_x = min_x + col * size_x
    min_y = min_y + row * size_y
    
    max_x = min_x + size_x
    max_y = min_y + size_y

    if is_south:
        row = parts - 1 - row

    return row, col, size_x, size_y, min_x, max_x, min_y, max_y

