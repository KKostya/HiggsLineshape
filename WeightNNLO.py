from .Signal import Signal
from .Interference import Interference
from .KFactors import KFactors

class WeightNNLO:
    def __init__(self, sParam, iParam):
        self.kf     = KFactors()
        self.sig    = Signal(sParam)
        self.interf = Interference(iParam)

    def Get_SI_Central(self,m,c):
        s = self.sig.GetLS(m,c)
        i = self.interf.GetLS(m,c) 
        k = self.kf.GetK()
        sqkgg = self.kf.GetSqKgg()

        def sishape(x):
            return k(x)*s(x)+sqkgg(x)*i(x)
        return sishape


