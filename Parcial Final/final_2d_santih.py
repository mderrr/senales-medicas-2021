import final_shared_santih as shared

@shared.presentPoint
def main():
    print("El algoritmo que yo propongo seria el de primero, rectificar la señal removiendo su nivel dc y posteriormente sacando el valor absoluto, luego hacer una envoltura de RMS usando un convolve y por ultimo encontrar los picos de esta señal haciendo uso del modulo find_peaks de la libreria scipy. En mi opinion este algoritmo es mucho mas simple de entender y modificar y ademas de esto es bastante robusto asi como el de abp_peaks.")

if __name__ == "__main__":
    main()