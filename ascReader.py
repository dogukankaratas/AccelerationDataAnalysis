
import os
import datetime as datetime
import pandas as pd
import numpy as np

event = "20230206011732"
stationCode = '0118'
direction = 'E'

def ascReader(event, stationCode, direction):
    fileName = "_".join( [event, stationCode , "ap_AAD_Acc",direction+".asc"])

    print( f"{ fileName } işlemdedir")
                
    with open( os.path.join( ".","processedData", fileName) ) as f :
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

acc = ascReader(event, stationCode, 'E')
import plotly.graph_objects as go

accDefaultFig = go.Figure()
accDefaultFig.add_trace(go.Scatter(
        x = acc['t'],
        y = acc['acc'],
        line=dict(color='blue')
    ))
