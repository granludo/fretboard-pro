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
from lib import fretboard_lib_in as ft
from lib import dxf2image
# test at './input/json/test_fretboard.json'

def show_params(params):
    for param in params:
        print(param+":"+str(params[param]))

print("Usage:python3 fretboard.py inputfile.json folder")
print("Fretboard Generator by Marc Alier (c)2022")
print("Reading Fretboard File from:"+sys.argv[1])
f = open(sys.argv[1], 'r')
fretboard = json.load(f)
print("Json Load Ok")


#show_params(fretboard)
ft.calculate(fretboard)


print("Print writting Freatboard JSON file to:"+sys.argv[2])
with open("./output/"+sys.argv[2]+".json","w") as outfile:
    json.dump(fretboard, outfile, indent=4)
ft.generate_dxf(fretboard,"./output/"+sys.argv[2]+".dxf")
ft.save_to_scale(fretboard,scale=1,filename="./output/"+sys.argv[2]+".pdf")
#ft.save_to_scale(fretboard,scale=1,filename="./output/"+sys.argv[2]+".png")

print("Ok")
