########################################################
# TURKISH BUILDING SEISMIC CODE 2018 RESPONSE SPECTRUM #
########################################################
"""
2021_1027-AAD: Initially coded by AAD (adindar@gtu.edu.tr)
"""
########################################################
#%% IMPORT MODULES
# ımporting modules
# 
import os, pandas as pd,  numpy as np , datetime as dt , math  ,  scipy.interpolate as interp
from scipy.interpolate import interp1d

#========================================================================================================
def getSpectraValue(lat , lon , intensity = "DD2"):
    """
    Interpolates the "Ss","S1","PGA","PGV" values from the "AFAD_TDTH_parametre.csv" file
    -ARGUMENTS -------------------------------------
    lat : latitude
    lon : longitude
    intensity : Earthquake Level; any of the given list "DD1" , "DD2" , "DD3" , "DD4". Defatuls is "DD2"

    -RETURN -------------------------------------
    spectral_value_dict : spectral values of "Ss","S1","PGA","PGV" at the given location. 
    """
     # AFAD SPECTRAL VALUES
    """
    AFAD Turkish Seismic Hazard Spectral Values
    """
    afad_spectra_params_df = pd.read_csv("data/AFAD_TDTH_parametre.csv")   

    # Grid locattions
    x = afad_spectra_params_df["LAT"].to_list()
    y = afad_spectra_params_df["LON"].to_list()
    
    # Spectral values dictionary
    spectral_value_dict = {}
    for column_name in ["Ss","S1","PGA","PGV"]:

        z = afad_spectra_params_df[ f"{column_name}-{intensity}"].to_list()

        interpolator = interp.CloughTocher2DInterpolator( np.array([x,y]).T , z)

        spectral_value = np.round( interpolator( lat,lon)  , 3 )
        
        spectral_value_dict[ column_name ] = spectral_value
    # Return
    return( spectral_value_dict)

#========================================================================================================
def show_spectral_values( spectral_value_dict ):
    """
    Printing the spectral values estimated at the given location.         
    """
    [ print( f"{column_name} { item }") for column_name , item in spectral_value_dict.items() ]

#========================================================================================================
def soilclass(vs30) :
    # Soil Amplification values
    vs30_values = [ 0 , 180 , 360 , 760 , 1_500 , 20_000 ]
    soil_class_list = [ "ZE" , "ZD" , "ZC" , "ZB" , "ZA" ]
    vs_limit , count = 0 , 0
    while vs30 >= vs_limit:
        soilClass =  soil_class_list[ count ]
        count += 1
        vs_limit = vs30_values[ count]
    
    return( soilClass)

#========================================================================================================
def get_spectral_ordinates( soil_class , spectral_value_dict , period_list = 0 ) :
    """
    -ARGUMENTS -------------------------------------
        soil_class
        spectral_value_dict : 
        period_list = 0 for default values, otherwise provide your period list
    -RETURN -------------------------------------
        period_list :
        spectral_orbits :
        AFAD_spectral_values_dict :
    """

    # Determine the short and 1 sec spectral values. 
    if spectral_value_dict == {} : 
        print( "Provide location coordinates to estimate the spectral values, first. Then run self.get_spectral_ordinates() method.")
        raise()
    else:
        Ss = spectral_value_dict["Ss"] 
        S1 = spectral_value_dict["S1"] 
    

    # Spectral values
    Ss_range = [0.25 , 0.50 , 0.75, 1.00 , 1.25 , 1.50 ]

    FS_table = {"ZA": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZB": [0.9 , 0.9 , 0.9 , 0.9 , 0.9 , 0.9], 
                "ZC": [1.3 , 1.3 , 1.2 , 1.2 , 1.2 , 1.2],
                "ZD": [1.6 , 1.4 , 1.2 , 1.1 , 1.0 , 1.0],
                "ZE": [2.4 , 1.7 , 1.3 , 1.1 , 0.9 , 0.8]}

    S1_range = [0.10 , 0.20 , 0.30, 0.40 , 0.50 , 0.60 ]

    F1_table = {"ZA": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZB": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZC": [1.5 , 1.5 , 1.5 , 1.5 , 1.5 , 1.4],
                "ZD": [2.4 , 2.2 , 2.0 , 1.9 , 1.8 , 1.7],
                "ZE": [4.2 , 3.3 , 2.8 , 2.4 , 2.2 , 2.0]}

    # Short period
    if Ss < Ss_range[0]:
        Fs = FS_table[soil_class][0]
        SDs = Ss * Fs
    elif Ss > Ss_range[-1]:
        Fs = FS_table[soil_class][-1]
        SDs = Ss * Fs    
    else:
        FS_satir = interp1d(Ss_range, FS_table[soil_class], kind='linear')
        FS_katsayisi = FS_satir(Ss)
        Fs = round( float(FS_katsayisi) , 2) 
        SDs = Ss * Fs
    # 1sec period
    if S1 < S1_range[0] :
        F1 = F1_table[soil_class][0]
        SD1 = S1 * F1
    elif S1 > S1_range[-1]:
        F1 = F1 = F1_table[soil_class][-1]
        SD1 = S1 * F1
    else:    
        F1_satir = interp1d(S1_range, F1_table[soil_class], kind='linear')
        F1_katsayisi = F1_satir(S1)
        F1 = round(float(F1_katsayisi) , 2)
        SD1 = S1 * F1

    # DTS
    if SDs < .33 : 
        DTS = 4
    elif SDs >= 0.33 and SDs < 0.50 : 
        DTS = 3
    elif SDs >= 0.50 and SDs < 0.75 :
        DTS = 2 
    else : 
        DTS = 1

    # Corner period values
    TA = 0.2 * SD1 / SDs
    TB = SD1 / SDs
    TL = 6

    # Function for lateral spectral values
    def spektra_yatay(T,SDs,SD1, TA, TB , TL):  
        if T < TA :
            return((0.4 + 0.6*(T/TA))*SDs)
        elif T >= TA and T <= TB:
            return(SDs)
        elif T> TB and T <= TL:
            return(SD1 / T)
        elif T> TL:
            return(SD1*TL/(T**2))

   # Function for vertical spectral values

    def spektra_dusey(T,SDs,SD1, TA, TB , TL):  
        TAD , TBD , TLD = TA / 3 , TB / 3 , TL / 2
        if T < TAD :
            return(( 0.32 + 0.48*(T/TAD))*SDs)
        elif T >= TAD and T <= TBD:
            return(0.8 * SDs)
        elif T> TBD and T <= TLD:
            return( 0.8 * SDs * TBD / T)
        elif T> TLD:
            return( np.nan )

    # Creating the spectrum
    if period_list == 0  :
        # period_list  = [ item  for item in np.arange(0.0 , 5 , 0.01)]
        period_list = np.linspace( 0.0 , 5.0 , 1001)

    spectral_yatay_orbits = [ spektra_yatay(period,SDs,SD1, TA, TB , TL) for period in period_list ]
    spectral_dusey_orbits = [ spektra_dusey(period,SDs,SD1, TA, TB , TL) for period in period_list ]

    pga = spectral_value_dict["PGA"]
    pgv = spectral_value_dict["PGV"]

    AFAD_spectral_values_dict = {  "Ss":Ss , "S1":S1 , "PGA":pga, "PGV": pgv, "Fs":Fs, "F1":F1, "SDs":round(SDs, 3) , "SD1":round(SD1, 3) , "TA":round(TA,2) ,"TB":round(TB,2), "TL":round(TL,2) , "DTS" : DTS , "Soil Class" : soil_class}

    # Return
    return( period_list , spectral_yatay_orbits  , spectral_dusey_orbits , AFAD_spectral_values_dict )

#========================================================================================================
def spectra_plot(intensity, period_list , spectral_orbits , soil_class , lat , lon ):
    """
    Visualization of spectra
    """
    if spectral_orbits == [] :
        print( "Please run self.get_spectral_ordinates() method first")
        raise()
    
#========================================================================================================

def reduced_specta(  period_list , spectral_orbits , D = 0 , I = 1 , R = 1   , TB = 1) :
    """
    -ARGUMENTS -------------------------------------
        period_list : period values (list) 
        spectral_orbits : spectral values (list)
        TB = 1 : Corner period (Float)
        D = 0 : Overstrength (Int)
        I = 1 : Importance factor (Int)
        R = 1 : Load reduction factor (Int)    
    -RETURN -------------------------------------
        spectral_orbits_reduced : Reduced spectral values ( list )
    """
    spectral_orbits_reduced = []
    Ra = []
    for T , Sae in zip( period_list , spectral_orbits ) : 
        if T > TB: 
            Ra.append( R/ I )
            spectral_orbits_reduced.append(  Sae / (R / I) )
        else : 

            Ra.append( D + ( R/I - D ) * T / TB)
            spectral_orbits_reduced.append( Sae / ( D + ( R/I - D ) * T / TB ) )
    

    return( spectral_orbits_reduced, Ra)
#========================================================================================================
def tbdy2018_spektra( intensity , vs30 , coordinates , show_AFAD_values= True , show_yatay_plot = True , show_dusey_plot = True , period_list = 0 , reduced_spectrum = False , D = 0 , I = 1 , R = 1 ) :
    """
    This function estimates the spectral values of a given coordinate in accordance to Turkish Building Earthquake Code 2018. 
    The function  derives the spectral values for TR grid from "AFAD_TDTH_parametre.csv" file. Please make sure you the file is in the same folder with this file. 
    -ARGUMENTS -------------------------------------

        intensity : (Str) one of "DD1","DD2","DD3","DD4
        vs30 : (float) m/s
        coordinates : (list) [lat , lon]
        show_plot = True
        period_list =  0 for default period range, otherwise provide your own list
        reduced_spectrum = False for no design spectrum, True for reduced design spectrum. 
        D = 0 : Overstrength (Int)
        I = 1 : Importance factor (Int)
        R = 1 : Load reduction factor (Int)

    -RETURN -------------------------------------

        AFAD_spectral_values_dict
        soil_class: (Str) one of "ZA","ZB","ZC","ZD" but not "ZE"
        period_list: (list) period values in sec
        spectral_orbits : (list) float spectral values in g.
        spectral_orbits_reduced : (list) float reduced spectral values in g.
        Ra : (list) reduction factors.
    """
    # Coordinates
    lat, lon = coordinates[0] , coordinates[1]
    # Call the functions 
    spectral_value_dict = getSpectraValue(lat , lon , intensity )

    
    soil_class = soilclass( vs30)

    period_list , spectral_yatay_orbits , spectral_dusey_orbits , AFAD_spectral_values_dict = get_spectral_ordinates( soil_class , spectral_value_dict , period_list)

    if show_yatay_plot: spectra_plot( intensity, period_list , spectral_yatay_orbits , soil_class , lat , lon ) 
    if show_dusey_plot: spectra_plot( intensity, period_list , spectral_dusey_orbits , soil_class , lat , lon ) 


    if show_AFAD_values == True: show_spectral_values(AFAD_spectral_values_dict)

    # Return
    if reduced_spectrum == True : 

        spectral_orbits_reduced , Ra =  reduced_specta(  period_list , spectral_yatay_orbits , D , I ,  R , TB = AFAD_spectral_values_dict["TB"]  )
        spectral_orbits_reduced = [ round( item , 4) for item in spectral_orbits_reduced] 
        period_list = [0] +  [ round( item , 2) for item in period_list]
        spectral_yatay_orbits = AFAD_spectral_values_dict["PGA"] + [round( item , 4) for item in spectral_yatay_orbits]

        return( AFAD_spectral_values_dict , soil_class , period_list , spectral_yatay_orbits , spectral_orbits_reduced , Ra)

    else : 
        period_list = [ round( item , 3) for item in period_list]
        spectral_yatay_orbits = [round( item , 5 ) for item in spectral_yatay_orbits]

        return( AFAD_spectral_values_dict  , period_list , spectral_yatay_orbits , spectral_dusey_orbits)
