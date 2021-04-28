import shared

POINT_3D_RESPONSE = "\nSegún los datos obtenidos de las señales de cada neonato, es evidente que el neonato numero 2 se encuentra en claro peligro de apnea ya que tanto su frecuencia cardiaca como su frecuencia respiratoria, se encuentra por debajo de lo normal para un neonato descrito en la referencia de 'measurements' de la guía.\nEn especial el dato de la frecuencia respiratoria indica que el neonato tiene una capacidad de respiración reducida y probablemente debe ser revisado por personal medico lo más pronto posible."

@shared.presentPoint
def main():
    shared.displayResponse(POINT_3D_RESPONSE)

if __name__ == "__main__":
    main()