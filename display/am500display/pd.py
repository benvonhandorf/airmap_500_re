import sigrokdecode as srd
import math

class Decoder(srd.Decoder):
	api_version = 3
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


	def reset(self):
		self.sync = False

	def decode(self, ss, es, data):
		
		for (self.samplenum, pins) in data:
			(pc, sp, d0, d1, d2, d3) = pins

			if sp == 1:
				self.put(ss, es, self.out_ann, [1, ['Sync']])
				self.sync = True

			if self.sync and self.pc == 0 and pc == 1:
				# PC went positive, time to sample
				value = d0 + d1 << 1 + d2 << 2 + d3 << 3

				self.put(ss, es, self.out_ann, [0, [value, '{:02X}'.format(value)]])

				print("value: {}".format(value))

			self.pc = pc



