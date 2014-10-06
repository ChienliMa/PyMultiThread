import multiprocessing
from multiprocessing import Process
import time 
from datapool import datapool


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

def dataprocess( datapool, batch_lock, 
                 train_lock, pool_lock, buffer ):
    """
    """
    for batch in datapool.get():
        pool_lock.acquire()
        batch_lock.acquire()
        
        buffer.put(batch)
        
        batch_lock.release()
        train_lock.release()
    buffer.put( None )
    train_lock.release()

def trainprocess( batch_lock, train_lock,pool_lock, buffer ):
    """
    """
    while 1:
        train_lock.acquire()
        batch_lock.acquire()
        
        buffer_batch = buffer.get()
        if buffer_batch == None: 
            break
        cost = train( buffer_batch )
        print 'This is Training process, cost = ',cost

        batch_lock.release()
        pool_lock.release()

def test(): 
    """
    """
    batch_size = (4,3,128,128)
    pool = datapool( './Data/','data.txt', batch_size)

    buffer = multiprocessing.Queue()

    batch_lock = multiprocessing.Lock()
    pool_lock = multiprocessing.Lock()
    train_lock = multiprocessing.Lock()
    train_lock.acquire()

    args0 = ( pool, batch_lock, train_lock, 
                 pool_lock, buffer )
    args1 = ( batch_lock, train_lock,pool_lock, buffer )
    
    data = Process(target=dataprocess,args=args0)
    train = Process(target=trainprocess,args=args1)
    
    starttime = time.time()

    data.start()
    train.start()  
    
    data.join()
    train.join()

    endtime = time.time()

    print "used time:", endtime - starttime,'s'

if __name__ == "__main__":
    test()

