# -*- coding: utf-8 -*-
################################################################################
# Project: Topomaps nomenclature utility
# Purpose: Transform coordinates to nomenclature and vice versa
# Author:  Dmitry Baryshnikov, dmitry.baryshnikov@nextgis.ru
# Version: 0.1
################################################################################
# Copyright (C) 2020-2021, NextGIS <info@nextgis.com>
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
import parser
import text
import coord

if __name__ == "__main__":
    parser_obj = argparse.ArgumentParser(description='Transform coordinates to nomenclature and vice versa')
    parser_obj.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser_obj.add_argument('-c', '--coord2nomk', help='Transform coordinates (longtitude latitude) to nomenclature.', type=float, nargs=2, metavar=('X', 'Y'))
    parser_obj.add_argument('-n', '--nomk2coord', help='Transform nomenclature to coordinates', dest='nomk')
    parser_obj.add_argument('-s', '--scale', help='Override map scale in nomk2coord', dest='scale', choices=['1m', '500k', '200k', '100k', '50k', '25k', '10k', '5k', '2k' ])

    args = parser_obj.parse_args()

    X = Y = None
    if args.coord2nomk:
        X = args.coord2nomk[0]
        Y = args.coord2nomk[1]

    if X is not None and Y is not None:
        if X > 180.0 or X < -180.0 or Y > 90.0 or Y < -90.0:
            exit('Coordintates out of bounds')
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_1m(X, Y)
        print(u'1 : 1 000 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_500k(X, Y)
        print(u'1 : 500 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_200k(X, Y)
        print(u'1 : 200 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_100k(X, Y)
        print(u'1 : 100 000\t{}\t\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_50k(X, Y)
        print(u'1 : 50 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_25k(X, Y)
        print(u'1 : 25 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_10k(X, Y)
        print(u'1 : 10 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_5k(X, Y)
        print(u'1 : 5 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        nomk, min_x, max_x, min_y, max_y = coord.coords_to_2k(X, Y)
        print(u'1 : 2 000\t{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(nomk, min_x, min_y, max_x, max_y))
        
    if args.nomk is not None:
        scale, parts, is_south = parser.parse(args.nomk, args.scale)
        if scale == '1m':
            scale, min_x, max_x, min_y, max_y = text.text_to_1m(parts[0], parts[1], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '500k':
            scale, min_x, max_x, min_y, max_y = text.text_to_500k(parts[0], parts[1], parts[2], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '200k':
            scale, min_x, max_x, min_y, max_y = text.text_to_200k(parts[0], parts[1], parts[2], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '100k':
            scale, min_x, max_x, min_y, max_y = text.text_to_100k(parts[0], parts[1], parts[2], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '50k':
            scale, min_x, max_x, min_y, max_y = text.text_to_50k(parts[0], parts[1], parts[2], parts[3], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '25k':
            scale, min_x, max_x, min_y, max_y = text.text_to_25k(parts[0], parts[1], parts[2], parts[3], parts[4], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '10k':
            scale, min_x, max_x, min_y, max_y = text.text_to_10k(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '5k':
            scale, min_x, max_x, min_y, max_y = text.text_to_5k(parts[0], parts[1], parts[2], parts[3], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        elif scale == '2k':
            scale, min_x, max_x, min_y, max_y = text.text_to_2k(parts[0], parts[1], parts[2], parts[3], parts[4], is_south)
            print('{}\t[{:.6f} {:.6f}, {:.6f} {:.6f}]'.format(scale, min_x, min_y, max_x, max_y))
            exit(0)
        else:
            exit('Unrecognized nomenclature')
