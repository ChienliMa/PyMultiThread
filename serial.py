import numpy as np
import threading
import time 
from datapool import datapool



def train( x ):
    """
    a fake training function
    """
    num = 0
    sum = 0
    for i in x.flatten():
        sum += i
        num += 1
    return float( sum )/num
def test(): 
    """
    """
    batch_size = (4,3,128,128)
    pool = datapool( './Data/','data.txt', batch_size)
    
    starttime = time.time()
    for batch in pool.get():
        print "this cost = ", train( batch )
    endtime = time.time()
    
    print "used time:", endtime - starttime, 's'

if __name__ == "__main__":
    test()

