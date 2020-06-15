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

# Example:
# > python nomk.py -c 37.0 55.0
# > python nomk.py -n "N-37-100"

import argparse
import math

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
roman_figures = [['XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI'],
                 ['XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX'],
                 ['XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV'], 
                 ['XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII'], 
                 ['VII', 'VIII', 'IX', 'X', 'XI', 'XII'],
                 ['I', 'II', 'III', 'IV', 'V', 'VI']]
ru_letters = [['В', 'Г'],
              ['А', 'Б']]
ru_letters_lower = [['в', 'г'],
                    ['а', 'б']]              
ru_letters_small = [['ж', 'з', 'и'],
                    ['г', 'д', 'е'],
                    ['а', 'б', 'в']]         


# https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%80%D0%B0%D0%B7%D0%B3%D1%80%D0%B0%D1%84%D0%BA%D0%B8_%D0%B8_%D0%BD%D0%BE%D0%BC%D0%B5%D0%BD%D0%BA%D0%BB%D0%B0%D1%82%D1%83%D1%80%D1%8B_%D1%82%D0%BE%D0%BF%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D0%BA%D0%B0%D1%80%D1%82

# https://meganorm.ru/Data2/1/4293849/4293849307.htm
# На районы, ограниченные параллелями 60 и 76° северной и южной широт, листы карт издаются сдвоенными по долготе, а в пределах 76 - 84° - счетверенными, за исключением карты масштаба 1:200000, листы которой издаются строенными по долготе
# Номенклатуры листов карт масштабов 1:500000, 1:200000 и 1:100000 слагаются из номенклатуры листа карты масштаба 1:1000000 с последующим добавлением обозначений листов карт соответствующих масштабов. Номенклатуры листов карт масштабов 1:50000, 1:25000 и 1:10000 слагаются из номенклатуры листа карты масштаба 1:100000 с последующим добавлением обозначений листов карт соответствующих масштабов. Номенклатуры сдвоенных, строенных или счетверенных листов содержат обозначения всех отдельных листов.

# Например, номенклатуры листов топографических карт для северного полушария будут иметь вид:
# 1:1000000                 N-37                            Р-47, 48                    Т-45, 46, 47, 48
# 1:500000                   N-37-Б                         Р-47-А, Б                  Т-45-А, Б, 46-А, Б
# 1:200000                   N-37-IV                       P-47-I, II                   T-47-I, II, III
# 1:100000                   N-37-12                       P-47-9, 10                 Т-47-133, 134, 135, 136
# 1:50000                     N-37-12-А                   Р-47, 9-А, Б              Т-47-133-А, Б, 134-А, Б
# 1:25000                     N-37-12-A-a               Р-47-9-А-а, б           Т-47-12-А-а, б, Б-а, б
# 1:10000                     N-37-12-A-a-1            P-47-9-A-a-1, 2        Т-47-12-А-а-1, 2, б-1, 2

def coordsTo1m(x, y):
    abs_y = abs(y)

    if abs_y >= 88.0:
        return 'Z', -180.0, 180.0, 88.0, 90.0

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

    if y < 0:
        return '{}-{}(ЮП)'.format(letters[row], col_str), min_x, max_x, -min_y, -max_y
    return '{}-{}'.format(letters[row], col_str), min_x, max_x, min_y, max_y

def get1M(x, y):
    col = int(math.floor(x / 6.0))
    min_x = col * 6.0
    row = int(math.floor(y / 4.0))
    min_y = math.floor(row * 4.0)

    return col + 31, row, min_x, min_y

def coordsTo500k(x, y):
    abs_y = abs(y)
    col, row, min_x, min_y = get1M(x, abs_y)
    letter = ''

    # TODO: Add quad sheets

    if abs_y > 60.0: # Create double sheets
        if abs_y > min_y + 2.0:
            letter = 'А,Б'
            min_y + 2.0
        else: 
            letter = 'В,Г'
        max_x = min_x + 6.0
    else:
        pos_x = int(math.floor(abs(x - min_x) / 3.0))
        pos_y = int(math.floor((abs_y - min_y) / 2.0))
        
        # TODO: Fix for south
        if y < 0: pos_y = abs(1 - pos_y)
        letter = ru_letters[pos_y][pos_x]

        min_x = min_x + pos_x * 3.0
        min_y = min_y + pos_y * 2.0

        max_x = min_x + 3.0

    max_y = min_y + 2.0

    if y < 0:
        return '{}-{}-{}(ЮП)'.format(letters[row], col, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}-{}'.format(letters[row], col, letter), min_x, max_x, min_y, max_y


def coordsTo200k(x, y):
    abs_y = abs(y)
    col, row, min_x, min_y = get1M(x, abs_y)
    letter = ''
    size_x = 6.0 / 6
    size_y = 4.0 / 6

    row_200k = int(math.floor((abs_y - min_y) / size_y))
    col_200k = int(math.floor(abs(x - min_x) / size_x))

    # TODO: Fix for south
    if y < 0: row_200k = abs(5 - row_200k)

    if abs_y > 76.0: # Create triple sheets
        begin_col = math.floor(col_200k / 3) * 3
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(3):
            if letter == '':
                letter = '{}'.format(roman_figures[row_200k][begin_col + i])
            else: 
                letter = letter + ',{}'.format(roman_figures[row_200k][begin_col + i])
            max_x = max_x + size_x

    elif abs_y > 60.0 and abs_y <= 76.0: # Create double sheets
        begin_col = math.floor(col_200k / 2) * 2
        min_x = min_x + begin_col
        max_x = min_x
        for i in range(2):
            if letter == '':
                letter = '{}'.format(roman_figures[row_200k][begin_col + i])
            else: 
                letter = letter + ',{}'.format(roman_figures[row_200k][begin_col + i])
            max_x = max_x + size_x
    else:
        letter = roman_figures[row_200k][col_200k]

        min_x = min_x + col_200k
        min_y = min_y + row_200k * size_y
    
        max_x = min_x + size_x

    max_y = min_y + size_y

    if y < 0:
        return '{}-{}-{}(ЮП)'.format(letters[row], col, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}-{}'.format(letters[row], col, letter), min_x, max_x, min_y, max_y


def get_grid_pos(x, y, min_x, min_y, parts):
    size_x = 6.0 / parts
    size_y = 4.0 / parts

    row = int(math.floor((y - min_y) / size_y))
    col = int(math.floor(abs(x - min_x) / size_x))

    min_x = min_x + col * size_x
    min_y = min_y + row * size_y
    
    max_x = min_x + size_x
    max_y = min_y + size_y

    return row, col, min_x, max_x, min_y, max_y

def coordsTo100k(x, y, simple=False):

    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.

    abs_y = abs(y)
    col, row, min_x, min_y = get1M(x, abs_y)

    row_100k, col_100k, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 12)
    
    # TODO: Fix for south
    if y < 0: row_100k = abs(1 - row_100k)

    letter = (11 - row_100k) * 12 + col_100k + 1

    if y < 0:
        return '{}-{}-{}(ЮП)'.format(letters[row], col, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}-{}'.format(letters[row], col, letter), min_x, max_x, min_y, max_y


def coordsTo50k(x, y):

    # TODO: Fix for south
    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.

    abs_y = abs(y)
    nomk, min_x, max_x, min_y, max_y = coordsTo100k(x, y)

    row, col, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 24)
    
    # TODO: Fix for south
    if y < 0: row = abs(1 - row)
        
    letter = ru_letters[row][col]

    if y < 0:
        return '{}-{}(ЮП)'.format(nomk, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}'.format(nomk, letter), min_x, max_x, min_y, max_y

def coordsTo25k(x, y):

    # TODO: Fix for south
    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.

    abs_y = abs(y)
    nomk, min_x, max_x, min_y, max_y = coordsTo50k(x, abs_y)
    row, col, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 48)

    letter = ru_letters_lower[row][col]

    if y < 0:
        return '{}-{}(ЮП)'.format(nomk, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}'.format(nomk, letter), min_x, max_x, min_y, max_y

def coordsTo10k(x, y):

    # TODO: Fix for south
    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.
    
    abs_y = abs(y)
    nomk, min_x, max_x, min_y, max_y = coordsTo25k(x, abs_y)
    row, col, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 96)

    letter = (1 - row) * 2 + col + 1

    if y < 0:
        return '{}-{}(ЮП)'.format(nomk, letter), min_x, max_x, -min_y, -max_y
    return '{}-{}'.format(nomk, letter), min_x, max_x, min_y, max_y

def coordsTo5k(x, y, simple=False):

    # TODO: Fix for south
    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.

    abs_y = abs(y)
    nomk, min_x, max_x, min_y, max_y = coordsTo100k(x, abs_y)
    row, col, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 192)

    letter = (15 - row) * 16 + col + 1

    if simple:
        return '{}({}'.format(nomk, letter), min_x, max_x, min_y, max_y

    if y < 0:
        return '{}({})(ЮП)'.format(nomk, letter), min_x, max_x, -min_y, -max_y
    return '{}({})'.format(nomk, letter), min_x, max_x, min_y, max_y

def coordsTo2k(x, y):

    # TODO: Fix for south
    # TODO: Add double and quad sheets - ru: Севернее 60° с.ш. и южнее 60° ю.ш. карты сдвоены, севернее 76° с.ш. и южнее 76° ю.ш. счетверены.

    abs_y = abs(y)
    nomk, min_x, max_x, min_y, max_y = coordsTo5k(x, abs_y, True)
    row, col, min_x, max_x, min_y, max_y = get_grid_pos(x, abs_y, min_x, min_y, 576)

    letter = ru_letters_small[row][col]

    if y < 0:
        return '{}-{})(ЮП)'.format(nomk, letter), min_x, max_x, -min_y, -max_y
    return '{}-{})'.format(nomk, letter), min_x, max_x, min_y, max_y    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform coordinates to nomenclature and vice versa')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('-c', '--coord2nomk', required='True', help='Transform coordinates (longtitude latitude) to nomenclature.', type=float, nargs=2, metavar=('X', 'Y'))
    parser.add_argument('-n', '--nomk2coord', help='Transform nomenclature to coordinates', dest='nomk')

    args = parser.parse_args()

    X = Y = None
    if args.coord2nomk:
        X = args.coord2nomk[0]
        Y = args.coord2nomk[1]

    if X is not None and Y is not None:
        if X > 180.0 or X < -180.0 or Y > 90.0 or Y < -90.0:
            exit('Coordinates are out of bounds')
        
        #1 : 1 000 000
        nomk, min_x, max_x, min_y, max_y = coordsTo1m(X, Y)
        print('1 : 1 000 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 500 000
        nomk, min_x, max_x, min_y, max_y = coordsTo500k(X, Y)
        print('1 : 500 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 200 000
        nomk, min_x, max_x, min_y, max_y = coordsTo200k(X, Y)
        print('1 : 200 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 100 000
        nomk, min_x, max_x, min_y, max_y = coordsTo100k(X, Y)
        print('1 : 100 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 50 000
        nomk, min_x, max_x, min_y, max_y = coordsTo50k(X, Y)
        print('1 : 50 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 25 000
        nomk, min_x, max_x, min_y, max_y = coordsTo25k(X, Y)
        print('1 : 25 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 10 000
        nomk, min_x, max_x, min_y, max_y = coordsTo10k(X, Y)
        print('1 : 10 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 5 000
        nomk, min_x, max_x, min_y, max_y = coordsTo5k(X, Y)
        print('1 : 5 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
        #1 : 2 000
        nomk, min_x, max_x, min_y, max_y = coordsTo2k(X, Y)
        print('1 : 2 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))

        
    if args.nomk is not None:
        # TODO:
        exit(1)


    