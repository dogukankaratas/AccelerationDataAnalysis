import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go
import targetSpectrumCreator
import numpy as np
from ascReader import ascReader
from st_pages import show_pages_from_config

st.set_page_config("Kahramanmaraş Depremi Verileri 2023", layout='wide')

st.success("Tüm interaktif uygulamalar [SeisKit](https://seiskit.streamlit.app/) sitesinde bulunabilir.", icon="✅")

st.title("Kahramanmaraş Depremi Verileri 2023")
show_pages_from_config()

with st.sidebar:
    st.info("Tüm veriler 10.02.2023 tarihinde AFAD veritabanından ham olarak elde edilmiştir. \
    Bu aracın herhangi bir ticari amacı olmayıp, araştırmacılar ve mühendisler için bilgi amaçlı oluşturulmuştur.", icon="ℹ️")
    st.info("Güncel veriler icin AFAD sitesini takip ediniz.", icon="⚠️")
    st.markdown("**Katkıda Bulunanlar**")
    st.markdown("[Doğukan Karataş](https://www.linkedin.com/in/dogukankaratas/)")
    st.markdown("[Yunus Emre Daşdan](https://www.linkedin.com/in/yunus-emre-dasdan/)")
    st.markdown("[Dr. Ahmet Anıl Dindar](https://www.linkedin.com/in/adindar/)")
    st.markdown("**Referans**")
    st.markdown("[Doğukan Karataş, 2023, Development of Ground Motion Selection and Scaling Framework Compatible with TBEC-2018 (Under Review),\
                 Earthquake and Structural Engineering MSc Dissertation](https://github.com/dogukankaratas/scalepy/blob/main/Development%20of%20Ground%20Motion%20Selection%20and%20Scaling%20Framework%20Compatible%20with%20TBEC-2018%20(Under%20Review).pdf)")

targetSpectrumTab, firstEqTab, secondEqTab = st.tabs(["TBDY-2018 Hedef Spektrum",
                                   "06.02.2023 01:17:32 Pazarcık (Kahramanmaraş) Earthquake MW 7.7",
                                   "06.02.2023 10:24:47 Elbistan (Kahramanmaraş) Earthquake MW 7.6"])

stationFrameURL = pd.read_csv('https://raw.githubusercontent.com/dogukankaratas/dataRepo/main/stationData.csv')
stationFrame1 = pd.read_excel('data/stationData1.xlsx', converters={'ID': str})
stationFrame2 = pd.read_excel('data/stationData2.xlsx', converters={'ID': str})
accFrame = pd.read_excel('data/1_Spectral_Acceleration_Stations.xlsx')
acc2Frame = pd.read_excel('data/2_Spectral_Acceleration_Stations.xlsx')
firstEqLocation = pd.read_json('https://raw.githubusercontent.com/dogukankaratas/dataRepo/main/firstEq.json')
secondEqLocation = pd.read_json('https://raw.githubusercontent.com/dogukankaratas/dataRepo/main/secondEq.json')
icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height":128,
    "anchorY": 128
}

firstEqLocation['icon_data']= None
for i in firstEqLocation.index:
     firstEqLocation['icon_data'][i] = icon_data

secondEqLocation['icon_data']= None
for i in secondEqLocation.index:
     secondEqLocation['icon_data'][i] = icon_data

with firstEqTab:
    layer = pdk.Layer(
        'ScatterplotLayer',
        stationFrameURL,
        get_position=['Longitude', 'Latitude'],
        get_radius=5000,
        get_fill_color=[200, 30, 0, 160],
        pickable=True
    )

    icon_layer = pdk.Layer(
        type='IconLayer',
        data=firstEqLocation,
        get_icon='icon_data',
        get_size=4,
        pickable=False,
        size_scale=15,
        get_position='coordinates'
    )

    # Set the viewport location
    view_state = pdk.ViewState(
            longitude=36, latitude=38, zoom=6
        )
    # Combined all of it and render a viewport
    r = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer, icon_layer],
            tooltip = {
            "html": "<b>Istasyon:</b> {ID} <br/> <b>Vs30:</b> {Vs30} <br/> <b>Enlem:</b> {Latitude} <br/> <b>Boylam:</b> {Longitude} <br/>" ,
            "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
            }
    }
        )

    st.pydeck_chart(r)
    inputCol, accGraphCol = st.columns([1, 2])
    with inputCol:
        provinces = set(stationFrame1['Province'].to_list())
        provinces = [x for x in sorted(provinces)]
        selectedProvince = st.selectbox('Şehir', provinces, 2)
                        
        isSelectedProvince = stationFrame1['Province'] == selectedProvince
        filteredFrame = stationFrame1[isSelectedProvince]

        stations = filteredFrame['ID']
        stations = [x for x in sorted(stations)]
        selectedStation = st.selectbox('İstasyon', stations)

        isSelectedStation = stationFrame1['ID'] == selectedStation
        filteredStationFrame = stationFrame1[isSelectedStation]

        if filteredStationFrame['Vs30'].to_list()[0] == 0:
                    
            st.info("Seçilen istasyon için zemin bilgisi bulunmamaktadır. Bir zemin sınıfı belirtin.")
                    
            soilType = st.selectbox('Zemin Sınıfı', ["ZA", "ZB", "ZC", "ZD", "ZE"], 2)

            if soilType == "ZA":
                selectedVs30 = 1600
            elif soilType == "ZB":
                selectedVs30 = 900
            elif soilType == "ZC":
                selectedVs30 = 500
            elif soilType == "ZD":
                selectedVs30 = 250
            elif soilType == "ZE":
                selectedVs30 = 100            
        else:
            selectedVs30 = filteredStationFrame['Vs30'].to_list()[0]

        selectedLatitude = filteredStationFrame['Latitude'].to_list()[0]
        selectedLongitude = filteredStationFrame['Longitude'].to_list()[0]
            
        with st.form("firstInput"):
            selectedComponent = st.selectbox('İvme Kaydı Bileşeni', ['N-S', 'E-W', 'U-D'])
            graphButton = st.form_submit_button("Grafikleri Gör")

    accDefaultFig = go.Figure()
    accDefaultFig.update_xaxes(
                        title_text = 'Time (s)',
                        showgrid = True,
                        range = [0,3],
                        showline = False,
                        zeroline=False
    )
    accDefaultFig.update_yaxes(
                    title_text = 'Acceleration (g)',
                    range = [0,3],
                    showgrid = True,
                    zeroline=False,
                    showline=False
                )

    accDefaultFig.update_layout(width=980,height=500,
                                    title_text='N-S Bileşeni', title_x=0.5, paper_bgcolor="white")

    defaultFig = go.Figure()
    defaultFig.update_xaxes(
                        title_text = 'Period (sec)',
                        range=[0,3],
                        tickvals=np.arange(0,5.3,0.5),
                        dtick = 1,
                        showgrid = True,
                        zeroline=False,
                        zerolinewidth=1
                    )

    defaultFig.update_yaxes(
                        title_text = 'pSa (g)',
                        range=[0,3],
                        showgrid = True,
                        zeroline=False,
                        zerolinewidth=1
                    )

    defaultFig.update_layout(showlegend=True, template=None,width=750,height=500,
                                            title_text='Yatay Spektrum', title_x=0.5, paper_bgcolor="white",legend=dict(
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
                        zeroline=False,
                        zerolinewidth=1
                    )

    defaultFigVer.update_yaxes(
                        title_text = 'pSa (g)',
                        range=[0,3],
                        showgrid = True,
                        zeroline=False,
                        zerolinewidth=1
                    )

    defaultFigVer.update_layout(showlegend=True, template=None,width=750,height=500,
                                            title_text='Düşey Spektrum', title_x=0.5, paper_bgcolor="white", legend=dict(
                                                                            yanchor="top",
                                                                            x = 1,
                                                                            xanchor="right")
                                            )

    if graphButton:
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
            proData = ascReader("20230206011732", selectedStation, "E", "data/1_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )

            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='E-W Bileşeni', title_x=0.5, paper_bgcolor="white")
        elif selectedComponent == 'N-S':
            proData = ascReader("20230206011732", selectedStation, "N", "data/1_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )

            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='N-S Bileşeni', title_x=0.5, paper_bgcolor="white")
        elif selectedComponent == 'U-D':
            proData = ascReader("20230206011732", selectedStation, "U", "data/1_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )

            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='U-D Bileşeni', title_x=0.5, paper_bgcolor="white")

        valuesDD1, periodDD1, horizontalOrbitsDD1, verticalOrbitsDD1 = targetSpectrumCreator.tbdy2018_spektra("DD1", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetDD1 = pd.DataFrame(columns=['T', 'Sa'])
        defaultTargetDD1['T'] = periodDD1
        defaultTargetDD1['Sa'] = horizontalOrbitsDD1
        valuesDD2, periodDD2, horizontalOrbitsDD2, verticalOrbitsDD2 = targetSpectrumCreator.tbdy2018_spektra("DD2", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetDD2 = pd.DataFrame(columns=['T', 'Sa'])
        defaultTargetDD2['T'] = periodDD2
        defaultTargetDD2['Sa'] = horizontalOrbitsDD2

        defaultFig = go.Figure()

        maxgList = [max(defaultTargetDD1['Sa'].to_list()), max(defaultTargetDD2['Sa'].to_list()), 
                        max(selectedAccFrame[selectedEName].to_list()), max(selectedAccFrame[selectedNName].to_list())]
        maxg = max(maxgList)

        defaultFig.add_trace(go.Scatter(x = defaultTargetDD1['T'],
                                            y=defaultTargetDD1['Sa'],
                                            name='Tasarım Spektrumu (DD1)', line=dict(color='red')))
                                    

        defaultFig.add_trace(go.Scatter(x = defaultTargetDD2['T'],
                                            y=defaultTargetDD2['Sa'],
                                            name='Tasarım Spektrumu (DD2)', line=dict(color='green')))


        defaultFig.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedEName], 
                        name = 'E-W',
                        line = dict(color='black', width=2.5),
                        showlegend=True
                    ))


        defaultFig.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedNName], 
                        name = 'N-S',
                        line = dict(color='black', width=2.5, dash='dot'),
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
                            range=[0,round(maxg, 0) +1],
                            showgrid = True,
                            zeroline=True,
                            zerolinewidth=1
                        )

        defaultFig.update_layout(showlegend=True, template=None,width=700,height=500,
                                                title_text='Yatay Spektrum', title_x=0.5, paper_bgcolor="white", legend=dict(
                                                                                yanchor="top",
                                                                                x = 1,
                                                                                xanchor="right")
                                                )

        valuesVerDD1, periodVerDD1, horizontalOrbitsVerDD1, verticalOrbitsVerDD1 = targetSpectrumCreator.tbdy2018_spektra("DD1", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetVerDD1 = pd.DataFrame(columns=['T', 'Sad'])
        defaultTargetVerDD1['T'] = periodDD1
        defaultTargetVerDD1['Sad'] = verticalOrbitsVerDD1
        valuesVerDD2, periodVerDD2, horizontalOrbitsVerDD2, verticalOrbitsVerDD2 = targetSpectrumCreator.tbdy2018_spektra("DD2", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetVerDD2 = pd.DataFrame(columns=['T', 'Sad'])
        defaultTargetVerDD2['T'] = periodDD2
        defaultTargetVerDD2['Sad'] = verticalOrbitsVerDD2
        defaultFigVer = go.Figure()

        maxgVerList = [max(defaultTargetVerDD1['Sad'].to_list()), max(defaultTargetVerDD2['Sad'].to_list()), max(selectedAccFrame[selectedUName].to_list())]
        maxgVer = max(maxgVerList)

        defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD1['T'],
                                            y=defaultTargetVerDD1['Sad'],
                                            name='Düşey Tasarım Spektrumu (DD1)', line=dict(color='red')))
                                    

        defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD2['T'],
                                            y=defaultTargetVerDD2['Sad'],
                                            name='Düşey Tasarım Spektrumu (DD2)', line=dict(color='green')))


        defaultFigVer.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedUName], 
                        name = 'U-D',
                        line = dict(color='black', width=2.5),
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
                            range=[0,round(maxgVer, 0) +1],
                            showgrid = True,
                            zeroline=True,
                            zerolinewidth=1
                        )

        defaultFigVer.update_layout(showlegend=True, template=None,width=700,height=500,
                                                title_text='Düşey Spektrum', title_x=0.5,  paper_bgcolor="white", legend=dict(
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

with secondEqTab:
    layer = pdk.Layer(
        'ScatterplotLayer',
        stationFrameURL,
        get_position=['Longitude', 'Latitude'],
        get_radius=5000,
        get_fill_color=[200, 30, 0, 160],
        pickable=True
    )

    icon_layer = pdk.Layer(
        type='IconLayer',
        data=secondEqLocation,
        get_icon='icon_data',
        get_size=4,
        pickable=False,
        size_scale=15,
        get_position='coordinates'
    )

    # Set the viewport location
    view_state = pdk.ViewState(
            longitude=36, latitude=38, zoom=6
        )
    # Combined all of it and render a viewport
    r = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer, icon_layer],
            tooltip = {
            "html": "<b>Istasyon:</b> {ID} <br/> <b>Vs30:</b> {Vs30} <br/> <b>Enlem:</b> {Latitude} <br/> <b>Boylam:</b> {Longitude} <br/>" ,
            "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
            }
    }
        )

    st.pydeck_chart(r)
    inputCol, accGraphCol = st.columns([1, 2])
    with inputCol:
        provinces = set(stationFrame2['Province'].to_list())
        provinces = [x for x in sorted(provinces)]
        selectedProvince = st.selectbox('Şehir ', provinces, 2)
                        
        isSelectedProvince = stationFrame2['Province'] == selectedProvince
        filteredFrame = stationFrame2[isSelectedProvince]

        stations = filteredFrame['ID']
        stations = [x for x in sorted(stations)]
        selectedStation = st.selectbox('İstasyon ', stations)

        isSelectedStation = stationFrame2['ID'] == selectedStation
        filteredStationFrame = stationFrame2[isSelectedStation]

        if filteredStationFrame['Vs30'].to_list()[0] == 0:
                    
            st.info("Seçilen istasyon için zemin bilgisi bulunmamaktadır. Bir zemin sınıfı belirtin.")
                    
            soilType = st.selectbox('Zemin Sınıfı ', ["ZA", "ZB", "ZC", "ZD", "ZE"], 2)

            if soilType == "ZA":
                selectedVs30 = 1600
            elif soilType == "ZB":
                selectedVs30 = 900
            elif soilType == "ZC":
                selectedVs30 = 500
            elif soilType == "ZD":
                selectedVs30 = 250
            elif soilType == "ZE":
                selectedVs30 = 100            
        else:
            selectedVs30 = filteredStationFrame['Vs30'].to_list()[0]

        selectedLatitude = filteredStationFrame['Latitude'].to_list()[0]
        selectedLongitude = filteredStationFrame['Longitude'].to_list()[0]
            
        with st.form("firstInput2"):
            selectedComponent = st.selectbox('İvme Kaydı Bileşeni ', ['N-S', 'E-W', 'U-D'])
            graphButton = st.form_submit_button("Grafikleri Gör ")

    accDefaultFig = go.Figure()
    accDefaultFig.update_xaxes(
                        title_text = 'Time (s)',
                        showgrid = True,
                        showline = False,
                        zeroline = False
    )
    accDefaultFig.update_yaxes(
                    title_text = 'Acceleration (g)',
                    showgrid = True,
                    showline=False,
                    zeroline = False
                )

    accDefaultFig.update_layout(width=980,height=500,
                                    title_text='N-S Bileşeni', title_x=0.5, paper_bgcolor="white")

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
                                            title_text='Yatay Spektrum', title_x=0.5, paper_bgcolor="white",legend=dict(
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
                                            title_text='Düşey Spektrum', title_x=0.5, paper_bgcolor="white", legend=dict(
                                                                            yanchor="top",
                                                                            x = 1,
                                                                            xanchor="right")
                                            )

    if graphButton:
        selectedAccFrame = pd.DataFrame()
        selectedAccFrame['Period'] = acc2Frame['Period'].to_list()
        selectedEName = selectedStation + '-E_(g)'
        selectedNName = selectedStation + '-N_(g)'
        selectedUName = selectedStation + '-U_(g)'
        try:
            selectedAccFrame[selectedEName] = acc2Frame[selectedEName].to_list()
            selectedAccFrame[selectedNName] = acc2Frame[selectedNName].to_list()
            selectedAccFrame[selectedUName] = acc2Frame[selectedUName].to_list()   
        except:
            st.warning("Bu istasyon için veri bulunamamıştır.")

        if selectedComponent == 'E-W':
            proData = ascReader("20230206102447", selectedStation, "E", "data/2_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )

            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='E-W Bileşeni', title_x=0.5, paper_bgcolor="white")
        elif selectedComponent == 'N-S':
            proData = ascReader("20230206102447", selectedStation, "N", "data/2_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )
            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='N-S Bileşeni', title_x=0.5, paper_bgcolor="white")
        elif selectedComponent == 'U-D':
            proData = ascReader("20230206102447", selectedStation, "U", "data/2_processedData")
            accDefaultFig = go.Figure()
            accDefaultFig.add_trace(go.Scatter(
                x = proData['t'],
                y = proData['acc'],
                line=dict(color='blue')
            ))
            accDefaultFig.update_xaxes(
                                title_text = 'Time (s)',
                                showgrid = True,
                                showline = False
            )
            accDefaultFig.update_yaxes(
                            title_text = 'Acceleration (g)',
                            showgrid = True,
                            showline=False
                        )

            accDefaultFig.update_layout(width=980,height=500,
                                            title_text='U-D Bileşeni', title_x=0.5, paper_bgcolor="white")

        valuesDD1, periodDD1, horizontalOrbitsDD1, verticalOrbitsDD1 = targetSpectrumCreator.tbdy2018_spektra("DD1", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetDD1 = pd.DataFrame(columns=['T', 'Sa'])
        defaultTargetDD1['T'] = periodDD1
        defaultTargetDD1['Sa'] = horizontalOrbitsDD1
        valuesDD2, periodDD2, horizontalOrbitsDD2, verticalOrbitsDD2 = targetSpectrumCreator.tbdy2018_spektra("DD2", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetDD2 = pd.DataFrame(columns=['T', 'Sa'])
        defaultTargetDD2['T'] = periodDD2
        defaultTargetDD2['Sa'] = horizontalOrbitsDD2

        defaultFig = go.Figure()

        maxgList = [max(defaultTargetDD1['Sa'].to_list()), max(defaultTargetDD2['Sa'].to_list()), 
                        max(selectedAccFrame[selectedEName].to_list()), max(selectedAccFrame[selectedNName].to_list())]
        maxg = max(maxgList)

        defaultFig.add_trace(go.Scatter(x = defaultTargetDD1['T'],
                                            y=defaultTargetDD1['Sa'],
                                            name='Tasarım Spektrumu (DD1)', line=dict(color='red')))
                                    

        defaultFig.add_trace(go.Scatter(x = defaultTargetDD2['T'],
                                            y=defaultTargetDD2['Sa'],
                                            name='Tasarım Spektrumu (DD2)', line=dict(color='green')))


        defaultFig.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedEName], 
                        name = 'E-W',
                        line = dict(color='black', width=2.5),
                        showlegend=True
                    ))


        defaultFig.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedNName], 
                        name = 'N-S',
                        line = dict(color='black', width=2.5, dash='dot'),
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
                            range=[0,round(maxg, 0) +1],
                            showgrid = True,
                            zeroline=True,
                            zerolinewidth=1
                        )

        defaultFig.update_layout(showlegend=True, template=None,width=700,height=500,
                                                title_text='Yatay Spektrum', title_x=0.5, paper_bgcolor="white", legend=dict(
                                                                                yanchor="top",
                                                                                x = 1,
                                                                                xanchor="right")
                                                )

        valuesVerDD1, periodVerDD1, horizontalOrbitsVerDD1, verticalOrbitsVerDD1 = targetSpectrumCreator.tbdy2018_spektra("DD1", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetVerDD1 = pd.DataFrame(columns=['T', 'Sad'])
        defaultTargetVerDD1['T'] = periodDD1
        defaultTargetVerDD1['Sad'] = verticalOrbitsVerDD1
        valuesVerDD2, periodVerDD2, horizontalOrbitsVerDD2, verticalOrbitsVerDD2 = targetSpectrumCreator.tbdy2018_spektra("DD2", selectedVs30, [selectedLatitude, selectedLongitude], False, False, False)
        defaultTargetVerDD2 = pd.DataFrame(columns=['T', 'Sad'])
        defaultTargetVerDD2['T'] = periodDD2
        defaultTargetVerDD2['Sad'] = verticalOrbitsVerDD2
        defaultFigVer = go.Figure()

        maxgVerList = [max(defaultTargetVerDD1['Sad'].to_list()), max(defaultTargetVerDD2['Sad'].to_list()), max(selectedAccFrame[selectedUName].to_list())]
        maxgVer = max(maxgVerList)

        defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD1['T'],
                                            y=defaultTargetVerDD1['Sad'],
                                            name='Düşey Tasarım Spektrumu (DD1)', line=dict(color='red')))
                                    

        defaultFigVer.add_trace(go.Scatter(x = defaultTargetVerDD2['T'],
                                            y=defaultTargetVerDD2['Sad'],
                                            name='Düşey Tasarım Spektrumu (DD2)', line=dict(color='green')))


        defaultFigVer.add_trace(go.Scatter(
                        x = selectedAccFrame['Period'],
                        y = selectedAccFrame[selectedUName], 
                        name = 'U-D',
                        line = dict(color='black', width=2.5),
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
                            range=[0,round(maxgVer, 0) +1],
                            showgrid = True,
                            zeroline=True,
                            zerolinewidth=1
                        )

        defaultFigVer.update_layout(showlegend=True, template=None,width=700,height=500,
                                                title_text='Düşey Spektrum', title_x=0.5,  paper_bgcolor="white", legend=dict(
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
        
with targetSpectrumTab:
    st.markdown("# Bu uygulama [SeisKit](https://seiskit.streamlit.app/) sitesine taşınmıştır.")
