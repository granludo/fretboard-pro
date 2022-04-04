#
# line segment intersection using vectors
# see Computer Graphics by F.S. Hill
#
from numpy import *
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def extend_line(ymin,line):
    return extend(ymin,
    line[1][0],line[1][1],line[0][0],line[0][1])

#xmin,ymin,xmax, ymax defineixen boundaries
def extend(ymin, x1, y1, x2, y2):
    #returns X value when Y=ymin
    a=(y2-y1)/(x2-x1)
    b=y1-a*x1
    return (ymin-b)/a
