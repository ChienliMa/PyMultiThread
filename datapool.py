import numpy as np
import cv2

class datapool( object ):
    
    def __init__( self, path, list_file, batch_size ):
        """
        abs path
        """
        self.path = path
        self.list_file = list_file
        self.batch_size = batch_size

    def get( self ):
        """
        """
        sample_list = open( self.path + self.list_file, 'r')
        img_size = self.batch_size[ -2: ]
        batch = np.zeros(self.batch_size )
        batch_i = 0
        
        for sample_file in sample_list:
            # get rid of the format control symble
            sample_file = sample_file.rstrip()
            
            sample = cv2.imread( self.path + sample_file )
            sample = cv2.resize( sample, img_size )
            sample = np.transpose( sample, [2,0,1] )
            
            batch[ batch_i, ... ] = sample
            batch_i += 1
            
            if batch_i == self.batch_size[0]:
                # return one batch and reset batch
                yield batch
                batch_i = 0
                batch = np.zeros( self.batch_size )
    def batch_size( self, batch_size ):
        self.batch_size = batch_size
