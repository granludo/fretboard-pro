#ok let's try
from __future__ import annotations
from numpy import *
import ezdxf
from ezdxf import units
from lib import intersect
from pathlib import Path
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.math import Vec2
from ezdxf.enums import TextEntityAlignment, MTextEntityAlignment
import json

x=0
y=1
left=0
right=1
inch_x_mm =25.4
lang_es={
    "Diapasón multiescala":"Diapasón multiescala",
    "Escala Izquierda: ":"Escala Izquierda: ",
    "Escala Derecha: ":"Escala Derecha: ",
    "Traste Perpenticular: ":"Traste Perpenticular: ",
    "Escala: ":"Escala: ",
    "Trastes: ":"Trastes: ",
    "Ancho en Cejuela (centro cuerda E a centro cuerda e): ":
        "Ancho en Cejuela :  ",
    "Ancho en Puente (centro cuerda a centro cuerda)":
        "Ancho en Puente/Silleta : ",
    "Borde izquierdo: ":"Borde izquierdo: ",
    "Borde derecho: ":"Borde derecho: ",
    "Cuerdas: ":"Número de Cuerdas: ",
    "Cordaje: ":"Cordaje: ",
    "Compensation:":"Compensación multiescala:",
    "Puente con entonación":"Puente con entonación ",
    "Compensación entonación izquierda":"Compensación entonación izquierda: ",
    "Compensación entonación derecha":"Compensación entonación derecha: "
}
lang_en={
    "Diapasón multiescala":"Mulstiscale (FAN) fretboard",
    "Escala Izquierda: ":"Left Scale: ",
    "Escala Derecha: ":"Right Scale: ",
    "Traste Perpenticular: ":"Perpenticular Fret: ",
    "Escala: ":"Scale: ",
    "Trastes: ":"Frets: ",
    "Ancho en Cejuela (centro cuerda E a centro cuerda e): ":     "Width at Nut :  ",
    "Ancho en Puente (centro cuerda a centro cuerda)": "Width at Bridge :",
    "Borde izquierdo: ":"Left overhang: ",
    "Borde derecho: ":"Right overhang: ",
    "Cuerdas: ":"Number of Strings: ",
    "Cordaje: ":"Gauges: ",
    "Compensation:":"Mulstiscale compensation:",
    "Puente con entonación":"Intonatted bridge ",
    "Compensación entonación izquierda":"Left intonnation: ",
    "Compensación entonación derecha":"Right intonnation:"
}


def toinch(num,convert=0):
    if convert!=0:
        return num/inch_x_mm
    else:
        return num

def calculate_space_between_strings_zero_line(fretboard):
    s=0;
    strings_acumulated_width=0
    n = 0
    width_in_mm=fretboard["strings"][0]*25.4/2
    strings_acumulated_width=strings_acumulated_width+width_in_mm
    n=n+1
    while n < len(fretboard["strings"])-1 :
        string = fretboard["strings"][n]
        width_in_mm=string*25.4
        strings_acumulated_width=strings_acumulated_width+width_in_mm
        n=n+1
    string = fretboard["strings"][n]
    width_in_mm=string*25.4/2
    strings_acumulated_width=strings_acumulated_width+width_in_mm

    B3=fretboard["width_at_zero_line"]
    B4=fretboard["left_border"]
    B5=fretboard["right_border"]
    return (B3-B4-B5-strings_acumulated_width) / (len(fretboard["strings"])-1)


def calculate_space_between_strings_bottom_line(fretboard):
    n=0
    strings_acumulated_width=0
    if fretboard["bridge_spacing_compensated"]==1:
    ## if the bridge has string spacing adjustment , else the calculation is just proportional
        width_in_mm=fretboard["strings"][0]*25.4/2
        strings_acumulated_width=strings_acumulated_width+width_in_mm
        n=n+1
        while n < len(fretboard["strings"])-1 :
            string = fretboard["strings"][n]
            width_in_mm=string*25.4
            strings_acumulated_width=strings_acumulated_width+width_in_mm
            n=n+1
        string = fretboard["strings"][n]
        width_in_mm=string*25.4/2
        strings_acumulated_width=strings_acumulated_width+width_in_mm

    B3=fretboard["width_at_bottom_line"]
    B4=fretboard["left_border"]
    B5=fretboard["right_border"]
    return (B3-B4-B5-strings_acumulated_width) / (len(fretboard["strings"])-1)

def calculate(fretboard):
    fretboard=calculate_frame(fretboard)
    fretboard=calculate_strings(fretboard)
    fretboard=calculate_frets(fretboard)
    return fretboard


def calculate_strings(fretboard):

    strings_segments=[]
    center_offsets=[]
    space_between_strings_zero_line=calculate_space_between_strings_zero_line(fretboard)
    space_between_strings_bottom_line=calculate_space_between_strings_bottom_line(fretboard)
    zero_offset=fretboard["left_border"]
    bottom_offset=fretboard["left_border"]
    n=0
    string=fretboard["strings"][n]
    zero_offset=zero_offset  #duh
    bottom_offset=bottom_offset #duh
    center_offsets.append([zero_offset,bottom_offset])
    if fretboard["bridge_spacing_compensated"]==1:
        bottom_offset=bottom_offset+space_between_strings_bottom_line+((string*25.4)/2)
    else :
        bottom_offset=bottom_offset+space_between_strings_bottom_line
    zero_offset=zero_offset+space_between_strings_zero_line+((string*25.4)/2)
    n=1
    while n < len(fretboard["strings"]):
        string = fretboard["strings"][n]
        zero_offset=zero_offset+((string*25.4)/2)
        if fretboard["bridge_spacing_compensated"]==1:
            bottom_offset=bottom_offset+((string*25.4)/2)
        center_offsets.append([zero_offset,bottom_offset])
        if fretboard["bridge_spacing_compensated"]==1:
            bottom_offset=bottom_offset+space_between_strings_bottom_line+((string*25.4)/2)
        else :
            bottom_offset=bottom_offset+space_between_strings_bottom_line

        zero_offset=zero_offset+space_between_strings_zero_line+((string*25.4)/2)
        n=n+1
#    print("last zero offset:"+str(zero_offset-space_between_strings_zero_line-((string*25.4)/2)))
#    print("right border:"+str(fretboard["right_border"]))
    for offset in center_offsets:
        a = [fretboard["left_side"][0][0]+offset[0],0]
        b = [fretboard["left_side"][1][0]+offset[1],max(fretboard["scale_left"],fretboard["scale_right"])]
        string_segment=[a,b]
        strings_segments.append(string_segment)
    extended_strings_segments=[]
    for segment in strings_segments:

        new_x=intersect.extend_line(-200,segment)
        aux=segment
        aux[0]=[new_x,-200]
        extended_strings_segments.append(aux)
    fretboard["strings_segments"]=strings_segments
    fretboard["extended_strings_segments"]=extended_strings_segments
    return fretboard

def calculate_frame(fretboard):
    zero_line=[[-fretboard["width_at_zero_line"]/2,0],[fretboard["width_at_zero_line"]/2,0]]
    fretboard["zero_line"]=zero_line
    max_scale=max(fretboard["scale_left"],fretboard["scale_right"])
    bottom_line=[[-fretboard["width_at_bottom_line"]/2,max_scale],[fretboard["width_at_bottom_line"]/2,max_scale]]
    fretboard["bottom_line"]=bottom_line
    left_side=[zero_line[left],bottom_line[left]]
    fretboard["left_side"]=left_side
    right_side=[zero_line[right],bottom_line[right]]
    fretboard["right_side"]=right_side
    left_border_line=[
        [zero_line[left][x]+fretboard["left_border"],0],
        [bottom_line[left][x]+fretboard["left_border"],max_scale]
    ]
    fretboard["left_border_line"]=left_border_line
    right_border_line=[
        [zero_line[right][x]-fretboard["right_border"],0],
        [bottom_line[right][x]-fretboard["right_border"],max_scale]
    ]
    fretboard["right_border_line"]=right_border_line
    return fretboard


def  generate_frame(msp,draw,fretboard):
    ini_x=-110
    ini_y=-50
    draw.draw_line(msp,ini_x, ini_y, ini_x, ini_y+700)
    # Dibuja las líneas de escala
    for i in range(0, 701):
        if i % 10 == 0:
            if i % 100 == 0:
            # Dibuja una línea larga cada 10 cm
                draw.draw_line(msp,ini_x, ini_y+i, ini_x-30, ini_y+i)
            else:
                if i % 50 == 0:
                # Dibuja una línea corta cada 5 cm
                    draw.draw_line(msp,ini_x, ini_y+i, ini_x-20, ini_y+i)
                else:
                    draw.draw_line(msp,ini_x, ini_y+i, ini_x-10, ini_y+i)
    draw.draw_line_list(msp,fretboard["zero_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["bottom_line"],{"linetype":"DOT2"})
    #draw.add_text(msp,str(round(fretboard["bottom_line"][0][1],2))+" mm",(-100,fretboard["bottom_line"][0][1]), 'LEFT')
    draw.draw_line_list(msp,fretboard["left_side"])
    draw.draw_line_list(msp,fretboard["right_side"])
    draw.draw_line_list(msp,[[0,-300],[0,900]],{"linetype":"CENTER"})
    draw.draw_line_list(msp,fretboard["left_border_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["right_border_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["comprensated_bridge"])
    draw.draw_line_list(msp,fretboard["intonated_bridge"])
    draw.draw_line_list(msp,
        [
            fretboard["intonated_bridge"][0],
            [fretboard["intonated_bridge"][0][0],fretboard["intonated_bridge"][0][1]+40]
        ],{"linetype":"DOT2"})
    draw.add_text(msp,"Puente con entonación/Intonated Bridge",(fretboard["comprensated_bridge"][0][0],fretboard["comprensated_bridge"][0][1]+40), 'LEFT')

    #if   fretboard["bridge_multiscale_compensation"]>0 :
        #draw.draw_line_list(msp,
        #[fretboard["comprensated_bridge"][1],[100,fretboard["comprensated_bridge"][1][1]]],{"linetype":"DOT2"})
        #text="Compensación/Compensation:"+str(round(fretboard["bridge_multiscale_compensation"],2))+" mm"
        #draw.add_text(msp,text,(80,fretboard["comprensated_bridge"][1][1]+5), 'LEFT')
    draw.draw_line_list(msp,
    [fretboard["comprensated_bridge"][0],[-150,fretboard["comprensated_bridge"][0][1]]],{"linetype":"DOT2"})
    draw.add_text(msp,str(round(fretboard["comprensated_bridge"][1][1],2))+" mm",(100,fretboard["comprensated_bridge"][1][1]), 'LEFT')
    draw.add_text(msp,str(round(fretboard["comprensated_bridge"][0][1],2))+" mm",(-100,fretboard["comprensated_bridge"][0][1]), 'LEFT')
    return


def generate_strings(msp,draw,fretboard):
    for string in fretboard["strings_segments"]:
        draw.draw_line_list(msp,string,{"linetype":"DASHED"})
    for string in fretboard["extended_strings_segments"]:
        draw.draw_line_list(msp,string,{"linetype":"DASHED2"})
    n=0
    strings=fretboard["strings"]
    nut=fretboard["frets_segments"][0]
    while n<len(strings):
        string=fretboard["strings_segments"][n]
        p1 = array( string[0])
        p2 = array( string[1])
        p3 = array( nut[0])
        p4 = array( nut[1])
        point = intersect.seg_intersect( p1,p2, p3,p4)


        #draw.draw_line(msp,0,0,string[0][0],string[0][1])
        draw.draw_circle(msp,point, strings[n]*25.4)
        n=n+1
    return



def generate_frets(msp,draw,fretboard):
    n=0
    for fret in fretboard["scale_positions"][left]:
        draw.draw_line(msp,-150,fret,-fretboard["width_at_bottom_line"]/2,fret,{"linetype":"DOT"})
        draw.add_text(msp,str(n)+" : "+str(round(fret,3))+" mm",(-100,fret),'LEFT')
        n=n+1

    n=0
    for fret in fretboard["scale_positions"][right]:
        draw.draw_line(msp,fretboard["width_at_bottom_line"]/2,fret,150,fret,{"linetype":"DOT"})
        draw.add_text(msp,str(n)+" : "+str(round(fret,3))+" mm",(110,fret), 'RIGHT')
        n=n+1
    for fret in fretboard["frets_segments"]:
        draw.draw_line_list(msp,fret)
    return

def calculate_scale(scale,n_frets, compensation=0):
    frets=[]
    n = 0
    while n<n_frets :
        fret=scale - (scale / pow(2,(n/12)) ) + compensation
        frets.append(fret)
        n=n+1
    return frets

def calculate_frets(fretboard):
    frets_left=calculate_scale(fretboard["scale_left"],fretboard["number_of_frets"]+1)
    frets_right=calculate_scale(fretboard["scale_right"],fretboard["number_of_frets"]+1)
    number=int(fretboard["fret_perpenticular_to_centerline"])
    compensation=frets_left[number]-frets_right[number]
    fretboard["bridge_multiscale_compensation"]=compensation
#    print("compensation"+str(compensation))

#    print("frets_right uncompensated"+str(frets_right))
    compensated_frets_right=[]
    for fret in frets_right:
        compensated_frets_right.append(fret+compensation)
#    print("frets_right compensated"+str(frets_right))
    fretboard["scale_positions"]=[frets_left,compensated_frets_right]
    fretboard=calculate_frets_segments(fretboard)
    return fretboard

def calculate_frets_segments(fretboard):
    left_string=fretboard["strings_segments"][0]
    right_string=fretboard["strings_segments"][len(fretboard["strings_segments"])-1]
    frets_segments=[]
    p3 = array( left_string[0] )
    p4 = array( left_string[1] )
    p5 = array( right_string[0] )
    p6 = array( right_string[1] )
    n=0
    while n<= fretboard["number_of_frets"]:
        position=[fretboard["scale_positions"][left][n],fretboard["scale_positions"][right][n]]
        left_baseline=[-300,position[left]],[300, position[left]]
        right_baseline=[-300,position[right]],[300, position[right]]
        p1 = array( [-300,position[left]]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
        p2 = array( [300, position[left]])
        p1r = array( [-300, position[right]]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
        p2r = array( [300, position[right]])
        point_a = intersect.seg_intersect( p1,p2, p3,p4)
        point_b = intersect.seg_intersect( p1r,p2r, p5,p6)
        segment=[[point_a[0],point_a[1]],[point_b[0],point_b[1]]]
        frets_segments.append(segment)
        n=n+1
    p1 = array( [-300,fretboard["scale_left"]]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
    p2 = array( [300, fretboard["scale_left"]])
    p1r = array( [-300, fretboard["scale_right"]+fretboard["bridge_multiscale_compensation"]]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
    p2r = array( [300, fretboard["scale_right"]+fretboard["bridge_multiscale_compensation"]]) #using 200 as a far out point to calculate the instersection, for weird instruments should be bigger
    point_a = intersect.seg_intersect( p1,p2, p3,p4)
    point_b = intersect.seg_intersect( p1r,p2r, p5,p6)
    bridge=[[point_a[0],point_a[1]],[point_b[0],point_b[1]]]

    fretboard["frets_segments"]=frets_segments
    fretboard["comprensated_bridge"]=bridge
    bridge2=[
        [bridge[0][0],bridge[0][1]],[bridge[1][0],bridge[1][1]]
    ]
    bridge2[0][1]=bridge[0][1]+fretboard["intonation_compensation_left"]
    bridge2[1][1]=bridge[1][1]+fretboard["intonation_compensation_right"]
    fretboard["intonated_bridge"]=bridge2
    return fretboard

def generate_dxf(fretboard, fname) :
    doc = ezdxf.new(setup=True)
#    doc.header['$INSUNITS'] = 4 #sets units to milimeters
    doc.units = units.MM
    inch_x_mm =1
    msp = doc.modelspace()
    draw=draw_tool()
#    draw.draw_grid(msp)
    generate_frame(msp,draw,fretboard)
    generate_strings(msp,draw,fretboard)
    generate_frets(msp,draw,fretboard)
#    draw.draw_line(msp,1,1,100,100)
    doc.saveas(fname)
    return
################################################
def make_doc(fretboard,offset=(0, 0), size=(3, 4)):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    inch_x_mm =25.4
    draw=draw_tool()
    draw.convert=1
    #draw.draw_grid(msp)
    generate_frame(msp,draw,fretboard)
    generate_strings(msp,draw,fretboard)
    generate_frets(msp,draw,fretboard)

    x, y = offset
    sx, sy = size
#    red_dashed = {"color": 1, "linetype": "dashed"}
    #msp.add_line((-100, 5), (100, 5), dxfattribs=red_dashed)
#    msp.add_line((6, -100), (6, 100), dxfattribs=red_dashed)
    #msp.add_lwpolyline(
    #    [(x, y), (x + sx, y), (x + sx, y + sy), (x, y + sy)], close=True
    #)
    center = Vec2(offset) + Vec2(size) * 0.5
    #msp.add_text(
    #    f"{size[0]:.1f} inch x {size[1]:.1f} inch ",
    #    height=0.25,
    #    dxfattribs={"style": "OpenSans"},
    #).set_placement(center, align=TextEntityAlignment.MIDDLE_CENTER)
    return doc





def render_limits(
    origin: tuple[float, float],
    size_in_inches: tuple[float, float],
    scale: float,
) -> tuple[float, float, float, float]:
    """Returns the render limits in drawing units. """
    min_x, min_y = origin
    max_x = min_x + size_in_inches[0] * scale
    max_y = min_y + size_in_inches[1] * scale
    return min_x, min_y, max_x, max_y

def describe(fretboard, lang) :

    nga=("scale left:"+str(fretboard["scale_left"])+
            "\nscale right:"+str(fretboard["scale_right"])+
            "\nwidth at zero line:"+str(fretboard["width_at_zero_line"])+
            "\nwidth at bottom line:"+str(fretboard["width_at_bottom_line"])+
            "\nperpenticular fret:"+str(fretboard["fret_perpenticular_to_centerline"])+
            "\nstrings (inches):"+str(fretboard["strings"])
            )

    specs=fretboard_specs(fretboard,lang)
    #specs=specs+"\n\n\n"+fretboard_specs(fretboard,lang)
    return specs


def fretboard_specs(fretboard,lang):
    cadena=""
    newline="\n"
    #cadena=cadena+str(fretboard["about"])+newline
    cadena=cadena+str(fretboard["fretboard_name"])+newline

    if fretboard["scale_left"]!=fretboard["scale_right"]:
        cadena=cadena+lang["Diapasón multiescala"]+newline
        cadena=cadena+lang["Escala Izquierda: "]+ str(fretboard["scale_left"])+ newline
        cadena=cadena+lang["Escala Derecha: "]+ str(fretboard["scale_right"])+newline
        cadena=cadena+lang["Traste Perpenticular: "]+ str(fretboard["fret_perpenticular_to_centerline"])+newline

    else :
        cadena=cadena+lang["Escala: "]+ str(fretboard["scale_left"])+ newline
    cadena=cadena+lang["Trastes: "]+str(fretboard["number_of_frets"])+newline
    cadena=cadena+ lang["Ancho en Cejuela (centro cuerda E a centro cuerda e): "]+str(fretboard["width_at_zero_line"])+newline+   lang["Ancho en Puente (centro cuerda a centro cuerda)"]+ str(fretboard["width_at_bottom_line"])+newline
    cadena=cadena+lang["Borde izquierdo: "]+str(fretboard["left_border"])+newline
    cadena=cadena+lang["Borde derecho: "]+str(fretboard["right_border"])+newline
    cadena=cadena+lang["Cuerdas: "]+str(len(fretboard["strings"]))+newline
    cadena=cadena+lang["Cordaje: "]+str(fretboard["strings"])+newline
    cadena=cadena+lang["Compensación entonación izquierda"]+str(fretboard["intonation_compensation_left"])+newline
    cadena=cadena+lang["Compensación entonación derecha"]+str(fretboard["intonation_compensation_right"])+newline


#      "strings": [0.046, 0.036, 0.026, 0.017, 0.013, 0.010],
#      "fret_perpenticular_to_centerline":12
    return cadena

def save_to_scale(fretboard,
    size_in_inches: tuple[float, float] = (300/25.4, 1000/25,4),
    origin: tuple[float, float] = (0, 0),  # of modelspace area to render
    scale: float = 1,
    dpi: int = 300,
    filename="filename.pdf",

):
    doc = make_doc(fretboard,offset=(1, 2), size=(6.5, 8))
    msp = doc.modelspace()

    msp.add_mtext(
        "Fretboard Generator \nby Marc Alier 2022 \n"
        ,
        dxfattribs={"style": "OpenSans", "char_height": 0.22},
    ).set_location(
        (0.2, 36.5), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )
    msp.add_mtext(
        "http://aprendizdeluthier.com/fretboard_generator\nScale 1:1"
        ,
        dxfattribs={"style": "OpenSans", "char_height": 0.14},
    ).set_location(
        (0.2, 35.5), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )
    msp.add_mtext(
        "Fretboard Generator \nby Marc Alier 2022 \n"
        ,
        dxfattribs={"style": "OpenSans", "char_height": 0.22},
    ).set_location(
        (0.2, 2), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )
    msp.add_mtext(
        "http://aprendizdeluthier.com/fretboard_generator\nScale 1:1"
        ,
        dxfattribs={"style": "OpenSans", "char_height": 0.16},
    ).set_location(
        (0.2, 1), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )

    msp.add_mtext(
    describe(fretboard,lang_en),
    dxfattribs={"style": "OpenSans", "char_height": 0.13},
    ).set_location(
        (0.2, 32), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )
    msp.add_mtext(
    describe(fretboard,lang_es),
    dxfattribs={"style": "OpenSans", "char_height": 0.13},
    ).set_location(
        (7, 32), attachment_point=MTextEntityAlignment.BOTTOM_LEFT
    )


    ctx = RenderContext(doc)
    fig = plt.figure(dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])

    # Get render limits in drawing units:
    min_x, min_y, max_x, max_y = render_limits(
        origin, size_in_inches, scale
    )
## added by lud
    ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = '#FFFFFF'
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    out = MatplotlibBackend(ax)
    # Finalizing invokes auto-scaling by default!
    Frontend(ctx, out).draw_layout(msp, finalize=False)

    # Set output size in inches:
    fig.set_size_inches(size_in_inches[0], size_in_inches[1], forward=True)
    fig.savefig(filename, dpi=dpi)
    plt.close(fig)

####################################################################
class draw_tool:
    #silly class implemented for rendering nicelly, original coords mean 0,0 is at the nut
    convert = 0
    flip_model=-1
    offset= 750 # arbitrary number
    grid = 5
    def __init__(self):
        self.flip_model=-1

    def add_text(self,msp,palangana, pos, align_):
        pos=[pos[0]+150,self.transform(pos[1])]
        msp.add_mtext(palangana,dxfattribs={"style": "OpenSans", "char_height": 0.10}).set_location((toinch(pos[0],self.convert),toinch(pos[1],self.convert)))


    def transform(self,y):
        return self.offset+(y*self.flip_model)

    def draw_grid(self, msp):
        red_dashed = {"color": 1, "linetype": "dashed"}
        #msp.add_line((-100, 5), (100, 5), dxfattribs=red_dashed)
        msp.add_line((80, -100), (6, 100), dxfattribs=red_dashed)
        n=0
        while n<9:
            msp.add_line(
            (
                toinch(n*50,self.convert) ,toinch(20,self.convert)),
                (toinch(n*50,self.convert),toinch(1200,self.convert)
            ),{"linetype":"DOT2"} )
            msp.add_mtext((n*50),dxfattribs={"style": "OpenSans", "char_height": 0.25}).set_location((toinch(n*50,self.convert),toinch(10,self.convert)))
            msp.add_mtext((n*50),dxfattribs={"style": "OpenSans", "char_height": 0.25}).set_location((toinch(n*50,self.convert),toinch(1210,self.convert)))
            n=n+1
        return

    def draw_circle(self,msp,centre,radi):
        x=toinch(centre[0]+150,self.convert)
        y=toinch(self.transform(centre[1]),self.convert)
        msp.add_circle((x,y), radius=toinch(radi,self.convert))
        return

    def draw_line(self,msp,x1,y1,x2,y2,atribs={"linetype":"CONTIUNUOUS"} ) :
        y1=toinch(self.transform(y1),self.convert)
        y2=toinch(self.transform(y2),self.convert)
        x1=toinch(x1+150,self.convert)
        x2=toinch(x2+150,self.convert)
        msp.add_line((x1,y1),(x2,y2),dxfattribs=atribs)
        return

    def draw_line_list(self,msp,line,atribs={"linetype":"CONTIUNUOUS"}):
        self.draw_line(msp,line[0][0],line[0][1],line[1][0],line[1][1],atribs=atribs)
