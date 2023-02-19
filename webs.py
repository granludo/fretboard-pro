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



def multiscale_2_markdonw(fretboard,outputfile):
    mark=[]

    perp=fretboard["fret_perpenticular_to_centerline"]
    mark.append("<p></p>")
    mark.append("# Fret positions\* / Posiciones de los trastes \**")
    mark.append("<p></p>")
    mark.append("\* Distances measured in milimeters from de 0 fret in the Left Scale</br>")
    mark.append("\** Dist&aacute;ncias medidas en mil&iacute;metros desde el traste 0 en la Escala Izquierda")
    mark.append("<p></p>")
    mark.append("|**Fret / Traste **|** Left / Izquierda**|&nbsp;&nbsp;&nbsp;&nbsp;**Right / Derecha**|")
    mark.append("|:---|------:|------:|")
    scale_left=fretboard["scale_positions"][0] # left scale
    scale_right=fretboard["scale_positions"][1] # rigth scale
    n=0
    while n < fretboard["number_of_frets"]:
        fret_left=scale_left[n]
        fret_rigth=scale_right[n]
        if n==0 :
            mark.append("**0 - Nut - Cejuela**|----------  "+str(round(fret_left,4))+" mm|----------  "+str(round(fret_rigth,4))+" mm|")
        else :
            if n==perp :
                mark.append("**Fret / Traste "+ str(n) +"**|**"+str(round(fret_left,4))+" mm**|**"+str(round(fret_rigth,4))+"mm**|")
            else :
                mark.append("**Fret / Traste "+ str(n) +"**|"+str(round(fret_left,4))+" mm|"+str(round(fret_rigth,4))+"mm|")

        n=n+1
    mark.append("**Intonated Bridge**\n**Puente con entonaci&oacute;n** |"+str(round(fretboard["intonated_bridge"][0][1],4))+" mm**|**"+str(round(fretboard["intonated_bridge"][1][1],4)))
    mark.append("<p></p>")
    mark.append("## Strings gauches / grosores de cuerdas ")
    mark.append("*Units in inches*, *Unidades en pulgadas*")
    mark.append(str(fretboard["strings"]))
    mark.append("## Download Files / Descarga Ficheros")
    f = open("conf.json", 'r')
    configuracio = json.load(f)
    mark.append("[Scale 1:1 PDF File / Fichero PDF a Escala 1:1]("+configuracio["base_output_file_url"]+"/"+outputfile+".pdf) , ")
    mark.append("[DXF File / Fichero DXF]("+configuracio["base_output_file_url"]+"/"+outputfile+".dxf)")

    return mark


def single_scale_2_markdonw(fretboard,outputfile):
    mark=[]


    mark.append("<p></p>")
    mark.append("# Fret positions\* / Posiciones de los trastes \**")
    mark.append("<p></p>")
    mark.append("\* Distances measured in milimeters from de 0 fret in the Left Scale</br>")
    mark.append("\** Dist&aacute;ncias medidas en mil&iacute;metros desde el traste 0 en la Escala Izquierda")
    mark.append("<p></p>")

    mark.append("|**Fret / Traste &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**|**Scale / Escala**|")
    mark.append("|:---|------:|")
    scale_left=fretboard["scale_positions"][0] # left scale
    scale_right=fretboard["scale_positions"][1] # rigth scale
    n=0
    while n < fretboard["number_of_frets"]:
        fret_left=scale_left[n]
        fret_rigth=scale_right[n]
        if n==0 :
            mark.append("**0 / Nut / Cejuela **|  "+str(round(fret_left,4))+" mm  ")
        else :
            mark.append("**Fret / Traste "+ str(n) +"**|"+str(round(fret_left,4))+" mm")
        n=n+1
    mark.append("<p></p>")
    mark.append("**Intonated Bridge \n Puente Entonado :**"+str(round(fretboard["intonated_bridge"][0][1],4))+" mm** / **"+str(round(fretboard["intonated_bridge"][1][1],4)))
    mark.append("<p></p>")
    mark.append("## Strings gauges / Grosores cuerdas ")
    mark.append("<p></p>")
    mark.append("*Units in inches* / *Unidades en pulgadas*")
    mark.append(str(fretboard["strings"]))
    mark.append("## Download Files / Descarga Ficheros")
    f = open("conf.json", 'r')
    configuracio = json.load(f)
    mark.append("<p></p>")
    mark.append("[Scale 1:1 PDF File / Fichero PDF a Escala 1:1]("+configuracio["base_output_file_url"]+"/"+outputfile+".pdf) , ")
    mark.append("[DXF File / Fichero DXF]("+configuracio["base_output_file_url"]+"/"+outputfile+".dxf)")

    return mark



def fretb_2_markdown(fretboard,outputfile):

    mark=[]
    mark.append(fretboard["about"])
    mark.append("# "+fretboard["fretboard_name"])
    mark.append("")
    multiscale=(fretboard["scale_left"]!=fretboard["scale_right"])
    if multiscale :
        mark.append("## Multiscale Fretboard / Diapas&oacute;n Multi-escala ")
    else:
        mark.append("## Fretboard / Diapas&oacute;n ")
    mark.append("<p></p>")
    mark.append("*Units in milimeters except for string gauges* / *Unidades en mil&iacute;metros excepto para los grosores de cuerdas*")
    mark.append("<p></p>")
    mark.append("|Fretboard Parameters |Values|&nbsp;&nbsp;&nbsp;|Par&aacute;metros diapas&oacute;n|Valores|")
    mark.append("|:---|---:|---|:---|---:")
    if multiscale :
        mark.append("|**Left Scale**:|"+str(fretboard["scale_left"])+" mm ||**Escal Izquierda**|"+str(fretboard["scale_left"])+" mm")
        mark.append("|**Right Scale**:|"+str(fretboard["scale_right"])+" mm ||**Escala Derecha**|"+str(fretboard["scale_right"])+" mm")
        mark.append("|**Fret perpenticular to centerline**:|"+str(fretboard["fret_perpenticular_to_centerline"])+
        " ||**Traste perpenticular a la l&iacute;nea central**|"+str(fretboard["fret_perpenticular_to_centerline"])+" ")

    else :
        mark.append("|**Scale**:|"+str(fretboard["scale_left"])+" mm ||**Escala**|"+str(fretboard["scale_left"])+" mm")
    mark.append("|**Frets**:|"+str(fretboard["number_of_frets"])+"||**N&uacute;mero de Trastes**|"+str(fretboard["number_of_frets"])+" mm")
    mark.append("|**Width at nut** :|"+str(fretboard["width_at_zero_line"])+
    " mm||**Ancho en Cejuela**|"+str(fretboard["width_at_zero_line"])+" mm")
    mark.append("|**Width at bridge** :|"+str(fretboard["width_at_bottom_line"])+" mm||**Ancho en silleta/puente**|"+str(fretboard["width_at_bottom_line"])+" mm")
    mark.append("|**Left border**:|"+str(fretboard["left_border"])+
    " mm||**Borde Izquierdo**|"+str(fretboard["left_border"])+" mm")
    mark.append("|**Right border**:|"+str(fretboard["right_border"])+" mm||**Borde Derecho**|"+str(fretboard["right_border"])+" mm")

    if fretboard["bridge_spacing_compensated"]==1 :
        mark.append("|**Bridge strings spacing**| Gauge Compensation ||**Espaciado cuerdas en Selleta**| Compensado por grosor|")
    else :
        mark.append("|**Bridge strings spacing**| Equal distances ||**Espaciado cuerdas en Selleta**| Dist&aacute;ncias iguales|")
    mark.append("|**Bridge Intonnation Left**:|"+str(fretboard["intonation_compensation_left"])+
        " ||**Entonaci&oacute;n Puente Izquierda**|"+str(fretboard["intonation_compensation_left"])+" mm")
    mark.append("|**Bridge Intonnation Right**:|"+str(fretboard["intonation_compensation_right"])+
        " ||**Entonaci&oacute;n Puente Derecha**|"+str(fretboard["intonation_compensation_right"])+" mm")




    if multiscale :
        mark=mark+multiscale_2_markdonw(fretboard,outputfile)
    else:
        mark=mark+single_scale_2_markdonw(fretboard,outputfile)
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

def render_fretboard_output(filename,outputfile) :
 f = open(filename, 'r')
 fretboard = json.load(f)
 md_text=fretb_2_markdown(fretboard,outputfile)
 html = markdown.markdown(md_text,extensions=["tables"])
 return html


def select_strings(data) :
    default=[0.0, 0.0, 0.0,0.0, 0.0, 0.0,0.0,0.0]
    strings={
        "default":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0],
        "strings_e9s":[0.009, 0.011, 0.016, 0.024, 0.032, 0.042,0.052,0.062],
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
    if "number_of_strings" in data :
        nstrings=int(data["number_of_strings"])
    else :
        return default
    stringset="default"
    print("hello"+str(data["Cordaje"]))
    if "Cordaje" in data :
        stringset=data["Cordaje"]
        print("Stringset="+stringset+"ostia:"+data["Cordaje"]+"\nDATA="+str(data))
    else :
        print("Webs.py:Warning in Select_strings:Cordaje not fount in Data:"+str(data))
    selection=strings[stringset]
    if nstrings > len(selection):
        print("Webs.py:Error in Select_strings:not enough strings in "+str(selection))
        return selection
    sel=selection[:nstrings]
    sel.reverse()
    return sel


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
        print("Webs.py Errro ajusta_json JSON:missing key '"+key+"':data:"+str(data))
        return
    key="scale_left"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("Webs.py Errro ajusta_json JSON:missing key '"+key+"':data:"+str(data))
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
        print("Webs.py Errro ajusta_json JSON:missing key '"+key+"':data:"+str(data))
        return
    key="width_at_zero_line"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("Webs.py Errro ajusta_json JSON:missing key '"+key+"':data:"+str(data))
        return
    key="width_at_bottom_line"
    if key in data :
        fretboard[key]=float(data[key])
    else :
        print("Webs.py Errro ajusta_json JSON:missing key '"+key+"':data:"+str(data))
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
        return "<a href='httpa://aprendideluthier.com/fretboard_generator'>Go back</a>"

    def POST(self):
        try :
            data = web.input() # you can get data use this method
            fretboard= ajusta_json(data)
            if fretboard["scale_right"]==0:
                fretboard["scale_right"]=fretboard["scale_left"]
            output="POST DATA:\n\n"+json.dumps(data,indent=3,sort_keys=False)+"\n"
            output=output+"FRETBOARD PARAMETERS:\n\n"+json.dumps(fretboard,indent=3,sort_keys=False)
            # get current date and time
            current_datetime = datetime.now()
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
            print("Webs.py Executing python3 fretboard.py "+filename+" "+outputfile)
            os.system("python3 fretboard.py "+filename+" "+outputfile)
            print("Webs.py ok")
            #print("./output/"+outputfile+".json")
            # output=output+"\n\n\nFRETBOARD RESULT\n"+render_fretboard_output("./output/"+outputfile+".json")

            return render_fretboard_output("./output/"+outputfile+".json", outputfile)
        except :
            return "ops something did not work"

if __name__ == "__main__":
    f = open("conf.json", 'r')
    configuracio = json.load(f)
    print(str(configuracio))

    app = web.application(urls, globals())
    app.run()
