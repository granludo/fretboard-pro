import json
import markdown

def multiscale_2_markdonw(fretboard):
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

f = open( 'tmp.json',"r")
fretboard = json.load(f)
md_text=fretb_2_markdown(fretboard)
print(md_text)
html = markdown.markdown(md_text,extensions=["tables"])
print(html)
f = open( 'tmp.html',"w")
f.write(html)
