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

	        # print("callback--", str((x,f)))
	        lnl_values.append([x.tolist()[0],f.tolist()[0]])
	        # return lnl_values
	        # return lnl_values.append({x:f})

	    b0 = n / sumT

	    i = 0

	    maxIterations = 100
	    leftEndPoint = b0 / 2
	    leftEndPointMLE = GO_MLEeq(leftEndPoint)
	    rightEndPoint = 1.2 * b0
	    rightEndPointMLE = GO_MLEeq(rightEndPoint)

	    while(leftEndPointMLE * rightEndPointMLE > 0 & i <= maxIterations):
	    	# print(leftEndPoint, rightEndPoint)
	    	leftEndPoint = leftEndPoint / 2
	    	leftEndPointMLE = GO_MLEeq(leftEndPoint)
	    	rightEndPoint = 2 * rightEndPoint
	    	rightEndPointMLE = GO_MLEeq(rightEndPoint)
	    	i = i + 1

	    if(leftEndPointMLE * rightEndPointMLE > 0):
	    	return("nonconvergence")
	    else:
	    	# maxiter = 20
	    	# sol =
	    	# optimize.bisect(GO_MLEeq,0,1e20,xtol=1e-10,rtol=1e-10,maxiter=1000,full_output=False,disp=False)
	    	sol = optimize.root(GO_MLEeq, b0, method='krylov', callback=tracing)
	    	bMLE = sol.x
	    	# print(sol)

	    	aMLE = n / (1 - math.exp(-bMLE * (tn)))

	    	sol = pd.DataFrame([aMLE, bMLE]).transpose()
	    	# print(sol)
	    	sol.columns = ["aMLE", "bMLE"]
	    	# print(sol)
	        # print("callback trace")
	        # print(lnl_values);
	    	return([sol,lnl_values,[leftEndPoint,rightEndPoint]])



	def mvf(self, params, d):
		n = len(d['FN'])
		# print(d['FN'])
		ft = list(d['FN'])
		# print(ft)
		f = lambda x: -(math.log((list(params['aMLE'])[0] - x)/list(params['aMLE'])[0]))/list(params['bMLE'])[0]
		r = map(f,list(d['FN']))
		r = pd.DataFrame([list(d['FN']),list(r)]).transpose()
		# print("-------------------------------")
		# print(r)
		r.columns= ["FN","FT"]
		# print(r)
		return(r)


	def lnl(self, params,d):
	    # print(params)
	    aMLE = params['aMLE']
	    bMLE = params['bMLE']
	    # print("d is :",d)
	    n = len(d)
	    # print("length:",n)

	    tn = d[-1]
	    # print("final value:", tn)
	    # firstSumTerm = 0
	    firstSumTerm = sum([(-bMLE*d[i]) for i in range(n)])
	    # print("firstsumterm")
	    # print(firstSumTerm)
	    lnL =  -(aMLE)*(1-math.exp(-bMLE*tn)) + n*(math.log(aMLE)) + n*(math.log(bMLE)) + firstSumTerm
	    # print("Present Log likelihood:")
	    # print(lnL)
	    return lnL
