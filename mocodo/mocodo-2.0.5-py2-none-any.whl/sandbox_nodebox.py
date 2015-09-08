# Généré par Mocodo 2.0.4 le Tue, 08 Sep 2015 15:58:30

(width,height) = (1163.0,610.0)
cx = {
    u"PEUT VIVRE DANS"    :  248.00,
    u"ENCLOS"             :  571.00,
    u"OCCUPE"             :  806.00,
    u"PÉRIODE"            :  1047.00,
    u"ESPÈCE"             :  248.00,
    u"DF"                 :  571.00,
    u"ANIMAL"             :  806.00,
    u"A MÈRE"             :  1047.00,
    u"PEUT COHABITER AVEC":  248.00,
    u"A PÈRE"             :  806.00,
}
cy = {
    u"PEUT VIVRE DANS"    :  94.00,
    u"ENCLOS"             :  94.00,
    u"OCCUPE"             :  94.00,
    u"PÉRIODE"            :  94.00,
    u"ESPÈCE"             :  324.00,
    u"DF"                 :  324.00,
    u"ANIMAL"             :  324.00,
    u"A MÈRE"             :  324.00,
    u"PEUT COHABITER AVEC":  535.00,
    u"A PÈRE"             :  535.00,
}
k = {
    u"PEUT VIVRE DANS,ESPÈCE"         :  1.00,
    u"PEUT VIVRE DANS,ENCLOS"         :  1.00,
    u"OCCUPE,ANIMAL"                  :  1.00,
    u"OCCUPE,PÉRIODE"                 :  1.00,
    u"OCCUPE,ENCLOS"                  :  1.00,
    u"DF,ESPÈCE"                      :  1.00,
    u"DF,ANIMAL"                      :  1.00,
    u"A MÈRE,ANIMAL,-1.0"             : -4.00,
    u"A MÈRE,ANIMAL,1.0"              :  4.00,
    u"PEUT COHABITER AVEC,ESPÈCE,-1.0": -4.00,
    u"PEUT COHABITER AVEC,ESPÈCE,1.0" :  4.00,
    u"A PÈRE,ANIMAL,-1.0"             : -4.00,
    u"A PÈRE,ANIMAL,1.0"              :  4.00,
}
t = {
    u"A MÈRE,ANIMAL,1.0":  0.50,
    u"A PÈRE,ANIMAL,1.0":  0.50,
}
colors = {
    u"annotation_color"                : u'#000000',
    u"annotation_text_color"           : u'#FFFFFF',
    u"association_attribute_text_color": u'#000000',
    u"association_cartouche_color"     : u'#FFFFFF',
    u"association_cartouche_text_color": u'#000000',
    u"association_color"               : u'#FFFFFF',
    u"association_stroke_color"        : u'#000000',
    u"background_color"                : None,
    u"card_text_color"                 : u'#000000',
    u"entity_attribute_text_color"     : u'#000000',
    u"entity_cartouche_color"          : u'#FFFFFF',
    u"entity_cartouche_text_color"     : u'#000000',
    u"entity_color"                    : u'#FFFFFF',
    u"entity_stroke_color"             : u'#000000',
    u"label_text_color"                : u'#000000',
    u"leg_stroke_color"                : u'#000000',
    u"transparent_color"               : None,
}

for c in colors: colors[c] = (color(*[int((colors[c]+"FF")[i:i+2],16)/255.0 for i in range(1,9,2)]) if colors[c] else None)
card_max_width = 36
card_max_height = 28
card_margin = 8.0
arrow_width = 24.0
arrow_half_height = 12.0
arrow_axis = 16.0

def card_pos(ex, ey, ew, eh, ax, ay, k):
    if ax != ex and abs(float(ay - ey) / (ax - ex)) < float(eh) / ew:
        (x0, x1) = (ex + cmp(ax, ex) * (ew + card_margin), ex + cmp(ax, ex) * (ew + card_margin + card_max_width))
        (y0, y1) = sorted([ey + (x0 - ex) * (ay - ey) / (ax - ex), ey + (x1 - ex) * (ay - ey) / (ax - ex)])
        return (min(x0, x1), (y0 + y1 - card_max_height + k * abs(y1 - y0 + card_max_height)) / 2 + cmp(k, 0) * card_margin)
    else:
        (y0, y1) = (ey + cmp(ay, ey) * (eh + card_margin), ey + cmp(ay, ey) * (eh + card_margin + card_max_height))
        (x0, x1) = sorted([ex + (y0 - ey) * (ax - ex) / (ay - ey), ex + (y1 - ey) * (ax - ex) / (ay - ey)])
        return ((x0 + x1 - card_max_width + k * abs(x1 - x0 + card_max_width)) / 2 + cmp(k, 0) * card_margin, min(y0, y1))


def line_arrow(x0, y0, x1, y1, t):
    (x, y) = (t * x0 + (1 - t) * x1, t * y0 + (1 - t) * y1)
    return arrow(x, y, x1 - x0, y0 - y1)


def curve_arrow(x0, y0, x1, y1, x2, y2, x3, y3, t):
    (cx, cy) = (3 * (x1 - x0), 3 * (y1 - y0))
    (bx, by) = (3 * (x2 - x1) - cx, 3 * (y2 - y1) - cy)
    (ax, ay) = (x3 - x0 - cx - bx, y3 - y0 - cy - by)
    t = 1 - t
    bezier = lambda t: (ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0)
    (x, y) = bezier(t)
    u = 1.0
    while t < u:
        m = (u + t) / 2.0
        (xc, yc) = bezier(m)
        d = ((x - xc)**2 + (y - yc)**2)**0.5
        if abs(d - arrow_axis) < 0.01:
            break
        if d > arrow_axis:
            u = m
        else:
            t = m
    return arrow(x, y, xc - x, y - yc)


def round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w - r, y)
    curveto(x + w, y, x + w, y + r, x + w, y + r)
    lineto(x + w, y + h - r)
    curveto(x + w, y + h - r, x + w, y + h, x + w - r, y + h)
    lineto(x + r, y + h)
    curveto(x, y + h, x, y + h - r, x, y + h - r)
    lineto(x, y + r)
    curveto(x, y + r, x, y, x + r, y)
    lineto(x + w - r, y)
    endpath()


def upper_round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w - r, y)
    curveto(x + w, y, x + w, y + r, x + w, y + r)
    lineto(x + w, y + h)
    lineto(x, y + h)
    lineto(x, y + r)
    curveto(x, y + r, x, y, x + r, y)
    lineto(x + w - r, y)
    endpath()


def lower_round_rect(x, y, w, h, r):
    beginpath()
    moveto(x + w, y)
    lineto(x + w, y + h - r)
    curveto(x + w, y + h - r, x + w, y + h, x + w - r, y + h)
    lineto(x + r, y + h)
    curveto(x, y + h, x, y + h - r, x, y + h - r)
    lineto(x, y)
    lineto(x + w, y)
    endpath()


def dash_line(x0, x1, y, w):
    nofill()
    beginpath(x0, y)
    for i in range(int(x0 + 0.5), int(x1 + 0.5), int(2 * w + 0.5)):
        lineto(min(i + w, x1), y)
        moveto(i + 2 * w, y)
    endpath()


def curve(x0, y0, x1, y1, x2, y2, x3, y3):
    nofill()
    beginpath(x0, y0)
    curveto(x1, y1, x2, y2, x3, y3)
    endpath()


def arrow(x, y, a, b):
    c = (a * a + b * b)**0.5
    (cos, sin) = (a / c, b / c)
    beginpath(x, y)
    lineto(x + arrow_width * cos - arrow_half_height * sin,
           y - arrow_half_height * cos - arrow_width * sin)
    lineto(x + arrow_axis * cos, y - arrow_axis * sin)
    lineto(x + arrow_width * cos + arrow_half_height * sin,
           y + arrow_half_height * cos - arrow_width * sin)
    lineto(x, y)
    endpath()


size(width,height)
autoclosepath(False)
background(colors['background_color'])

# Association PEUT COHABITER AVEC
(x,y) = (cx[u"PEUT COHABITER AVEC"],cy[u"PEUT COHABITER AVEC"])
strokewidth(2.0)
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*-1.0)/4,(3*ey+y+(x-ex)*-1.0)/4,(3*x+ex+(y-ey)*-1.0)/4,(3*y+ey+(x-ex)*-1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,93.0,76.0,x,23.8+y,k[u"PEUT COHABITER AVEC,ESPÈCE,-1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
strokewidth(2.0)
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*1.0)/4,(3*ey+y+(x-ex)*1.0)/4,(3*x+ex+(y-ey)*1.0)/4,(3*y+ey+(x-ex)*1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,93.0,76.0,x,23.8+y,k[u"PEUT COHABITER AVEC,ESPÈCE,1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
strokewidth(0)
stroke(colors["association_cartouche_color"])
fill(colors["association_cartouche_color"])
upper_round_rect(-230.0+x,-57.0+y,460.0,56.0,28.0)
stroke(colors["association_color"])
fill(colors["association_color"])
lower_round_rect(-230.0+x,-1.0+y,460.0,58.0,28.0)
fill(colors["transparent_color"])
stroke(colors["association_stroke_color"])
strokewidth(3.0)
round_rect(-230.0+x,-57.0+y,460.0,114.0,28.0)
strokewidth(3.0)
line(-230.0+x,-1.0+y,230.0+x,-1.0+y)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"PEUT COHABITER AVEC",-216+x,-14.4+y)
fill(colors["association_attribute_text_color"]);font("Gill Sans",30.0);text(u"nb. max. commensaux",-216.0+x,35.1+y)

# Association DF
(x,y) = (cx[u"DF"],cy[u"DF"])
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,93.0,76.0,x,23.8+y,k[u"DF,ESPÈCE"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"DF,ANIMAL"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,1",tx,ty)
strokewidth(2.0)
stroke(colors["card_text_color"])
strokewidth(3.0)
stroke(colors["association_stroke_color"])
fill(colors["association_cartouche_color"])
oval(x-38.0,y-38.0,2*38.0,2*38.0)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"DF",-24.0+x,11.6+y)

# Association OCCUPE
(x,y) = (cx[u"OCCUPE"],cy[u"OCCUPE"])
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"OCCUPE,ANIMAL"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,N",tx,ty)
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"PÉRIODE"],cy[u"PÉRIODE"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,98.0,76.0,x,23.8+y,k[u"OCCUPE,PÉRIODE"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,N",tx,ty)
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,92.0,59.0,x,23.8+y,k[u"OCCUPE,ENCLOS"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,N",tx,ty)
strokewidth(0)
stroke(colors["association_cartouche_color"])
fill(colors["association_cartouche_color"])
upper_round_rect(-91.0+x,-57.0+y,182.0,56.0,28.0)
stroke(colors["association_color"])
fill(colors["association_color"])
lower_round_rect(-91.0+x,-1.0+y,182.0,58.0,28.0)
fill(colors["transparent_color"])
stroke(colors["association_stroke_color"])
strokewidth(3.0)
round_rect(-91.0+x,-57.0+y,182.0,114.0,28.0)
strokewidth(3.0)
line(-91.0+x,-1.0+y,91.0+x,-1.0+y)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"OCCUPE",-77+x,-14.4+y)

# Association A PÈRE
(x,y) = (cx[u"A PÈRE"],cy[u"A PÈRE"])
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*-1.0)/4,(3*ey+y+(x-ex)*-1.0)/4,(3*x+ex+(y-ey)*-1.0)/4,(3*y+ey+(x-ex)*-1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"A PÈRE,ANIMAL,-1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*1.0)/4,(3*ey+y+(x-ex)*1.0)/4,(3*x+ex+(y-ey)*1.0)/4,(3*y+ey+(x-ex)*1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"A PÈRE,ANIMAL,1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
fill(colors["leg_stroke_color"])
strokewidth(0)
curve_arrow(ex,ey,(3*ex+x+(y-ey)*1.0)/4,(3*ey+y+(x-ex)*1.0)/4,(3*x+ex+(y-ey)*1.0)/4,(3*y+ey+(x-ex)*1.0)/4,x,y,1-t[u"A PÈRE,ANIMAL,1.0"])
strokewidth(0)
stroke(colors["association_cartouche_color"])
fill(colors["association_cartouche_color"])
upper_round_rect(-81.0+x,-57.0+y,162.0,56.0,28.0)
stroke(colors["association_color"])
fill(colors["association_color"])
lower_round_rect(-81.0+x,-1.0+y,162.0,58.0,28.0)
fill(colors["transparent_color"])
stroke(colors["association_stroke_color"])
strokewidth(3.0)
round_rect(-81.0+x,-57.0+y,162.0,114.0,28.0)
strokewidth(3.0)
line(-81.0+x,-1.0+y,81.0+x,-1.0+y)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"A PÈRE",-67+x,-14.4+y)

# Association A MÈRE
(x,y) = (cx[u"A MÈRE"],cy[u"A MÈRE"])
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*-1.0)/4,(3*ey+y+(x-ex)*-1.0)/4,(3*x+ex+(y-ey)*-1.0)/4,(3*y+ey+(x-ex)*-1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"A MÈRE,ANIMAL,-1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,1",tx,ty)
strokewidth(2.0)
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
stroke(colors["leg_stroke_color"])
curve(ex,ey,(3*ex+x+(y-ey)*1.0)/4,(3*ey+y+(x-ex)*1.0)/4,(3*x+ex+(y-ey)*1.0)/4,(3*y+ey+(x-ex)*1.0)/4,x,y)
(tx,ty)=card_pos(ex,23.8+ey,105.0,110.0,x,23.8+y,k[u"A MÈRE,ANIMAL,1.0"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"0,N",tx,ty)
fill(colors["leg_stroke_color"])
strokewidth(0)
curve_arrow(ex,ey,(3*ex+x+(y-ey)*1.0)/4,(3*ey+y+(x-ex)*1.0)/4,(3*x+ex+(y-ey)*1.0)/4,(3*y+ey+(x-ex)*1.0)/4,x,y,1-t[u"A MÈRE,ANIMAL,1.0"])
strokewidth(0)
stroke(colors["association_cartouche_color"])
fill(colors["association_cartouche_color"])
upper_round_rect(-84.0+x,-57.0+y,168.0,56.0,28.0)
stroke(colors["association_color"])
fill(colors["association_color"])
lower_round_rect(-84.0+x,-1.0+y,168.0,58.0,28.0)
fill(colors["transparent_color"])
stroke(colors["association_stroke_color"])
strokewidth(3.0)
round_rect(-84.0+x,-57.0+y,168.0,114.0,28.0)
strokewidth(3.0)
line(-84.0+x,-1.0+y,84.0+x,-1.0+y)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"A MÈRE",-70+x,-14.4+y)

# Association PEUT VIVRE DANS
(x,y) = (cx[u"PEUT VIVRE DANS"],cy[u"PEUT VIVRE DANS"])
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,93.0,76.0,x,23.8+y,k[u"PEUT VIVRE DANS,ESPÈCE"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,N",tx,ty)
stroke(colors["leg_stroke_color"])
strokewidth(2.0)
(ex,ey) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
line(ex,ey,x,y)
(tx,ty)=card_pos(ex,23.8+ey,92.0,59.0,x,23.8+y,k[u"PEUT VIVRE DANS,ENCLOS"]);fill(colors["card_text_color"]);font("Futura",22.0);text(u"1,N",tx,ty)
strokewidth(0)
stroke(colors["association_cartouche_color"])
fill(colors["association_cartouche_color"])
upper_round_rect(-179.0+x,-57.0+y,358.0,56.0,28.0)
stroke(colors["association_color"])
fill(colors["association_color"])
lower_round_rect(-179.0+x,-1.0+y,358.0,58.0,28.0)
fill(colors["transparent_color"])
stroke(colors["association_stroke_color"])
strokewidth(3.0)
round_rect(-179.0+x,-57.0+y,358.0,114.0,28.0)
strokewidth(3.0)
line(-179.0+x,-1.0+y,179.0+x,-1.0+y)
fill(colors["association_cartouche_text_color"]);font("Copperplate",36.0);text(u"PEUT VIVRE DANS",-165+x,-14.4+y)
fill(colors["association_attribute_text_color"]);font("Gill Sans",30.0);text(u"nb. max. congénères",-165.0+x,35.1+y)

# Entity ENCLOS
(x,y) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
strokewidth(0)
stroke(colors["entity_cartouche_color"])
fill(colors["entity_cartouche_color"])
rect(-92.0+x,-59.0+y,184.0,60.0)
stroke(colors["entity_color"])
fill(colors["entity_color"])
rect(-92.0+x,1.0+y,184.0,58.0)
stroke(colors["entity_stroke_color"])
strokewidth(3.0)
fill(colors["transparent_color"])
rect(-92.0+x,-59.0+y,184.0,118.0)
strokewidth(3.0)
line(-92.0+x,1.0+y,92.0+x,1.0+y)
fill(colors["entity_cartouche_text_color"]);font("Copperplate",36.0);text(u"ENCLOS",-76+x,-16.4+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"num. enclos",-76.0+x,35.1+y)
strokewidth(2.0)
stroke(colors["entity_attribute_text_color"])
line(-76.0+x,41.0+y,72.0+x,41.0+y)

# Entity ANIMAL
(x,y) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
strokewidth(0)
stroke(colors["entity_cartouche_color"])
fill(colors["entity_cartouche_color"])
rect(-105.0+x,-110.0+y,210.0,60.0)
stroke(colors["entity_color"])
fill(colors["entity_color"])
rect(-105.0+x,-50.0+y,210.0,160.0)
stroke(colors["entity_stroke_color"])
strokewidth(3.0)
fill(colors["transparent_color"])
rect(-105.0+x,-110.0+y,210.0,220.0)
strokewidth(3.0)
line(-105.0+x,-50.0+y,105.0+x,-50.0+y)
fill(colors["entity_cartouche_text_color"]);font("Copperplate",36.0);text(u"ANIMAL",-70+x,-67.4+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"nom",-89.0+x,-15.9+y)
strokewidth(2.0)
stroke(colors["entity_attribute_text_color"])
dash_line(-89.0+x,-33.0+x,-10.0+y,8.0)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"sexe",-89.0+x,18.1+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"date naissance",-89.0+x,52.1+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"date décès",-89.0+x,86.1+y)

# Entity ESPÈCE
(x,y) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
strokewidth(0)
stroke(colors["entity_cartouche_color"])
fill(colors["entity_cartouche_color"])
rect(-93.0+x,-76.0+y,186.0,60.0)
stroke(colors["entity_color"])
fill(colors["entity_color"])
rect(-93.0+x,-16.0+y,186.0,92.0)
stroke(colors["entity_stroke_color"])
strokewidth(3.0)
fill(colors["transparent_color"])
rect(-93.0+x,-76.0+y,186.0,152.0)
strokewidth(3.0)
line(-93.0+x,-16.0+y,93.0+x,-16.0+y)
fill(colors["entity_cartouche_text_color"]);font("Copperplate",36.0);text(u"ESPÈCE",-73+x,-33.4+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"code espèce",-77.0+x,18.1+y)
strokewidth(2.0)
stroke(colors["entity_attribute_text_color"])
line(-77.0+x,24.0+y,77.0+x,24.0+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"libellé",-77.0+x,52.1+y)

# Entity PÉRIODE
(x,y) = (cx[u"PÉRIODE"],cy[u"PÉRIODE"])
strokewidth(0)
stroke(colors["entity_cartouche_color"])
fill(colors["entity_cartouche_color"])
rect(-98.0+x,-76.0+y,196.0,60.0)
stroke(colors["entity_color"])
fill(colors["entity_color"])
rect(-98.0+x,-16.0+y,196.0,92.0)
stroke(colors["entity_stroke_color"])
strokewidth(3.0)
fill(colors["transparent_color"])
rect(-98.0+x,-76.0+y,196.0,152.0)
strokewidth(3.0)
line(-98.0+x,-16.0+y,98.0+x,-16.0+y)
fill(colors["entity_cartouche_text_color"]);font("Copperplate",36.0);text(u"PÉRIODE",-82+x,-33.4+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"date début",-82.0+x,18.1+y)
strokewidth(2.0)
stroke(colors["entity_attribute_text_color"])
line(-82.0+x,24.0+y,51.0+x,24.0+y)
fill(colors["entity_attribute_text_color"]);font("Gill Sans",30.0);text(u"date fin",-82.0+x,52.1+y)
strokewidth(2.0)
stroke(colors["entity_attribute_text_color"])
line(-82.0+x,58.0+y,10.0+x,58.0+y)