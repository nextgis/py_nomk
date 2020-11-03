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

import re
import nomk
import util

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

# 1m U-37,38,39,40
# 500k Q-48-В,Г || T-47-В,Г,48-В,Г
# 200k T-48-28,29,30 || T-48-XXVIII,XXIX,XXX
# 100k U-48-141,142,143,144
# 50k 50k T-48-033-А,Б,034-А,Б || U-49-135-В,Г,136-В,Г || T-48-035-А,Б,036-А,Б
# 25k T-48-047-А-а,б,Б-а,б || U-49-137-В-а,б,Г-а,б || T-48-046-А-а,б,Б-а,б
# 10k T-47-004-А-а-1,2,б-1,2 || U-47-136-В-в-3,4,г-3,4 || U-47-136-В-в-1,2,г-1,2
# 5k O-41-109-(064)
# 2k M-38-125-(063)-а

def south_suffix():
    return util.south_suffix().replace(u'(', u'\(').replace(u')', u'\)')

def get_first_sym(val):
    some_str = val.replace(',', '')
    parts = some_str.split('-')
    return parts[0]

def parse1m(nomk_str):
    regex_1m = ur'^([A-V])-((,?\d+)+)\s?({})?'.format(south_suffix())
    result = re.match(regex_1m, nomk_str)
    letter = result.group(1)
    number = int(result.group(3).replace(',', ''))
    return [letter, number], result.group(4) != None

def parse500k(nomk_str):
    regex_500k = ur'^([A-V])-((,?\d+-(,?[А-Г])+)+)\s?({})?'.format(south_suffix())
    result = re.match(regex_500k, nomk_str)
    letter = result.group(1)
    number = int(get_first_sym(result.group(3)))
    last_letter = result.group(4).replace(',', '')
    return [letter, number, last_letter], result.group(5) != None

def parse200k(nomk_str):
    regex_200k = ur'^([A-V])-((,?\d+-(,?[IVX]+)+)+)\s?({})?'.format(south_suffix())
    result = re.match(regex_200k, nomk_str)
    letter = result.group(1)
    number = int(get_first_sym(result.group(2)))
    last_letter = result.group(4).replace(',', '')
    return [letter, number, last_letter], result.group(5) != None

def parse100k(nomk_str):
    regex_100k = ur'^([A-V])-(\d+)-((,?\d+)+)\s?({})?'.format(south_suffix())
    result = re.match(regex_100k, nomk_str)
    letter = result.group(1)
    number = int(get_first_sym(result.group(2)))
    last_letter = result.group(4).replace(',', '')
    last_letter_num = int(last_letter)
    return [letter, number, last_letter_num], result.group(5) != None

def parse50k(nomk_str):
    regex_50k = ur'^([A-V])-(\d+)-((,?\d+)-(,?[А-Г])+)+\s?({})?'.format(south_suffix())
    result = re.match(regex_50k, nomk_str)
    letter = result.group(1)
    number = int(get_first_sym(result.group(2)))
    last_number = result.group(4).replace(',', '')
    last_number_num = int(last_number)
    last_letter = result.group(5).replace(',', '')
    return [letter, number, last_number_num, last_letter], result.group(6) != None

def parse25k(nomk_str):
    regex_25k = ur'^([A-V])-(\d+)-(\d+)-(,?[А-Г]-(,?[а-г])+)+\s?({})?'.format(south_suffix())
    result = re.match(regex_25k, nomk_str)
    letter = result.group(1)
    number = int(result.group(2))
    number2 = int(result.group(3))
    letter2 = get_first_sym(result.group(4))
    last_letter = result.group(5).replace(',', '')
    return [letter, number, number2, letter2, last_letter], result.group(6) != None

def parse10k(nomk_str):
    regex_10k = ur'^([A-V])-(\d+)-(\d+)-([А-Г])-((,?[а-г])+-(,?\d)+)+\s?({})?'.format(south_suffix())
    result = re.match(regex_10k, nomk_str)
    letter = result.group(1)
    number = int(result.group(2))
    number2 = int(result.group(3))
    letter2 = result.group(4).replace(',', '')
    last_letter = result.group(6).replace(',', '')
    last_number = int(result.group(7).replace(',', ''))
    return [letter, number, number2, letter2, last_letter, last_number], result.group(8) != None

def parse(nomk_str, scale = ''):
    """Parses input nomenclature string and returns scale and 
        list of parts of first sheet

        Raises exception if not parsed 
    """

    nomk_str = nomk_str.strip().replace(" ", "")

    if scale == '1m':
        return ('1m',) + parse1m(nomk_str)
    elif scale == '500k':
        return ('500k',) + parse500k(nomk_str)
    elif scale == '200k':
        return ('200k',) + parse200k(nomk_str)
    elif scale == '100k':
        return ('100k',) + parse100k(nomk_str)
    elif scale == '50k':
        return ('50k',) + parse50k(nomk_str)
    elif scale == '25k':
        return ('25k',) + parse25k(nomk_str)
    elif scale == '10k':
        return ('10k',) + parse10k(nomk_str)
    else:
        # Test all parsers
        try:
            return ('10k',) + parse10k(nomk_str)
        except:
            pass

        try:
            return ('25k',) + parse25k(nomk_str)
        except:
            pass

        try:
            return ('50k',) + parse50k(nomk_str)
        except:
            pass

        try:
            return ('100k',) + parse100k(nomk_str)
        except:
            pass

        try:
            return ('200k',) + parse200k(nomk_str)
        except:
            pass

        try:
            return ('500k',) + parse500k(nomk_str)
        except:
            pass    

        try:
            return ('1m',) + parse1m(nomk_str)
        except:
            pass
 
        raise Exception('Failed to parse')
