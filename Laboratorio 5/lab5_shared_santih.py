import os
import sys
import pandas
import platform

WINDOWS_PLATFORM_NAME    = "Windows"
WINDOWS_CLEAR            = "cls"
UNIX_CLEAR               = "clear"

WINDOWS_EXECUTE_TEMPLATE = "py .\{}"
UNIX_EXECUTE_TEMPLATE    = "python3 './{}'"

POINT_TITLE_TEMPLATE     = "////////////////  Punto {}  ////////////////"

CURRENT_FILE_DIRECTORY   = os.path.dirname(__file__)

def setCurrentWorkingDirectory():
    if (CURRENT_FILE_DIRECTORY != os.getcwd()):
        os.chdir(CURRENT_FILE_DIRECTORY)

def clear(title=""):
    os.system(WINDOWS_CLEAR if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_CLEAR)
    if title: print(POINT_TITLE_TEMPLATE.format(title))

def getPythonName():
    python_name = WINDOWS_EXECUTE_TEMPLATE if platform.system() == WINDOWS_PLATFORM_NAME else UNIX_EXECUTE_TEMPLATE
   
    return python_name

def getPointName():
    return os.path.basename(sys.argv[0]).split("_")[1]

def getSignalFromFile(file_name, dict_key=None):
    file_dictionary = pandas.read_csv(file_name)
    dict_key = dict_key if dict_key is not None else list(file_dictionary.keys())[0]
    
    return file_dictionary[dict_key]

setCurrentWorkingDirectory()