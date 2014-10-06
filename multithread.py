import numpy as np
import threading
import time 
from datapool import datapool


batch_size = (4,3,128,128)
buffer_batch = np.zeros( batch_size )

def train( x ):
    """
    a fake training function
    """
    sum = 0
    num = 0
    for i in x.flatten():
        sum += i
        num += 1
    return float(sum)/num  

    

class DataThread( threading.Thread ):
    def __init__( self, datapool, batch_lock, train_lock,pool_lock ): 
        """
        """
        threading.Thread.__init__(self)
        self.datapool = datapool
        self.batch_lock = batch_lock
        self.pool_lock = pool_lock
        self.train_lock = train_lock

    def run( self ):
        """
        """
        global buffer_batch
        for batch in self.datapool.get():
            
            self.pool_lock.acquire()
            self.batch_lock.acquire()
            
            buffer_batch = batch

            self.batch_lock.release()
            if self.train_lock.locked():
                self.train_lock.release()
                
        buffer_batch = None
        if self.train_lock.locked():
            self.train_lock.release()

class TrainThread( threading.Thread ):
    def __init__( self, batch_lock, train_lock,pool_lock ): 
        """
        """
        threading.Thread.__init__(self)
        self.batch_lock = batch_lock
        self.pool_lock = pool_lock
        self.train_lock = train_lock


    def run( self ):
        """
        """
        global buffer_batch
        while 1:

            self.train_lock.acquire()
            self.batch_lock.acquire()
            
            if buffer_batch == None: 
                break
            cost = train( buffer_batch )
            print 'This is TrainThread, cost = ',cost

            self.batch_lock.release()
            if self.pool_lock.locked():
                self.pool_lock.release()

def test(): 
    """
    """
    pool = datapool( './Data/','data.txt', batch_size)

    # locks
    batch_lock = threading.Lock()
    pool_lock = threading.Lock()
    train_lock = threading.Lock()
    train_lock.acquire()

    # define thread
    datathread = DataThread( pool, batch_lock, train_lock, pool_lock)
    trainthread = TrainThread(batch_lock, train_lock, pool_lock)
    
    # start training 
    starttime = time.time()

    datathread.start()
    trainthread.start()  
    
    datathread.join()
    trainthread.join()

    endtime = time.time()
    print "used time:", endtime - starttime,'s'

if __name__ == "__main__":
    test()

