# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 23:32:30 2016

@author: arhik
"""

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
