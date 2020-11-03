import string
import re


class Nomk(object):
	reg_exp = None

	def to_wkt(self, x_min, y_min, x_max, y_max):
		return 'POLYGON (({x_min} {y_min}, {x_min} {y_max}, {x_max} {y_max}, {x_max} {y_min}, {x_min} {y_min}))'.format(
			x_min=x_min,
			y_min=y_min,
			x_max=x_max,
			y_max=y_max,
		)

	def get_bbox_as_wkt(self):
		return self.to_wkt(*self.get_bbox())


class Nomk1m(Nomk):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*$'

	row_availbale = string.ascii_lowercase[:22].upper()
	col_availbale = range(1, 61)

	def __init__(self, row, cols):
		super().__init__()

		self.row = row
		self.cols = list(map(int, cols.split(',')))

		self._all_parts = {}
		self._requested_parts = {}
		self._sheet_size = {
			'1m': (6.0, 4.0)
		}

	def get_bbox(self):
		parts = self.prepare_parts()

		col_min = self.cols[0]
		col_max = self.cols[-1]

		x_max = col_max * 6 - 180
		x_min = col_min * 6 - 180 - 6

		y_max = (self.row_availbale.find(self.row) + 1) * 4
		y_min = y_max - 4
		
		bbox = [x_min, y_min, x_max, y_max]

		for scale in sorted(self._all_parts, key=lambda scale: int(scale.replace('k', '000').replace('m','000000')), reverse=True):
			bbox = self.get_bbox_by_parts(
				bbox, 
				self._all_parts[scale],
				self._requested_parts[scale],
				parts[scale],
				self._sheet_size[scale][0],
				self._sheet_size[scale][1],
			)


		return bbox

	@classmethod
	def construct(cls, nomk):
		row, cols = nomk.split('-')
		return cls(row, cols)

	def prepare_parts(self):
		all_parts = {}
		for scale, parts in self._all_parts.items():
			all_parts[scale] = {}
			row_num = 1
			for row in parts:
				col_num = 1
				for col in row:
					all_parts[scale][col] = (row_num, col_num)
					col_num += 1
				row_num += 1
		return all_parts


	@staticmethod
	def calc_parts_offset(row, col_min, col_max, parts_matrix, x_size, y_size):
		# print('---', row, col_min, col_max)
		rows = len(parts_matrix)
		cols = len(parts_matrix[0])

		x_offset_point = x_size / cols
		y_offset_point = y_size / rows

		return [
			(col_min - 1) * x_offset_point, 
			(rows - row) * y_offset_point, 
			- (cols - col_max) * x_offset_point,
			- (row - 1) * y_offset_point, 		 
		]

	@staticmethod
	def get_bbox_by_parts(parent_bbox, parts_matrix, parts_list, parts, x_size, y_size):
		x_min, y_min, x_max, y_max = parent_bbox
		parts_indexes = [parts[part] for part in parts_list]
		parts_row = parts_indexes[0][0]
		parts_col_min = min([y for x, y in parts_indexes])
		parts_col_max = max([y for x, y in parts_indexes])

		d_x_min, d_y_min, d_x_max, d_y_max = Nomk1m.calc_parts_offset(
			parts_row, parts_col_min, parts_col_max,
			parts_matrix, x_size, y_size
		)
		# print('---', d_x_min, d_y_min, d_x_max, d_y_max)

		return [
			x_min + d_x_min,
			y_min + d_y_min,
			x_max + d_x_max,
			y_max + d_y_max
		]

class Nomk500k(Nomk1m):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-[А-Г](,[А-Г]){0,2}$'

	def __init__(self, row, cols, parts_1m):
		super().__init__(row, cols)

		self._all_parts['1m'] = (
			('А', 'Б'),
			('В', 'Г'),
		)
		self._requested_parts['1m'] = parts_1m.split(',')

	@classmethod
	def construct(cls, nomk):
		row, cols, parts = nomk.split('-')
		return cls(row, cols, parts)


class Nomk200k(Nomk1m):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d\d$'
	# reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-[XIV]{1,5}$'

	def __init__(self, row, cols, parts_1m):
		super().__init__(row, cols)

		# self._all_parts['1m'] = (
		# 	('I', 'II', 'III', 'IV', 'V', 'VI'),
		# 	('VII', 'VIII', 'IX', 'X', 'XI', 'XII'),
		# 	('XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII'),
		# 	('XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV'),
		# 	('XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX'),
		# 	('XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI'),
		# )
		self._all_parts['1m'] = [list(range(row * 6 + 1, row * 6 + 6 + 1)) for row in range(6)]

		self._requested_parts['1m'] = map(int, parts_1m.split(','))

	@classmethod
	def construct(cls, nomk):
		row, cols, parts = nomk.split('-')
		return cls(row, cols, parts)


class Nomk100k(Nomk1m):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d\d\d$'

	def __init__(self, row, cols, parts_1m):
		super().__init__(row, cols)

		self._sheet_size['100k'] = (6.0 / 12, 4.0 / 12)

		self._all_parts['1m'] = [list(range(row * 12 + 1, row * 12 + 12 + 1)) for row in range(12)]
		self._requested_parts['1m'] = map(int, parts_1m.split(','))

	@classmethod
	def construct(cls, nomk):
		row, cols, parts = nomk.split('-')
		return cls(row, cols, parts)


class Nomk50k(Nomk100k):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d{1,3}-[А-Г](,[А-Г]){0,2}$'
	
	def __init__(self, row, cols, parts_1m, parts_100k):
		super().__init__(row, cols, parts_1m)

		self._sheet_size['50k'] = (6.0 / 12 / 2, 4.0 / 12 / 2)

		self._all_parts['100k'] = (
			('А', 'Б'),
			('В', 'Г'),
		)
		self._requested_parts['100k'] = parts_100k.split(',')

	@classmethod
	def construct(cls, nomk):
		row, cols, parts_1m, parts_100k = nomk.split('-')
		return cls(row, cols, parts_1m, parts_100k)


class Nomk25k(Nomk50k):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d{1,3}-[А-Г](,[А-Г]){0,2}-[а-г](,[а-г]){0,2}$'

	def __init__(self, row, cols, parts_1m, parts_100k, parts_50k):
		super().__init__(row, cols, parts_1m, parts_100k)

		self._sheet_size['25k'] = (6.0 / 12 / 2 / 2, 4.0 / 12 / 2 / 2)
		
		self._all_parts['50k'] = (
			('а', 'б'),
			('в', 'г'),
		)
		self._requested_parts['50k'] = parts_50k.split(',')

	@classmethod
	def construct(cls, nomk):
		row, cols, parts_1m, parts_100k, parts_50k = nomk.split('-')
		return cls(row, cols, parts_1m, parts_100k, parts_50k)


class Nomk10k(Nomk25k):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d{1,3}-[А-Г](,[А-Г]){0,2}-[а-г](,[а-г]){0,2}-[1-4]$'
	
	def __init__(self, row, cols, parts_1m, parts_100k, parts_50k, parts_25k):
		super().__init__(row, cols, parts_1m, parts_100k, parts_50k)

		self._all_parts['25k'] = (
			('1', '2'),
			('3', '4'),
		)
		self._requested_parts['25k'] = parts_25k.split(',')

	@classmethod
	def construct(cls, nomk):
		row, cols, parts_1m, parts_100k, parts_50k, parts_25k = nomk.split('-')
		return cls(row, cols, parts_1m, parts_100k, parts_50k, parts_25k)


class Nomk5k(Nomk100k):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d{1,3}\(\d{1,3}\)$'
	
	def __init__(self, row, cols, parts_1m, parts_100k):
		super().__init__(row, cols, parts_1m)

		self._sheet_size['5k'] = (6.0 / 12 / 16, 4.0 / 12 / 16)

		self._all_parts['100k'] = [list(range(row * 16 + 1, row * 16 + 16 + 1)) for row in range(16)]

		self._requested_parts['100k'] =  map(int, parts_100k.split(','))

	@classmethod
	def construct(cls, nomk):
		# N-37-87(70)
		row, cols, parts_1m_and_parts_100k = nomk.split('-')
		parts_1m = parts_1m_and_parts_100k.split('(')[0] 
		parts_100k = parts_1m_and_parts_100k.split('(')[1].split(')')[0]
		return cls(row, cols, parts_1m, parts_100k)


class Nomk2k(Nomk5k):
	reg_exp = r'^[A-V]-\d{1,2}(,\d{1,2})*-\d{1,3}\(\d{1,3}-[а-и]\)$'
	
	def __init__(self, row, cols, parts_1m, parts_100k, parts_5k):
		super().__init__(row, cols, parts_1m, parts_100k)

		self._all_parts['5k'] = (
			('а', 'б', 'в'),
			('г', 'д', 'е'),
			('ж', 'з', 'и'),
		)

		self._requested_parts['5k'] =  parts_5k.split(',')

	@classmethod
	def construct(cls, nomk):
		# N-37-87(70-и)
		row, cols, parts_1m_and_parts_100k, parts_5k_muddy = nomk.split('-')
		parts_1m, parts_100k= parts_1m_and_parts_100k.split('(')
		parts_5k = parts_5k_muddy.strip(')')
		return cls(row, cols, parts_1m, parts_100k, parts_5k)


def get_nomk(nomk):
	''' Get nomk class by nomk string
		Example:
            from nomk2 import get_nomk
            nomk = get_nomk('O-37-050')
            print(nomk.get_bbox_as_wkt())
	'''
	for nomk_class in [Nomk1m, Nomk500k, Nomk200k, Nomk100k, Nomk50k, Nomk25k, Nomk10k, Nomk5k, Nomk2k]:
		if re.match(nomk_class.reg_exp, nomk):
			return nomk_class.construct(nomk)

if __name__ == '__main__':
	
	# samples from https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%80%D0%B0%D0%B7%D0%B3%D1%80%D0%B0%D1%84%D0%BA%D0%B8_%D0%B8_%D0%BD%D0%BE%D0%BC%D0%B5%D0%BD%D0%BA%D0%BB%D0%B0%D1%82%D1%83%D1%80%D1%8B_%D1%82%D0%BE%D0%BF%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D0%BA%D0%B0%D1%80%D1%82
	samples = {
		Nomk1m: ['N-37', 'O-38', 'U-37,38,39,40'],
		Nomk500k: ['N-37-А', 'N-36-А', 'R-39-А,Б', 'T-47-В,Г,48-В,Г'],
		Nomk200k: ['N-37-01', 'N-36-15', 'U-40-31,32,33', 'T-48-28,29,30'],
		Nomk100k: ['N-37-001', 'N-36-023', 'N-37-056', 'U-48-141,142,143,144'],
		Nomk50k: ['N-37-56-А', 'N-37-134-А', 'T-48-033-А,Б,034-А,Б'],
		Nomk25k: ['N-37-56-А-г', 'T-48-047-А-а,б,Б-а,б'],
		Nomk10k: ['N-37-56-А-г-1', 'N-37-56-А-г-3'],
		Nomk5k: ['N-37-87(70)'],
		Nomk2k: ['N-37-87(70-и)'],
	}
	
	for nomk_class, scale_samples in samples.items(): 
		print('--- %s ---' % nomk_class.__name__)
		for nomk in scale_samples:
			print(nomk, '\t:', nomk_class.construct(nomk).get_bbox_as_wkt())
