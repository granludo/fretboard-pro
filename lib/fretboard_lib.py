
from numpy import *
import ezdxf

x=0
y=1
left=0
right=1
def calculate_strings(fretboard):

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
    left_border=[
        [zero_line[left][x]+fretboard["left_border"],0],
        [bottom_line[left][x]+fretboard["left_border"],max_scale]
    ]
    fretboard["left_border"]=left_border
    right_border=[
        [zero_line[right][x]-fretboard["right_border"],0],
        [bottom_line[right][x]-fretboard["right_border"],max_scale]
    ]
    fretboard["right_border"]=right_border
    return fretboard


def  generate_frame(msp,draw,fretboard):

    draw.draw_line_list(msp,fretboard["zero_line"])
    draw.draw_line_list(msp,fretboard["bottom_line"])
    draw.draw_line_list(msp,fretboard["left_side"])
    draw.draw_line_list(msp,fretboard["right_side"])
    draw.draw_line_list(msp,fretboard["left_border"])
    draw.draw_line_list(msp,fretboard["right_border"])

def generate_dxf(fretboard, fname) :
    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = 4 #sets units to milimeters
    msp = doc.modelspace()
    draw=draw_tool()

    generate_frame(msp,draw,fretboard)
    doc.saveas(fname)




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

    def draw_line(self,msp,x1,y1,x2,y2) :
        y1=self.transform(y1)
        y2=self.transform(y2)
        msp.add_line((x1,y1),(x2,y2))

    def draw_line_list(self,msp,line):
        print("line:"+str(line))
        self.draw_line(msp,line[0][0],line[0][1],line[1][0],line[1][1])
