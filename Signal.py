import numpy as np
import os
import json
from   scipy.interpolate import Rbf

from .Spline import spline

################### The siganl shape is fitted with this ###################
def BWS(m,x,n,g):
    return n*x*spline(x)/((x**2-m**2)**2+(m*g)**2)
###########################################################################


class Signal:
    def __init__(self,paramFname=None):
        if not paramFname:
            paramFname = os.path.dirname(os.path.realpath(__file__)) + "/signalParams.json"
        # Loading parameters
        fitParams = {}
        with open(paramFname) as jsonFile:
            fitParams = json.load(jsonFile)
            # Converting string to numbers 
            for m in fitParams: 
                fitParams[int(m)] = fitParams.pop(m)
                for c in fitParams[int(m)]: 
                    fitParams[int(m)][float(c)] = fitParams[int(m)].pop(c)
        if not fitParams: raise Exception("Could not read the {0}  file.".format(paramFile))

        # Creating parameter interpolations  
        self.m = np.array(sorted(fitParams.keys()))
        self.splines = [None for a in range(2)]
        self.datas   = self.splines[:]
        for nvar, smooth in [ (1, 1E-4), (0, 1E-4)]:
            data = []
            for c in [0.5,0.6,0.7,0.8,0.9,1.0]: 
                data +=  [(x,c,fitParams[x][c][nvar]) for x in self.m if c in fitParams[x]]

            ms,cs,vs = [np.array(x) for x in zip(*data)]

            self.datas  [nvar] = (ms,cs,vs)
            self.splines[nvar] = Rbf(ms,1000*cs,vs,smooth=smooth)
        self.fp = fitParams

    def GetParam(self, nplotvar):
        return self.datas[nplotvar]
    def GetParamSpline(self, nplotvar):
        return self.splines[nplotvar]
        
    def GetLS(self,m,c):
        params = [self.splines[i](m,1000*c) for i in range(2)]
        def sLineShape(x):
            return BWS(m,x,*params)
        return sLineShape
