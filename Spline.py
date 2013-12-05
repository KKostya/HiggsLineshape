from scipy.interpolate import UnivariateSpline


########################## Spline data ############################33
t = [ 223., 223., 223., 223., 273., 323., 337., 349., 373., 421., 617., 1011., 1209., 1405., 1797., 1797., 1797., 1797.]
c = [ 0.00017048,  0.00021389,  0.00036477,  0.00060971,  0.0009098 , 0.00129752,
      0.00194537,  0.00311643,  0.00261153,  0.00135339, 0.00083337,  0.00038015,
        0.00026813,  0.00017928,  0.        , 0.        ,  0.        ,  0.        ]

def SplineFromTCK(t,c,k):
    self = UnivariateSpline.__new__(UnivariateSpline)
    self._eval_args = (t,c,k,)
    self._data = (None,None,None,None,None,k,None,len(t),t,c,None,None,None,None)
    return self

spline = SplineFromTCK(t,c,3)


