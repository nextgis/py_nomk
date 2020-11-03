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
 
import pytest
import coord
import util
import text

delta = 0.00000001

def test_1m():
    is_south = False
    letter = 'N'
    zone = 37

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_1m(37.61556, 55.75222)
    
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_1m(letter, zone, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '1m'
    assert nomk_str == 'N-37'

    is_south = True

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_1m(37.61556, -55.75222)
    
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_1m(letter, zone, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '1m'
    assert nomk_str == u'N-37' + util.south_suffix()

def test_500k():
    is_south = False
    letter = 'N'
    zone = 37
    last_letter = u'А'

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_500k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_500k(letter, zone, last_letter, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '500k'
    assert nomk_str == u'N-37-А'

    is_south = True

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_500k(37.61556, -55.75222)
    last_letter = u'В'
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_500k(letter, zone, last_letter, is_south)

    assert min_x1 - min_x2 < delta
    assert max_x1 - max_x2 < delta
    assert min_y1 - min_y2 < delta
    assert max_y1 - max_y2 < delta

    assert scale == '500k'
    assert nomk_str == u'N-37-В' + util.south_suffix()

def test_200k():
    is_south = False
    letter = 'N'
    zone = 37
    last_letter = u'II'

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_200k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_200k(letter, zone, last_letter, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '200k'
    assert nomk_str == u'N-37-II'

    is_south = True

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_200k(37.61556, -55.75222)
    last_letter = u'XXXII'
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_200k(letter, zone, last_letter, is_south)

    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '200k'
    assert nomk_str == u'N-37-XXXII' + util.south_suffix()

def test_100k():
    is_south = False
    letter = 'N'
    zone = 37
    last_letter = 4

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_100k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_100k(letter, zone, last_letter, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '100k'
    assert nomk_str == u'N-37-004'

def test_50k():
    is_south = False
    letter = 'N'
    zone = 37
    last_number = 4
    last_letter = u'В'

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_50k(letter, zone, last_number, last_letter, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '50k'
    assert nomk_str == u'N-37-004-В'

def test_25k():
    is_south = False
    letter = 'N'
    zone = 37
    last_number = 4
    letter2 = u'В'
    last_letter = u'а'

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_25k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_25k(letter, zone, last_number, letter2, last_letter, is_south)
    # print(u'{} - {},{},{},{}'.format(nomk_str, min_x1, max_x1, min_y1, max_y1))
    # print(u'{} - {},{},{},{}'.format(scale, min_x2, max_x2, min_y2, max_y2))
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '25k'
    assert nomk_str == u'N-37-004-В-а'
