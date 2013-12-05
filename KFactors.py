import os
import numpy as np
from scipy.interpolate import interp1d

class KFactors:
    def __init__(self):
        mepath   = os.path.dirname(os.path.realpath(__file__))
        self.datafile = mepath+"/MKF_W.dat"
        
        if not os.path.exists(self.datafile):
            print "K-factors data is not present -- downloading ..."
            os.system("wget -q  http://personalpages.to.infn.it/~giampier/MKF_W.dat -O {0}".format(self.datafile))
            print "... done"

        data = []
        with open(self.datafile) as kFile:
            for line in kFile:
                binl,binu,knnlo,sqkgg = [float(x) for x in line.split()]
                data += [((binl+binu)/2,knnlo,sqkgg)]

        bs,ks,kggs = [np.array(x) for x in zip(*data)]
        self.datas = (bs,ks,kggs)
        self.ks  = interp1d(bs,ks)
        self.kgg = interp1d(bs,kggs)

    def GetK(self):     return self.ks
    def GetSqKgg(self): return self.kgg


            
