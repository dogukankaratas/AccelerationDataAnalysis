import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go
import targetSpectrumCreator
import numpy as np
from ascReader import ascReader

st.set_page_config("Kahramanmaraş Depremi Verileri", layout='wide')

stationFrame = pd.read_csv('stationData.csv', sep=';')
accFrame = pd.read_excel('1_Spectral_Acceleration_Stations.xlsx')

layer = pdk.Layer(
    'HexagonLayer',  
    stationFrame,
    get_position=['Longitude', 'Latitude'],
    auto_highlight=False,
    radius=7000,
    pickable=True,
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=36, latitude=38, zoom=6
)
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer]   
)

st.pydeck_chart(r)
inputCol, accGraphCol = st.columns([1, 2])
with inputCol:
    provinces = set(stationFrame['Province'].to_list())
    provinces = [x for x in sorted(provinces)]
    selectedProvince = st.selectbox('Şehir', provinces, 2)
                
    isSelectedProvince = stationFrame['Province'] == selectedProvince
    filteredFrame = stationFrame[isSelectedProvince]

    stations = filteredFrame['ID']
    selectedStation = st.selectbox('İstasyon', stations)

    isSelectedStation = stationFrame['ID'] == selectedStation
    filteredStationFrame = stationFrame[isSelectedStation]

    if filteredStationFrame['Vs30'].to_list()[0] == 0:
            
        st.info("Seçilen istasyon için zemin bilgisi bulunmamaktadır. Bir zemin sınıfı belirtin.")
            
        soilType = st.selectbox('Zemin Sınıfı', ["ZA", "ZB", "ZC", "ZD", "ZE"], 2)

        selectedLatitude = filteredStationFrame['Latitude'].to_list()[0]
        selectedLongitude = filteredStationFrame['Longitude'].to_list()[0]
        if filteredStationFrame['Vs30'].to_list()[0] == 0:
            selectedVs30 = soilType
        else:
            selectedVs30 = filteredStationFrame['Vs30'].to_list()[0]
    
    selectedComponent = st.selectbox('İvme Kaydı Bileşeni', ['N-S', 'E-W', 'U-D'])

accDefaultFig = go.Figure()
accDefaultFig.update_xaxes(
                    showgrid = True,
                    showline = False
)
accDefaultFig.update_yaxes(
                title_text = 'Acceleration',
                showgrid = True,
                showline=False
            )

accDefaultFig.update_layout(width=980,height=500,
                            title_text='N-S Bileşeni', title_x=0.5)

defaultFig = go.Figure()
defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,3],
                tickvals=np.arange(0,5.3,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFig.update_yaxes(
                title_text = 'pSa (g)',
                range=[0,3],
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFig.update_layout(showlegend=True, template=None,width=750,height=500,
                                    title_text='Yatay Spektrum', title_x=0.5, legend=dict(
                                                                    yanchor="top",
                                                                    x = 1,
                                                                    xanchor="right")
                                    )

defaultFigVer = go.Figure()
defaultFigVer.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,3],
                tickvals=np.arange(0,5.3,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFigVer.update_yaxes(
                title_text = 'pSa (g)',
                range=[0,3],
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFigVer.update_layout(showlegend=True, template=None,width=750,height=500,
                                    title_text='Düşey Spektrum', title_x=0.5, legend=dict(
                                                                    yanchor="top",
                                                                    x = 1,
                                                                    xanchor="right")
                                    )

selectedAccFrame = pd.DataFrame()
selectedAccFrame['Period'] = accFrame['Period'].to_list()
selectedEName = selectedStation + '-E_(g)'
selectedNName = selectedStation + '-N_(g)'
selectedUName = selectedStation + '-U_(g)'
try:
    selectedAccFrame[selectedEName] = accFrame[selectedEName].to_list()
    selectedAccFrame[selectedNName] = accFrame[selectedNName].to_list()
    selectedAccFrame[selectedUName] = accFrame[selectedUName].to_list()   
except:
    st.warning("Bu istasyon için veri bulunamamıştır.")

if selectedComponent == 'E-W':
    proData = ascReader("20230206011732", selectedStation, "E")
    accDefaultFig = go.Figure()
    accDefaultFig.add_trace(go.Scatter(
        x = proData['t'],
        y = proData['acc'],
        line=dict(color='blue')
    ))
    accDefaultFig.update_xaxes(
                        showgrid = True,
                        showline = False
    )
    accDefaultFig.update_yaxes(
                    title_text = 'Acceleration',
                    showgrid = True,
                    showline=False
                )

    accDefaultFig.update_layout(width=980,height=500,
                                title_text='E-W Bileşeni', title_x=0.5)
elif selectedComponent == 'N-S':
    proData = ascReader("20230206011732", selectedStation, "N")
    accDefaultFig = go.Figure()
    accDefaultFig.add_trace(go.Scatter(
        x = proData['t'],
        y = proData['acc'],
        line=dict(color='blue')
    ))
    accDefaultFig.update_xaxes(
                        showgrid = True,
                        showline = False
    )
    accDefaultFig.update_yaxes(
                    title_text = 'Acceleration',
                    showgrid = True,
                    showline=False
                )

    accDefaultFig.update_layout(width=980,height=500,
                                title_text='N-S Bileşeni', title_x=0.5)
elif selectedComponent == 'U-D':
    proData = ascReader("20230206011732", selectedStation, "U")
    accDefaultFig = go.Figure()
    accDefaultFig.add_trace(go.Scatter(
        x = proData['t'],
        y = proData['acc'],
        line=dict(color='blue')
    ))
    accDefaultFig.update_xaxes(
                        showgrid = True,
                        showline = False
    )
    accDefaultFig.update_yaxes(
                    title_text = 'Acceleration',
                    showgrid = True,
                    showline=False
                )

    accDefaultFig.update_layout(width=980,height=500,
                                title_text='U-D Bileşeni', title_x=0.5)

defaultTargetDD1 = targetSpectrumCreator.targetSpectrum(selectedLatitude, selectedLongitude, selectedVs30, "DD1")
defaultTargetDD2 = targetSpectrumCreator.targetSpectrum(selectedLatitude, selectedLongitude, selectedVs30, "DD2")
defaultFig = go.Figure()

defaultFig.add_trace(go.Scatter(x = defaultTargetDD1['T'],
                                y=defaultTargetDD1['Sa'],
                                name='Tasarım Spektrumu (DD1)', line=dict(color='black')))
                        

defaultFig.add_trace(go.Scatter(x = defaultTargetDD2['T'],
                                y=defaultTargetDD2['Sa'],
                                name='Tasarım Spektrumu (DD2)', line=dict(color='gray')))


defaultFig.add_trace(go.Scatter(
            x = selectedAccFrame['Period'],
            y = selectedAccFrame[selectedEName], 
            name = 'E-W',
            line = dict(color='red'),
            showlegend=True
        ))


defaultFig.add_trace(go.Scatter(
            x = selectedAccFrame['Period'],
            y = selectedAccFrame[selectedNName], 
            name = 'N-S',
            line = dict(color='blue'),
            showlegend=True
        ))

defaultFig.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,3],
                tickvals=np.arange(0,3.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFig.update_yaxes(
                title_text = 'pSa (g)',
                range=[0,3],
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFig.update_layout(showlegend=True, template=None,width=750,height=500,
                                    title_text='Yatay Spektrum', title_x=0.5, legend=dict(
                                                                    yanchor="top",
                                                                    x = 1,
                                                                    xanchor="right")
                                    )

defaultTargetVerDD1 = targetSpectrumCreator.verticalTargetSpectrum(selectedLatitude, selectedLongitude, selectedVs30, "DD1")
defaultTargetVerDD2 = targetSpectrumCreator.verticalTargetSpectrum(selectedLatitude, selectedLongitude, selectedVs30, "DD2")
defaultFigVer = go.Figure()

defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD1['T'],
                                y=defaultTargetVerDD1['Sad'],
                                name='Düşey Tasarım Spektrumu (DD1)', line=dict(color='black')))
                        

defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD2['T'],
                                y=defaultTargetVerDD2['Sad'],
                                name='Düşey Tasarım Spektrumu (DD2)', line=dict(color='gray')))


defaultFigVer.add_trace(go.Scatter(
            x = selectedAccFrame['Period'],
            y = selectedAccFrame[selectedUName], 
            name = 'U-D',
            line = dict(color='orange'),
            showlegend=True
        ))

defaultFigVer.update_xaxes(
                title_text = 'Period (sec)',
                range=[0,3],
                tickvals=np.arange(0,3.5,0.5),
                dtick = 1,
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFigVer.update_yaxes(
                title_text = 'pSa (g)',
                range=[0,3],
                showgrid = True,
                zeroline=True,
                zerolinewidth=1
            )

defaultFigVer.update_layout(showlegend=True, template=None,width=750,height=500,
                                    title_text='Düşey Spektrum', title_x=0.5, legend=dict(
                                                                    yanchor="top",
                                                                    x = 1,
                                                                    xanchor="right")
                                    )

with accGraphCol:
    st.plotly_chart(accDefaultFig)

horCol, verCol = st.columns(2)
with horCol:
    st.plotly_chart(defaultFig)
with verCol:
    st.plotly_chart(defaultFigVer)