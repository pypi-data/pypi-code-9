from __future__ import unicode_literals, print_function

def read_spex_file(filename):
    with open(filename, "r", encoding = 'utf8') as f:
        spexcript = load_spexcript(f)
    return spexcript # the spex itself

def main(filename, *args):
    try:
        spex = read_spex_file(filename)
    except FileNotFoundError:
        print("File '" + filename + "' not found")
        return -1
    from .language import Finnish
    from . import latex
    spextex = latex.Spextex(Finnish)
    spex.generate_front_page(spextex)
    spex.generate_characters(spextex)
    spex.generate_listing(spextex)
    spex.generate_script(spextex)
    tex = spextex.final_result()
    latex.pdflatex(tex)
    latex.show()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]))