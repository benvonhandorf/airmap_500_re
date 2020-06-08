import sigrokdecode as srd
import math
from PIL import Image

class Decoder(srd.Decoder):
	api_version = 2
	id = 'am500display'
	name = 'am500 display protocol'
	longname = 'AirMap 500 Display Protocol'
	desc = 'AirMap 500 Display Protocol'
	license = 'gplv2+'
	inputs = ['spi']
	outputs = ['x', 'y']
	channels = (
		{'id': 'pc', 'name': 'PC', 'desc': 'Pixel Clock'},
		{'id': 'sp', 'name': 'SP', 'desc': 'Sync Pulse'},
		{'id': 'd0', 'name': 'D0', 'desc': 'Data 0 (LSB)'},
		{'id': 'd1', 'name': 'D1', 'desc': 'Data 1'},
		{'id': 'd2', 'name': 'D2', 'desc': 'Data 2'},
		{'id': 'd3', 'name': 'D3', 'desc': 'Data 3 (MSB)'},
		)
	optional_channels = (
	)

	annotations = (
		('pixel', 'Pixel Data'),
		('sync', 'Frame Sync'),
	)

	tags = []

	def start(self):
		self.out_ann = self.register(srd.OUTPUT_ANN)
		self.sync = False
		self.pc = 0
		self.width = 180
		self.height = 240
		self.skip = 0
		self.image = Image.new('L', (self.width, self.height))
		self.x = 0
		self.y = 0
		self.pixel_values = [0x00, 0x0F, 0x40, 0xFF]

	def write_next_pixel(self, value):
		self.image.putpixel((self.x, self.y), self.pixel_values[int(value)])
		
		self.x = self.x + 1

		if self.x >= self.width:
			self.y = self.y + 1
			self.x = 0
			self.image.save('image.jpg')

		if self.y >= self.height:
			print('Image wrapped')

			self.y = 0
			self.x = 0

	def handle_value(self, value):
		self.put(ss, es, self.out_ann, [0, ['{} {:02X}'.format(value, value)]])

		if self.skip == 0:
			self.write_next_pixel(value)
		else:
			self.skip = self.skip - 1



	def decode(self, ss, es, data):
		
		for (self.samplenum, pins) in data:
			(pc, sp, d0, d1, d2, d3) = pins

			if self.sync == False and sp == 1:
				self.put(ss, es, self.out_ann, [1, ['Sync']])
				self.sync = True

			if self.sync and self.pc == 0 and pc == 1:
				# PC went positive, time to sample
				value = d0 + (d1 << 1)

				self.handle_value(value)

				value = d2 + (d3 << 1)

				self.handle_value(value)

			self.pc = pc



