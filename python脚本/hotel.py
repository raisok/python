#!/usr/bin/env python

class HotelRoomCalc(object):
	'Hotel room rate calculator'
	def __init__(self, rt, sales=0.085, rm=0.1):
		self.salesTax = sales
		self.roomTax = rm
		self.roomRate = rt
	
	def calcTotal(self, days=1):
		daily = round((self.roomRate*(1+ self.roomTax + self.salesTax)),2)
		return float(days)*daily

		
class EmplAddrBookEntry(AddrBookEntry):
	def __init__ (self, nm, ph, em):
		AddrBookEntry.__init__ (self, nm, ph)
		self.empid = id
		self.email = em