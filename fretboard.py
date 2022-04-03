# By Marc Alier , https://aprendizdeluthier.com
# granludo at the gmail thing
# March 2022
# License GPLv3

from numpy import *
import ezdxf
#from gcode_lib import dxf2image
#from gcode_lib import intersect
#import fretboard_strings as strings
import json
import sys
import re
from lib import fretboard_lib as ft
# test at './input/json/test_fretboard.json'

def show_params(params):
    for param in params:
        print(param+":"+str(params[param]))

# print(parameters)
print("Fretboard Generator by Marc Alier (c)2022")
print("Reading Fretboard File from:"+sys.argv[1])
f = open(sys.argv[1], 'r')
fretboard = json.load(f)
print("Ok")

show_params(fretboard)

ft.calculate_strings(fretboard)



print("Print writting Freatboard JSON file to:"+sys.argv[2])
with open(sys.argv[2],"w") as outfile:
    json.dump(fretboard, outfile)

print("Ok")
