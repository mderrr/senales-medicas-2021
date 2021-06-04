import final_shared_santih as shared

@shared.presentPoint
def main():
    print("Alcides se equivoca por que el primer pico esta elevado desde el principio de la señal por lo cual el algoritmo no lo detecta ya que segun él nunca subio.")
    print("una forma simple de arreglaro es cambiar el primer valor de la señal (sig[0]) a 0 para que se evidencie esta primera subida.")

if __name__ == "__main__":
    main()