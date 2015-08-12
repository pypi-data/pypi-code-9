
def axesfontsize(ax,fontsize):
    items = ([ax.title,ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels())
    for item in items:
        item.set_fontsize(fontsize)
