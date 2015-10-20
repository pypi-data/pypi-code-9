"""
peeksrc

Main Routine for peekextn module

Peek into the sources and list the file types contained in the sources.
Also, enable display the sources in tree format.

"""


# Main Routine
if __name__ == "__main__":
    import peekextn

    source = peekextn.peeksrc.peeksrc()
    source.createExtnNodes()
    source.showextn()
    #source.genreport()

    
