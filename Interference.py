import json
import os
import numpy as np
from   scipy.interpolate import Rbf

################### Interference fitting functions ################### 
# Interference is modelled with that:

def interf(x,m,n,f,c,g):
    M = np.sqrt(m*m-g*m*1j)
    return -n*np.real((np.exp(f)/(x-M)-np.exp(-f)/(x+M))*np.exp(-x*f/M))

class Interference:
    def __init__(self,paramFname = None):
        if not paramFname:
            paramFname = os.path.dirname(os.path.realpath(__file__)) + "/params.json"


        cvals    = [0.5,0.6,0.7,0.8,0.9,1.0]
        smoothes = [ (3, 1E-6 ), (2, 1E-6), (1, 10), (0, 1E-6) ]


        self.fitParams = {}
        with open(paramFname) as jsonFile:
            self.fitParams = json.load(jsonFile)
            # Converting string to numbers 
            for m in self.fitParams: 
                self.fitParams[int(m)] = self.fitParams.pop(m)
                for c in self.fitParams[int(m)]: 
                    self.fitParams[int(m)][float(c)] = self.fitParams[int(m)].pop(c)

        if not self.fitParams: raise Exception("Could not read the {0} file.".format(paramFname))

        m = np.array(sorted(self.fitParams.keys()))

        self.splines = [None for a in range(4)]
        self.datas   = self.splines[:]
        for nvar, smooth in smoothes:
            data = []
            for c in cvals: 
                data +=  [(x,c,self.fitParams[x][c][nvar]) for x in m 
                             if c in self.fitParams[x] and (x,c)]

            ms,cs,vs = [np.array(x) for x in zip(*data)]
            self.datas  [nvar] = (ms,cs,vs)
            self.splines[nvar] = Rbf(ms,1000*cs,vs,smooth=smooth)

    def GetLS(self,m,c):
        params = [self.splines[i](m,1000*c) for i in range(4)]
        def iLineShape(x):
            return interf(x,m,*params)
        return iLineShape

    def GetParam(self, nplotvar):
        return self.datas[nplotvar]
    def GetParamSpline(self, nplotvar):
        return self.splines[nplotvar]
        
