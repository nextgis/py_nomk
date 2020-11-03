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
import parser
import util

def test_1m_parse():
    nomk_str = u'N-37'
    scale, parts, is_south = parser.parse(nomk_str, '1m')
    assert scale == '1m'
    assert len(parts) == 2
    assert parts[0] == 'N'
    assert parts[1] == 37
    assert is_south == False

    nomk_str = u'U-37,38,39,40'
    scale, parts, is_south = parser.parse(nomk_str)
    assert scale == '1m'
    assert len(parts) == 2
    assert parts[0] == 'U'
    assert parts[1] == 40
    assert is_south == False

    nomk_str = u'A-15' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str)
    assert scale == '1m'
    assert len(parts) == 2
    assert parts[0] == 'A'
    assert parts[1] == 15
    assert is_south == True

def test_500k_parse():
    nomk_str = u'O-48-Г'
    scale, parts, is_south = parser.parse(nomk_str, '500k')
    assert scale == '500k'
    assert len(parts) == 3
    assert parts[0] == 'O'
    assert parts[1] == 48
    assert parts[2] == u'Г'
    assert is_south == False

    nomk_str = u'N-48-Б' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str, '500k')
    assert scale == '500k'
    assert len(parts) == 3
    assert parts[0] == 'N'
    assert parts[1] == 48
    assert parts[2] == u'Б'
    assert is_south == True

    nomk_str = u'P-49-А,Б'
    scale, parts, is_south = parser.parse(nomk_str, '500k')
    assert scale == '500k'
    assert len(parts) == 3
    assert parts[0] == 'P'
    assert parts[1] == 49
    assert parts[2] == u'Б'
    assert is_south == False

    nomk_str = u'T-47-В,Г,48-В,Г'
    scale, parts, is_south = parser.parse(nomk_str, '500k')
    assert scale == '500k'
    assert len(parts) == 3
    assert parts[0] == 'T'
    assert parts[1] == 48
    assert parts[2] == u'Г'
    assert is_south == False

def test_200k_parse():
    nomk_str = u'T-48-XXVIII,XXIX,XXX'
    scale, parts, is_south = parser.parse(nomk_str, '200k')
    assert scale == '200k'
    assert len(parts) == 3
    assert parts[0] == 'T'
    assert parts[1] == 48
    assert parts[2] == u'XXX'
    assert is_south == False

    nomk_str = u'A-15-XIX' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str)
    assert scale == '200k'
    assert len(parts) == 3
    assert parts[0] == 'A'
    assert parts[1] == 15
    assert parts[2] == u'XIX'
    assert is_south == True

def test_100k_parse():
    nomk_str = u'U-48-141,142,143,144'
    scale, parts, is_south = parser.parse(nomk_str, '100k')
    assert scale == '100k'
    assert len(parts) == 3
    assert parts[0] == 'U'
    assert parts[1] == 48
    assert parts[2] == 144
    assert is_south == False

    nomk_str = u'A-15-009' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str)
    assert scale == '100k'
    assert len(parts) == 3
    assert parts[0] == 'A'
    assert parts[1] == 15
    assert parts[2] == 9
    assert is_south == True

def test_50k_parse():
    nomk_str = u'T-48-033-А,Б,034-А,Б' #U-49-135-В,Г,136-В,Г || T-48-035-А,Б,036-А,Б
    scale, parts, is_south = parser.parse(nomk_str, '50k')
    assert scale == '50k'
    assert len(parts) == 4
    assert parts[0] == 'T'
    assert parts[1] == 48
    assert parts[2] == 34
    assert parts[3] == u'Б'
    assert is_south == False

    nomk_str = u'U-49-135-В,Г,136-В,Г' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str, '50k')
    assert scale == '50k'
    assert len(parts) == 4
    assert parts[0] == 'U'
    assert parts[1] == 49
    assert parts[2] == 136
    assert parts[3] == u'Г'
    assert is_south == True

def test_25k_parse():
    nomk_str = u'T-48-047-А-а,б,Б-а,б' # U-49-137-В-а,б,Г-а,б || T-48-046-А-а,б,Б-а,б
    scale, parts, is_south = parser.parse(nomk_str, '25k')
    assert scale == '25k'
    assert len(parts) == 5
    assert parts[0] == 'T'
    assert parts[1] == 48
    assert parts[2] == 47
    assert parts[3] == u'Б'
    assert parts[4] == u'б'
    assert is_south == False

    nomk_str = u'U-49-137-В-а,б,Г-а,б' + util.south_suffix()
    scale, parts, is_south = parser.parse(nomk_str, '25k')
    assert scale == '25k'
    assert len(parts) == 5
    assert parts[0] == 'U'
    assert parts[1] == 49
    assert parts[2] == 137
    assert parts[3] == u'Г'
    assert parts[4] == u'б'
    assert is_south == True