from SRGM_base import SRGM

class GO(SRGM):
	def mle(self, x):
	    n = len(x)
	    tn = x[-1]
	    sumT = sum(x)
	    lnl_values = [];
	    def GO_MLEeq(b):
	    	return ((n * tn * math.exp(-b * tn)) / (1 - math.exp(-b * tn))) + sumT - n / b

	    def tracing(x,f):
	        lnl_values.append([x.tolist()[0],f.tolist()[0]])
	        
	    b0 = n / sumT
	    i = 0
	    maxIterations = 100
	    leftEndPoint = b0 / 2
	    leftEndPointMLE = GO_MLEeq(leftEndPoint)
	    rightEndPoint = 1.2 * b0
	    rightEndPointMLE = GO_MLEeq(rightEndPoint)

	    while(leftEndPointMLE * rightEndPointMLE > 0 & i <= maxIterations):
	    	leftEndPoint = leftEndPoint / 2
	    	leftEndPointMLE = GO_MLEeq(leftEndPoint)
	    	rightEndPoint = 2 * rightEndPoint
	    	rightEndPointMLE = GO_MLEeq(rightEndPoint)
	    	i = i + 1

	    if(leftEndPointMLE * rightEndPointMLE > 0):
	    	return("nonconvergence")
	    else:
	    	sol = optimize.root(GO_MLEeq, b0, method='krylov', callback=tracing)
	    	bMLE = sol.x
	    	aMLE = n / (1 - math.exp(-bMLE * (tn)))
	    	sol = pd.DataFrame([aMLE, bMLE]).transpose()
	    	sol.columns = ["aMLE", "bMLE"]
	    	return([sol,lnl_values,[leftEndPoint,rightEndPoint]])



	def mvf(self, params, d):
		n = len(d['FN'])
		ft = list(d['FN'])
		f = lambda x: -(math.log((list(params['aMLE'])[0] - x)/list(params['aMLE'])[0]))/list(params['bMLE'])[0]
		r = map(f,list(d['FN']))
		r = pd.DataFrame([list(d['FN']),list(r)]).transpose()
		r.columns= ["FN","FT"]
		return(r)


	def lnl(self, params,d):
	    aMLE = params['aMLE']
	    bMLE = params['bMLE']
	    n = len(d)
	    tn = d[-1]
	    firstSumTerm = sum([(-bMLE*d[i]) for i in range(n)])
	    lnL =  -(aMLE)*(1-math.exp(-bMLE*tn)) + n*(math.log(aMLE)) + n*(math.log(bMLE)) + firstSumTerm
	    return lnL
