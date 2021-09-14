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
 
import pytest
from nomk import coord, util, text

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

    is_south = False
    letter = 'U'
    
    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_1m(37.61556, 81.75222, True)

    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_1m(letter, zone, is_south, True)   

    assert scale == '1m'
    assert nomk_str == u'U-37'

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

    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_200k(29.4643518467, 60.4127030704)
    nomk2_str, min_x2, max_x2, min_y2, max_y2 = coord.coords_to_200k(29.4643518467, 61.0793697371)

    assert nomk1_str != nomk2_str and min_y1 != min_y2 and max_y1 != max_y2

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

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_100k(31.4643518467, 60.0793697371)
    assert min_x1 < 31.4643518467 and max_x1 > 31.4643518467
    
    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_100k(58.94643518467, 76.1793697371)
    assert min_x1 < 58.94643518467 and max_x1 > 58.94643518467

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

    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(29.38, 60.0793697371)
    nomk2_str, min_x2, max_x2, min_y2, max_y2 = coord.coords_to_50k(29.15, 60.0793697371)

    assert nomk1_str == nomk2_str and min_x1 == min_x2 and max_x1 == max_x2 and min_y1 == min_y2 and max_y2 == max_y2


    # Test double sheets 
    ## First
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.20, 75.90)

    assert nomk1_str == 'S-47-003-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 97.50000000000000) < delta
    assert abs(min_y1 - 75.83333333333334) < delta
    assert abs(max_y1 - 76.00000000000000) < delta

    ## Second
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.35, 75.90)

    assert nomk1_str == 'S-47-003-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 97.50000000000000) < delta
    assert abs(min_y1 - 75.83333333333334) < delta
    assert abs(max_y1 - 76.00000000000000) < delta

    # Test quad sheets 
    ## First
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.20, 76.60)

    assert nomk1_str == 'T-47-123-А,Б,124-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 98.00000000000000) < delta
    assert abs(min_y1 - 76.50000000000000) < delta
    assert abs(max_y1 - 76.66666666666667) < delta

    ## Second
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.35, 76.60)

    assert nomk1_str == 'T-47-123-А,Б,124-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 98.00000000000000) < delta
    assert abs(min_y1 - 76.50000000000000) < delta
    assert abs(max_y1 - 76.66666666666667) < delta

    ## Third
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.55, 76.60)

    assert nomk1_str == 'T-47-123-А,Б,124-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 98.00000000000000) < delta
    assert abs(min_y1 - 76.50000000000000) < delta
    assert abs(max_y1 - 76.66666666666667) < delta

    ## Forth
    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_50k(97.85, 76.60)

    assert nomk1_str == 'T-47-123-А,Б,124-А,Б'
    assert abs(min_x1 - 97.00000000000000) < delta
    assert abs(max_x1 - 98.00000000000000) < delta
    assert abs(min_y1 - 76.50000000000000) < delta
    assert abs(max_y1 - 76.66666666666667) < delta

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

    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_25k(29.29, 60.0793697371)
    nomk2_str, min_x2, max_x2, min_y2, max_y2 = coord.coords_to_25k(29.43, 60.0793697371)

    assert nomk1_str == nomk2_str and min_x1 == min_x2 and max_x1 == max_x2 and min_y1 == min_y2 and max_y2 == max_y2

def test_10k():
    is_south = False
    letter = 'N'
    zone = 37
    number2 = 4
    letter2 = u'В'
    last_letter = u'а'
    last_number = 4

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_10k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_10k(letter, zone, number2, letter2, last_letter, last_number, is_south)

    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '10k'
    assert nomk_str == u'N-37-004-В-а-4'

    nomk1_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_10k(29.39, 60.0793697371)
    nomk2_str, min_x2, max_x2, min_y2, max_y2 = coord.coords_to_10k(29.48, 60.0793697371)

    assert nomk1_str == nomk2_str and min_x1 == min_x2 and max_x1 == max_x2 and min_y1 == min_y2 and max_y2 == max_y2

def test_5k():
    is_south = False
    letter = 'N'
    zone = 37
    number2 = 4
    last_number = 180

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_5k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_5k(letter, zone, number2, last_number, is_south)
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '5k'
    assert nomk_str == u'N-37-004-(180)'

def test_2k():
    is_south = False
    letter = 'N'
    zone = 37
    number2 = 4
    last_number = 180
    last_letter = u'и'

    nomk_str, min_x1, max_x1, min_y1, max_y1 = coord.coords_to_2k(37.61556, 55.75222)
    scale, min_x2, max_x2, min_y2, max_y2 = text.text_to_2k(letter, zone, number2, last_number, last_letter, is_south)
    # print(u'{} - {},{},{},{}'.format(nomk_str, min_x1, max_x1, min_y1, max_y1))
    # print(u'{} - {},{},{},{}'.format(scale, min_x2, max_x2, min_y2, max_y2))
    
    assert abs(min_x1 - min_x2) < delta
    assert abs(max_x1 - max_x2) < delta
    assert abs(min_y1 - min_y2) < delta
    assert abs(max_y1 - max_y2) < delta

    assert scale == '2k'
    assert nomk_str == u'N-37-004-(180)-и'


def test_O_46_060():
    _, O_46_059_min_x2, O_46_059_max_x2, O_46_059_min_y2, O_46_059_max_y2 = text.text_to_100k('O', 46, 59, False)
    _, O_46_060_min_x2, O_46_060_max_x2, O_46_060_min_y2, O_46_060_max_y2 = text.text_to_100k('O', 46, 60, False)
    
    assert O_46_060_min_x2 > O_46_059_min_x2, 'O-46-59/60 Expected {} > {}'.format(O_46_060_min_x2, O_46_059_min_x2)
    assert O_46_060_max_x2 > O_46_059_max_x2, 'O-46-59/60 Expected {} > {}'.format(O_46_060_max_x2, O_46_059_max_x2)

def test_O_46_072_A():
    _, O_46_071_B_min_x2, O_46_071_B_max_x2, _, _ = text.text_to_50k('O', 46, 71, 'Б', False)
    _, O_46_072_A_min_x2, O_46_072_A_max_x2, _, _ = text.text_to_50k('O', 46, 72, 'А', False)
    
    assert O_46_072_A_min_x2 > O_46_071_B_min_x2
    assert O_46_072_A_max_x2 > O_46_071_B_max_x2
