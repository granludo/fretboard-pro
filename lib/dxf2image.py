import matplotlib.pyplot as plt
import matplotlib.style
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
#import wx
import glob
import re
import os


default_img_format = '.png'
default_img_res = 300
default_bg_color = '#FFFFFF' #White
def convert_dxf2img( names, folder, img_format=default_img_format, img_res=default_img_res, clr=default_bg_color):
    for name in names:
        doc = ezdxf.readfile(name)
        msp = doc.modelspace()
        # Recommended: audit & repair DXF document before rendering
        auditor = doc.audit()
        # The auditor.errors attribute stores severe errors,
        # which *may* raise exceptions when rendering.
        if len(auditor.errors) != 0:
            raise Exception("This DXF document is damaged and can't be converted! --> ", name)
            name = name =+ 1
        else :
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(doc)
            ctx.set_current_layout(msp)
            ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = clr
            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(msp, finalize=True)

            img_name = re.findall("(\S+)\.",name)  # select the image name that is the same as the dxf file name
            first_param = ''.join(img_name) + img_format  #concatenate list and string
            first_param=folder+os.path.basename(first_param)
            fig.savefig(first_param, dpi=img_res)
            print(name," Converted Successfully")


#convert_dxf2img(["fretboard_test.dxf"])
