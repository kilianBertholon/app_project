import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema

def liste_tests():
    dossier_tests = 'C:/Users/kilia/Desktop/app_projet/test_finaux'  # Spécifiez le dossier où se trouvent vos fichiers CSV
    fichiers = os.listdir(dossier_tests)
    fichiers_csv = [f for f in fichiers if f.endswith('.csv')]
    return fichiers_csv

dossier_tests = 'C:/Users/kilia/Desktop/app_projet/test_finaux'  # Spécifiez le dossier où se trouvent vos fichiers CSV

def analyse_capteur(fichiers_csv):

    data = pd.read_csv(os.path.join(dossier_tests, fichiers_csv), skiprows=10)
    accel_x = data['Acc_X']
    accel_y = data['Acc_Y']
    accel_z = data['Acc_Z']
    
    gyro_x = data['Gyr_X']
    gyro_y = data['Gyr_Y']
    gyro_z = data['Gyr_Z']
    
    mag_x = data['Mag_X']
    mag_y = data['Mag_Y']
    mag_z = data['Mag_Z']
    time = np.arange((data.shape[0]))/ 60.0  # Convertit les nombres de frame en temps en secondes
    
    accel_magnitude = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    mag_magnitude = np.sqrt(mag_x**2 + mag_y**2 + mag_z**2)
    
    def butter_lowpass_filter(data, cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        y = filtfilt(b, a, data)
        return y
    
    cutoff = 8 # Fréquence de coupure en Hz
    fs = 60  # Fréquence d'échantillonnage du capteur en Hz
    order = 2  # Ordre du filtre
    
    accel_magnitude_filtered = butter_lowpass_filter(accel_magnitude, cutoff, fs, order)
    
    slopes = np.diff(accel_magnitude_filtered)/np.diff(time)  
    
    threshold = 100
    positive_slope = slopes > threshold
    window_size = 5
    start_index = None
    for i in range(len(slopes) - window_size):
        if np.all(positive_slope[i:i+window_size]):
            start_index = i
            break
    if start_index is not None:
        print("Le début du signal est détecté à l'index", start_index)
    else:
        print("Le début du signal n'a pas été détecté.")
    slopes = slopes[start_index:]
    
    percentile_90 = np.percentile(slopes, 90)
    percentile_50 = np.percentile(slopes, 50)
    threshold = -250
    # Trouver les indices des pics minimums
    minima_indices = argrelextrema(slopes, np.less, order = 10)[0]
    minima_indices = minima_indices[slopes[minima_indices] < threshold]
    
    peak_height_max = (percentile_90 + percentile_50) / 2
    
    
    peaks, _ = find_peaks(slopes, height=peak_height_max)
    
    #temps de contact au sol
    taille_x = len(peaks)
    taille_y = len(minima_indices)
    
    # Remplir le tableau plus petit avec des zéros
    if taille_x > taille_y:
        minima_indices = np.pad(minima_indices, (0, taille_x - taille_y), mode='constant')
    else:
        peaks = np.pad(peaks, (0, taille_y - taille_x), mode='constant')
    
    # Créer un tableau en colonnes à partir de x et y
    tableau = np.column_stack((peaks, minima_indices))
    
    # Créer une nouvelle colonne avec la soustraction entre les données de la colonne 1 et la colonne 0
    tableau = np.column_stack((tableau, abs((tableau[:, 1] - tableau[:, 0]))/60))
    
    ground_contact = tableau[:, 2]
    
    # Tracer les données d'accélération
    plt.plot(slopes, label="Pente courbe d'accélérations")
    
    # Tracer les pics avec des croix
    plt.plot(peaks, slopes[peaks], "x", label="Pics max détectés")
    plt.plot(minima_indices, slopes[minima_indices], "o", label="Pics min détectés")
    
    # Légende et étiquettes des axes
    plt.legend()
    plt.xlabel("Échantillons")
    plt.ylabel("Pente courbe d'accélérations")
    
    print(ground_contact)
    median_ground_contact = np.median(ground_contact)
    
    print("Médiane temps de contact au sol :", median_ground_contact)
    
    tps_course = round((len(slopes)/60), 3)
    print("temps de course en s :", tps_course)
    
    distance = 30
    
    vitesse = round((distance / tps_course), 3)
    print("vitesse moyenne de course :", vitesse, "m/s", "\n", "ou", round((vitesse*3.6),3), "km/h")
    
    print("le nombre de foulée est : ", len(peaks), "pas", "\n", "ou", "\n", (((len(peaks))*60)/tps_course), "ppm (pas par minute)")
    
    longueur_foulee = distance/len(peaks)
    
    print("foulée moyenne de :",longueur_foulee, "m")
    
    # Sauvegardez le graphique en tant qu'image PNG
    plt.savefig('static/mon_graphique.png', bbox_inches='tight')
    # Créez un dictionnaire avec les résultats d'analyse que vous souhaitez afficher
    resultats = {
        'ground_contact': ground_contact,
        'median_ground_contact': round(median_ground_contact, 3),
        'tps_course': tps_course,
        'vitesse': vitesse,
        'vitesse_km_h': round((vitesse * 3.6), 3),
        'nombre_foulees': len(peaks),
        'ppm': round(((len(peaks) * 60) / tps_course), 3),
        'longueur_foulee': round(longueur_foulee,3)
}
    return resultats

