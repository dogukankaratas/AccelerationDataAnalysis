import os
import pandas as pd
import numpy as np

def ascReader(event, stationCode, direction):
    fileName = "_".join( [event, stationCode , "ap_AAD_Acc",direction+".asc"])
                
    with open( os.path.join( ".","data/1_processedData", fileName) ) as f :
        icerik = f.readlines()
                   
        acc = []
        for satir in icerik : 
            if "SAMPLING_INTERVAL_S:" in satir :
                dt = float( satir.strip().split(":")[-1] )
            try : 
                acc.append( float( satir ))
            except : 
                pass
    accData = pd.DataFrame()
    accData['acc'] = acc
    accData['t'] = np.arange(0, dt*len(acc), dt)
    return accData
