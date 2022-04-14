import web
import json
from numpy import *
import ezdxf
#from gcode_lib import dxf2image
#from gcode_lib import intersect
#import fretboard_strings as strings
import json
import sys
import os
import re
from datetime import datetime


render = web.template.render('templates/')

urls = (
    '/', 'index'
)

def select_strings(data) :
    default=[0.010, .0135, 0.017,0.025, 0.034, 0.046]
    strings={
        "strings_e9":[0.009, 0.011, 0.016, 0.024, 0.032, 0.042,0.052,0.062],
        "strings_e10s":[0.010, .0135, 0.017,0.025, 0.034, 0.046,0.060,0.072],
        "strings_e11s":[0.011, 0.014, 0.018,0.030, 0.042, 0.052, 0.064,0.074],
        "strings_e12s":[0.012,0.016,0.024,0.032,0.044,0.056,0.68,0.80],
        "strings_a12s":[0.012, 0.016,0.024, 0.032, 0.042, 0.053, 0.65,0.075],
        "strings_a13s":[0.013, 0.017, 0.026, 0.035, 0.045, 0.056,0.70,0.080],
        "strings_classic":[0.028,0.032,0.02,0.029,0.035,0.43,0.43,0.43],
        "strings_flamenco":[0.028,0.032,0.040,0.031,0.037,0.0444,0.0444,0.0444],
        "strings_bass":[0.045,0.065,0.8,0.1],
        "strings_bassthick":[0.03,0.045,0.065,0.08,0.1,0.13],
        "ukelele":[0.026,0.036,0.024,0.30],
        "nylon":[0.035,0.035,0.035,0.035,0.035,0.035,0.035,0.035,0.035,0.035,0.035]
        }
    options=strings.keys()
    if "number_of_strings" in data :
        nstrings=int(data["number_of_strings"])
    else :
        print("number_of_strings missing")
        return default
    stringset="strings_e10s"
    found=False
    for s in options:
        if s in data :
            stringset=s
            found=True
            break
    if not found :
        print("stringset not found in form data")
    if stringset in strings:
        selection=strings[stringset]
        if nstrings > len(selection):
            print("not enough strings in "+str(selection))
            return selection
        selection.reverse()
        sel=selection[:nstrings]
        return sel
    else :
        print("This should never happen\nUnknown stringset:"+stringset)
        return default


def ajusta_json(data):
    fretboard={
      "about": "Fretboard Definition format, by Marc Alier https://aprendideluthier.com 2022",
      "fretboard_name": "test 001 ",
      "version":0.1,
      "scale_left": 640,
      "scale_right": 628,
      "number_of_frets":22,
      "width_at_zero_line":43.18,
      "width_at_bottom_line":65,
      "left_border":3.56,
      "right_border":3.56,
      "bridge_spacing_compensated":1 ,
      "strings": [0.046, 0.036, 0.026, 0.017, 0.013, 0.010],
      "fret_perpenticular_to_centerline":12,
      "intonation_compensation_left":3,
      "intonation_compensation_right":1
    } #setting default values
    key="fretboard_name"
    if key in data :
        fretboard[key]=data[key]
    else :
        print("JSON:missing key '"+key+"'")
        return
    key="scale_left"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("JSON:missing key '"+key+"'")
        return
    key="scale_right"
    if key in data :
        if data[key]==0:
            fretboard[key]=float(fretboard["scale_left"])
        fretboard[key]=float(data[key])
    key="number_of_frets"
    if key in data :
        fretboard[key]=int(data[key])
    else :
        print("JSON:missing key '"+key+"'")
        return
    key="width_at_zero_line"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("JSON:missing key '"+key+"'")
        return
    key="width_at_bottom_line"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("JSON:missing key '"+key+"'")
        return
    key="left border"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        fretboard[key]=0
    key="right border"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        fretboard[key]=0
    key="bridge_spacing_compensated"
    if key in data :
        fretboard[key]=1 #just needs to be there 1 is True
    else :
        fretboard[key]=0
    fretboard["strings"]=select_strings(data)
    key="intonation_compensation_left"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        fretboard[key]=0
    key="intonation_compensation_right"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        fretboard[key]=0

    return fretboard


class index:
    def GET(self):
        name = 'Bob'
        return render.index(name)

    def POST(self):
        data = web.input() # you can get data use this method
        fretboard= ajusta_json(data)
        output="POST DATA\n"+json.dumps(data,indent=3,sort_keys=False)+"\n"
        output=output+"FRETBOARD PARAMETERS\n"+json.dumps(fretboard,indent=3,sort_keys=False)


        # get current date and time
        current_datetime = datetime.now()
        print("Current date & time : ", current_datetime)

        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        str_current_datetime=str_current_datetime.replace(" ","")
        # create a file object along with extension
        filename = "fretboard_"+str_current_datetime+".json"
        outputfile = "fretboard_"+str_current_datetime+"_out"

        with open(filename, 'w') as f:
            f.write(json.dumps(fretboard,indent=3,sort_keys=False))
            f.close()
        link_pdf=web.ctx.home+"output/"+outputfile+".pdf"
        output=output+link_pdf
        print("python3 fretboard.py "+filename+" "+outputfile)
        os.system("python3 fretboard.py "+filename+" "+outputfile)
        print("ok")

        return output

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
