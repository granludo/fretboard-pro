
from numpy import *
import ezdxf
from ezdxf import units
from lib import intersect

x=0
y=1
left=0
right=1

def calculate_space_between_strings_zero_line(fretboard):
    s=0;
    strings_acumulated_width=0
    for string in fretboard["strings"]:
        width_in_mm=string*25.4
        strings_acumulated_width=strings_acumulated_width+width_in_mm
    B3=fretboard["width_at_zero_line"]
    B4=fretboard["left_border"]
    B5=fretboard["right_border"]
    return (B3-B4-B5-strings_acumulated_width) / (len(fretboard["strings"])-1)

def calculate_space_between_strings_bottom_line(fretboard):
    s=0;
    strings_acumulated_width=0
    if fretboard["bridge_spacing_compensated"]==1:
    ## if the bridge has string spacing adjustment , else the calculation is just proportional
        for string in fretboard["strings"]:
            width_in_mm=string*25.4
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
    for string in fretboard["strings"]:
        zero_offset=zero_offset+((string*25.4)/2)
        bottom_offset=bottom_offset+((string*25.4)/2)
        center_offsets.append([zero_offset,bottom_offset])
        bottom_offset=bottom_offset+space_between_strings_bottom_line+((string*25.4)/2)
        zero_offset=zero_offset+space_between_strings_zero_line+((string*25.4)/2)
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

    draw.draw_line_list(msp,fretboard["zero_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["bottom_line"],{"linetype":"DOT2"})
    msp.add_text(str(fretboard["bottom_line"])+" mm").set_pos((-150,draw.transform(fretboard["bottom_line"][0][1])), align='LEFT')
    draw.draw_line_list(msp,fretboard["left_side"])
    draw.draw_line_list(msp,fretboard["right_side"])
    draw.draw_line_list(msp,[[0,-300],[0,900]],{"linetype":"CENTER"})
    draw.draw_line_list(msp,fretboard["left_border_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["right_border_line"],{"linetype":"DOT2"})
    draw.draw_line_list(msp,fretboard["comprensated_bridge"])
    if   fretboard["bridge_multiscale_compensation"]>0 :
        draw.draw_line_list(msp,
        [fretboard["comprensated_bridge"][1],[150,fretboard["comprensated_bridge"][1][1]]],{"linetype":"DOT2"})
        msp.add_text("Compensation:"+str(fretboard["bridge_multiscale_compensation"])+" mm").set_pos((150,draw.transform(fretboard["comprensated_bridge"][1][1])), align='RIGHT')

    return


def generate_strings(msp,draw,fretboard):
    for string in fretboard["strings_segments"]:
        draw.draw_line_list(msp,string,{"linetype":"DASHED2"})
    for string in fretboard["extended_strings_segments"]:
        draw.draw_line_list(msp,string,{"linetype":"DASHED2"})
    return

def generate_dxf(fretboard, fname) :
    doc = ezdxf.new('R12', setup=True)
#    doc.header['$INSUNITS'] = 4 #sets units to milimeters
    doc.units = units.MM
    msp = doc.modelspace()
    draw=draw_tool()
    generate_frame(msp,draw,fretboard)
    generate_strings(msp,draw,fretboard)
    generate_frets(msp,draw,fretboard)
#    draw.draw_line(msp,1,1,100,100)
    doc.saveas(fname)
    return

def generate_frets(msp,draw,fretboard):
    for fret in fretboard["scale_positions"][left]:
        draw.draw_line(msp,-150,fret,-fretboard["width_at_bottom_line"]/2,fret,{"linetype":"DOT"})
        msp.add_text(str(fret)+" mm").set_pos((-200,draw.transform(fret)), align='LEFT')

    for fret in fretboard["scale_positions"][right]:
        draw.draw_line(msp,fretboard["width_at_bottom_line"]/2,fret,150,fret,{"linetype":"DOT"})
        msp.add_text(str(fret)+" mm").set_pos((160,draw.transform(fret)), align='RIGHT')
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
    frets_left=calculate_scale(fretboard["scale_left"],fretboard["number_of_frets"])
    frets_right=calculate_scale(fretboard["scale_right"],fretboard["number_of_frets"])
    number=fretboard["fret_perpenticular_to_centerline"]
    lfret_from_bridge=frets_left[number]
    rfret_from_bridge=fretboard["scale_right"]-frets_right[number]
    fretboard["bridge_multiscale_compensation"] = lfret_from_bridge-rfret_from_bridge
    frets_right=calculate_scale(fretboard["scale_right"],fretboard["number_of_frets"],
        fretboard["bridge_multiscale_compensation"])
    fretboard["scale_positions"]=[frets_left,frets_right]
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
    while n< fretboard["number_of_frets"]:
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
    return fretboard

class draw_tool:
    #silly class implemented for rendering nicelly, original coords mean 0,0 is at the nut
    flip_model=-1
    offset= 750 # arbitrary number
    grid = 5
    def __init__(self):
        self.flip_model=-1

    def transform(self,y):
        return self.offset+(y*self.flip_model)

    def draw_grid(self, msp):
        if grid <0 :
            return
        n=0
        while n<600:
            msp.add_line((-300, n), (300, n),dxfattribs={"linetype": "CENTER"}) #hoizontal grid
            msp.add_line((0, n), (0, 0),dxfattribs={"linetype": "DOTTED"}) #vertical grid
            n=n+self.grid

    def draw_line(self,msp,x1,y1,x2,y2,atribs={"linetype":"CONTIUNUOUS"} ) :
        y1=self.transform(y1)
        y2=self.transform(y2)
        msp.add_line((x1,y1),(x2,y2),dxfattribs=atribs)

    def draw_line_list(self,msp,line,atribs={"linetype":"CONTIUNUOUS"}):
        self.draw_line(msp,line[0][0],line[0][1],line[1][0],line[1][1],atribs=atribs)
