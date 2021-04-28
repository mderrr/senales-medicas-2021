import os
import shared

# Este script es solo una herramienta para revisar todos los puntos a la vez
# si por alguna razón no funciona no importa, los puntos por separado deben
# funcionar normalmente. 

EXECUTE_SCRIPT_TEMPLATE = "python3 './{}'"
SCRIPT_FORMAT = "*_santih.py"

def main():
    lab_points = shared.findFilesOnDirectory(SCRIPT_FORMAT, os.getcwd())

    # Pop lab3_all
    lab_points.pop()

    for point in lab_points:
        os.system(EXECUTE_SCRIPT_TEMPLATE.format(point))

if __name__ == "__main__":
    main()