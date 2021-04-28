import os
import shared

# Este script es solo una herramienta para revisar todos los puntos a la vez
# si por alguna razón no funciona no importa, los puntos por separado deben
# funcionar normalmente. 

SCRIPT_FORMAT = "*_santih.py"

def main():
    lab_points = shared.findFilesOnDirectory(SCRIPT_FORMAT, os.getcwd())
    execute_script_template = shared.getPythonName()
    

    # Pop lab3_all
    lab_points.pop()

    for point in lab_points:
        command = execute_script_template.format(point)
        print(command)
        os.system(command)
   
if __name__ == "__main__":
    main()