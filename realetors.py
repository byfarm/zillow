class Company(object):
	def __init__(self, name: str, phone: str, address: str, websites: list, boss: object):
		self.name = name
		self.phone = phone
		self.address = address
		self.websites = websites
		self.realtors = [boss]

	def __repr__(self):
		return f'{self.name}'

	def add_rel(self, realtor: object):
		self.realtors.append(realtor)


class Realtor(object):
	def __init__(self, name: str, phone: str, company: str, address: str, websites: list):
		self.address = address
		self.name = name
		self.phone = phone
		self.company = company
		self.websites = websites

	def __repr__(self):
		return f'{self.name}'