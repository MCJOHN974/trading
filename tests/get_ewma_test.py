import sys
sys.path.append('..')
from get_ewma import get_ewma

print("get_ewma testing started")
assert list(get_ewma([1,2,3,4,5], 3, 0.25)) == [(1*0.25+2*0.5+3*1) / 1.75,
                                                (2*0.25+3*0.5+4*1) / 1.75,
                                                (3*0.25+4*0.5+5*1) / 1.75]

print("get_ewma tested successfully")
