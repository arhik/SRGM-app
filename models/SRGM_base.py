from abc import ABCMeta, abstractmethod

class SRGM(metaclass = ABCMeta):
	# pass
	@abstractmethod
	def mle(self, x):
		pass

	@abstractmethod
	def mvf(self, params, x):
		pass

	@abstractmethod
	def lnl(self, params, x):
		pass