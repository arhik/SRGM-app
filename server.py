import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import uuid
import pandas as pd
import json
import plotly
from plotly.offline import download_plotlyjs
from models.GO import *

import numpy as np
# import pandas as pd
# import plotly
__UPLOADS__ = "uploaded_csv_files/"
root = os.path.dirname(__file__)
from tornado.options import define, options
original_data = None;
define("port", default=3000, help="run on the given port", type=int)

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting',"Hello")
		self.render('index.html')

class Sample(tornado.web.RequestHandler):
	def get(self):
		dataframe = pd.read_csv()
		g = self.plotlyData(dataframe)
		self.finish(json.dumps(g))

class Upload(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Credentials", "true")
		self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
		self.set_header("Access-Control-Allow-Headers","Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")
		fileinfo = self.request.files['file'][0]
		# print ("fileinfo is", fileinfo)
		fname = fileinfo['filename']
		extn = os.path.splitext(fname)[1]
		cname = str(uuid.uuid4()) + extn
		# print(cname)
		fh = open(__UPLOADS__ + cname, 'wb')
		fh.write(fileinfo['body'])
		fh.close()
		dataframe = pd.read_csv(__UPLOADS__+cname)

		global original_data
		original_data = dataframe

		g = self.plotlyData(dataframe)
		# plotly.offline.plot([g])
		# print(json.dumps(g))
		self.finish(json.dumps(g))

	def dygraphData(self,df):
		# headers = df.
		dt = df.to_dict()
		headers = dt.keys()
		# ts =[[dt["FT"][i],dt["IF"][i],dt["FN"][i]] for i in range(len(dt[headers[0]]))]
		ts = [[dt["FT"][i],dt["FN"][i]] for i in range(len(dt[headers[0]]))]
		return json.dumps(ts)

	def plotlyData(self,dataframe):
		try:
			dataTrace = [{'x' : list(dataframe["FT"]), 'y' : list(dataframe["FN"]), 'mode': 'lines+markers',
					  "name": 'Original Data',
					  "line": {"shape": 'vh'},
					  "type": 'scatter'}]
		except Exception as e:
			return json.dumps(None)
		return json.dumps(dataTrace) # Should return list of the different plots.

	def datatablesData(self,dataframe):
		dt = dataframe.to_dict()
		headers = dt.keys()
		names = [{"title": i } for i in headers]
		ts =[[dt["FT"][i],dt["IF"][i],dt["FN"][i]] for i in range(len(dt[headers[0]]))]
		return json.dumps({"data": ts, "columns": names})


class Compute(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Credentials", "true")
		self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
		self.set_header("Access-Control-Allow-Headers","Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control")
		data = json.loads(self.request.body)

		# print("received data:")
		# print(data)
		x = data[0]["x"]
		y = data[0]["y"]
		# print("FT vector is")
		# print(x)
		soll,lnL_values, endpoints  = go_mle(x)
		# print(soll)
		# print(x,y)
		# print("compute data here:")
		# print(data)
		dataf = pd.DataFrame([x,y]).transpose()
		dataf.columns = ["FT","FN"]
		mvf_data = GO_MVF(soll,dataf)
		# mvf_data.columns = ["FT","FN"]
		# print(mvf_data)
		dataTrace1 = {'x' : list(mvf_data["FT"]), 'y' : list(mvf_data["FN"]), 'mode': 'lines+markers',
				  "name": 'GO-Model',
				  "line": {"shape": 'vh'},
				  "type": 'scatter'}
		# dataTrace2 = {'x' : range(50), 'y' : range(100), "mode": 'lines', "type": "scatter"}
		# dump = {"plotly": dataTrace, "plotly3d": }
		dataTrace3D, dataTrace2D = self.prepare1(lnL_values,x, endpoints)
		# print(dataTrace2)
		self.finish(json.dumps({"plotlyContour2D": dataTrace2D, "plotlyContour3D":dataTrace3D, "plotlyPlot":dataTrace1}))
		# self.finish(json.dumps(dataTrace2))

	def prepare1(self,lnL_values,x, endpoints):
		def GO_MLEeq(b):
			return((n * tn * math.exp(-b * tn)) / (1 - math.exp(-b * tn))) + sumT - n / b
		n = len(x)
		tn = x[-1]
		ba = lnL_values[0][0] 
		bb = lnL_values[-1][0]
		# ba = endpoints[0]
		# bb = endpoints[1]
		aa = n / (1 - math.exp(-ba * (tn)))
		ab = n / (1 - math.exp(-bb * (tn)))
		lnl_bmle_original = [lnL_values[i][0] for i in range(len(lnL_values))]
		lnl_amle_original = [n / (1 - math.exp(-i * (tn))) for i in lnl_bmle_original]
		lnl_bmle = np.linspace(ba, bb, 100).tolist()
		lnl_amle = np.linspace(aa, ab, 100).tolist()		
		# print(lnl_bmle,lnl_amle)

		
		# print("MLE check")
		# print(ba,bb,aa,ab)
		# X = np.linspace(ba, bb, 10).tolist()
		# Y = np.linspace(aa, ab, 10).tolist()
		X = np.linspace(ba, 2*bb - ba , 100).tolist()
		Y = np.linspace(aa, 2*ab - aa, 100).tolist()
		Z = [[GO_lnL({'bMLE':x1,'aMLE':y1}, x) for x1 in X]  for y1 in Y]
		z = [GO_lnL({'aMLE':lnl_amle[i],'bMLE':lnl_bmle[i]}, x) for i in range(len(lnl_bmle))]
		# print("minimum of Z", min(Z))
		# print("maximum of Z", max(Z))
		dataTrace3D = [{'x' : X, 'y' : Y, 'z': Z,
  "type": 'surface'},{"x": lnl_bmle, "y":lnl_amle, "z": z, "type": "scatter3d" }]
  		dataTrace2D = [{"x": X, "y":Y, "z": Z, "type": "contour" },{"x": lnl_bmle_original, "y":lnl_amle_original, "z": Z, "type": "line" }]
		return((dataTrace3D, dataTrace2D))

		

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/upload", Upload),
											(r"/compute", Compute),
											(r"/sample",Sample),
											(r"/(.*)", tornado.web.StaticFileHandler,\
				{"path":root, "default_filename":"index.html"})
											], debug=True)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
