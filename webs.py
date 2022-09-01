import web
import json
from numpy import *
import ezdxf
#from gcode_lib import dxf2image
#from gcode_lib import intersect
#import fretboard_strings as strings
import sys
import os
import re
from datetime import datetime

import markdown

def multiscale_2_markdonw(fretboard):
    mark=[]

    mark.append("## Scale")
    mark.append("|Fretboard Parameters |Values|")
    mark.append("|:---|---:|")
    mark.append("|**Left Scale**:|"+str(fretboard["scale_left"])+"|")
    mark.append("|**Right Scale**:|"+str(fretboard["scale_right"])+"|")
    mark.append("|**Frets**:|"+str(fretboard["number_of_frets"])+"|")
    mark.append("|**Fretboard Width at nut** \n*(From string center to string center)*:|"+str(fretboard["width_at_zero_line"])+" mm|")
    mark.append("|**Fretboard Width at bridge** \n*(From string center to string center)*:|"+str(fretboard["width_at_bottom_line"])+" mm|")
    mark.append("|**Left border**:|"+str(fretboard["left_border"])+" mm|")
    mark.append("|**Right border**:|"+str(fretboard["right_border"])+" mm|")
    mark.append("|**Bridge compensation**:|"+str(fretboard["bridge_spacing_compensated"])+" mm|")
    mark.append("|**Fret perpenticular to centerline**:|"+str(fretboard["fret_perpenticular_to_centerline"])+" |")
    perp=fretboard["fret_perpenticular_to_centerline"]
    mark.append("<p></p>")
    mark.append("# Fret positions")

    mark.append("|Fret |Left Scale|Right Scale|")
    mark.append("|:---|------:|------:|")
    scale_left=fretboard["scale_positions"][0] # left scale
    scale_right=fretboard["scale_positions"][1] # rigth scale
    n=0
    while n < fretboard["number_of_frets"]:
        fret_left=scale_left[n]
        fret_rigth=scale_right[n]
        if n==0 :
            mark.append("**Nut**|----------  "+str(round(fret_left,4))+" mm|----------  "+str(round(fret_rigth,4))+" mm|")
        else :
            if n==perp :
                mark.append("**Fret "+ str(n) +"**|**"+str(round(fret_left,4))+" mm**|**"+str(round(fret_rigth,4))+"mm**|")
            else :
                 mark.append("**Fret "+ str(n) +"**|"+str(round(fret_left,4))+" mm|"+str(round(fret_rigth,4))+"mm|")

        n=n+1

    mark.append("## Strings")
    mark.append(str(fretboard["strings"]))

    return mark


def single_scale_2_markdonw(fretboard):
    mark=[]

    mark.append("## Scale")
    mark.append("|Fretboard Parameters |Values|")
    mark.append("|:---|---:|")
    mark.append("|**Scale**:|"+str(fretboard["scale_left"])+"|")
    mark.append("|**Frets**:|"+str(fretboard["number_of_frets"])+"|")
    mark.append("|**Fretboard Width at nut** \n*(From string center to string center)*:|"+str(fretboard["width_at_zero_line"])+" mm|")
    mark.append("|**Fretboard Width at bridge** \n*(From string center to string center)*:|"+str(fretboard["width_at_bottom_line"])+" mm|")
    mark.append("|**Left border**:|"+str(fretboard["left_border"])+" mm|")
    mark.append("|**Right border**:|"+str(fretboard["right_border"])+" mm|")
    mark.append("|**Bridge compensation**:|"+str(fretboard["bridge_spacing_compensated"])+" mm|")

    mark.append("<p></p>")
    mark.append("# Fret positions")

    mark.append("|Fret |Distance from nut|")
    mark.append("|:---|---:|")
    scale=fretboard["scale_positions"][0] # left scale
    n=0
    for fret in scale:
        if n==0 :
            mark.append("**Nut**|"+str(fret)+" mm|")
        else:
            mark.append("**Fret"+ str(n) +"**|"+str(round(fret,4))+" mm|")
        n=n+1

    return mark

def fretb_2_markdown(fretboard):

    mark=[]
    mark.append(fretboard["about"])
    mark.append("# "+fretboard["fretboard_name"])
    mark.append("")
    multiscale=(fretboard["scale_left"]!=fretboard["scale_right"])
    if multiscale :
        mark=mark+multiscale_2_markdonw(fretboard)
    else:
        mark=mark+single_scale_2_markdonw(fretboard)
    return markdown_2_string(mark)

def markdown_2_string(mark):
    out=""
    for line in mark:
        out=out+line+"\n"
    return out
configuracio={}

render = web.template.render('templates/')

urls = (
    '/', 'index'
)

def render_fretboard_output(filename) :
 f = open(filename, 'r')
 fretboard = json.load(f)
 md_text=fretb_2_markdown(fretboard)
# print(md_text)
 html = markdown.markdown(md_text,extensions=["tables"])
 return html


def select_strings(data) :
    default=[0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0,0.0]
    strings={
#        "strings_e9s":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0],
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
        print("number of strings:"+str(nstrings))
    else :
        print("number_of_strings missing")
        return default
    stringset="strings_e10s"
    found=False
#    print("options:"+str(data))
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

        sel=selection[:nstrings]
        sel.reverse()
        return sel
    else :
        print("This should never happen\nUnknown stringset:"+stringset)
        return default


def ajusta_json(data):
    fretboard={
      "about": "Fretboard layout generated by fretboard-generator,  [https://aprendideluthier.com/fretboard-generator](https://aprendideluthier.com/fretboard-generator) (c)Marc Alier @granludo 2022",
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
    key="left_border"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        fretboard[key]=0
    key="right_border"
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
    key="fret_perpenticular_to_centerline"
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
        if fretboard["scale_right"]==0:
        #    print("--- single scale fretboard")
            fretboard["scale_right"]=fretboard["scale_left"]
        #else:
        #    print("--- multiscale fretboard")
        output="POST DATA:\n\n"+json.dumps(data,indent=3,sort_keys=False)+"\n"
        output=output+"FRETBOARD PARAMETERS:\n\n"+json.dumps(fretboard,indent=3,sort_keys=False)


        # get current date and time
        current_datetime = datetime.now()
        print("Current date & time : ", current_datetime)

        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        str_current_datetime=str_current_datetime.replace(" ","")
        # create a file object along with extension
        filename = "./tmp/fretboard_"+str_current_datetime+".json"
        outputfile = "fretboard_"+str_current_datetime+"_out"

        with open(filename, 'w') as f:
            f.write(json.dumps(fretboard,indent=3,sort_keys=False))
            f.close()
        link_pdf=web.ctx.home+"output/"+outputfile+".pdf"
        output=output+link_pdf
        print("python3 fretboard.py "+filename+" "+outputfile)
        os.system("python3 fretboard.py "+filename+" "+outputfile)
        print("ok")
        #print("./output/"+outputfile+".json")
        # output=output+"\n\n\nFRETBOARD RESULT\n"+render_fretboard_output("./output/"+outputfile+".json")

        return render_fretboard_output("./output/"+outputfile+".json")

if __name__ == "__main__":

    f = open("conf.json", 'r')
    configuracio = json.load(f)

    app = web.application(urls, globals())
    app.run()
