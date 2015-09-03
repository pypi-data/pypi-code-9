from __future__ import print_function
import sys
from json import loads as _json_loads
from reportlab.pdfgen import canvas
import os.path
from optparse import OptionParser

UNKNOWN = '.'
SUDOKU_SIZE = (9, 9)
CELL_SIZE = (3, 3)
SUDOKU_FONT_SIZE = 30
SUDOKU_PDF_OFFSET = (110, 200)
SUDOKU_XPAD, SUDOKU_YPAD = (5, 5)
DIFFERENCE_FOR_NUMBERS = ((SUDOKU_FONT_SIZE + SUDOKU_XPAD) // 2,
                          (SUDOKU_FONT_SIZE + SUDOKU_YPAD) // 2)


class Sudoku(object):

    def __init__(self, mat):
        self._mat = mat

        for row in mat:
            if not isinstance(row, list):
                raise ValueError("row should be list.")
            for col in row:
                if (not isinstance(col, int) or (col <= 0 or col >= 10)) and \
                        col != UNKNOWN:
                    raise ValueError("Illegal Value: {}".format(col))

    @property
    def mat(self):
        return self._mat

    @staticmethod
    def loads(text):
        matrixes = _json_loads(text)
        return [Sudoku(mat) for mat in matrixes]

    @staticmethod
    def load(f):
        return Sudoku.loads(f.read())

    def __eq__(self, other):
        return self.mat == other.mat


class SudokuPageInfo(object):

    def __init__(self, sudoku, title,
                 show_page_number=False, page_number=None, show_title=True):
        self._sudoku = sudoku
        self._show_title = show_title
        self._title = title
        self._show_page_number = show_page_number
        self._page_number = page_number

    @property
    def sudoku(self):
        return self._sudoku

    @property
    def show_title(self):
        return self._show_title

    @property
    def title(self):
        return self._title

    @property
    def show_page_number(self):
        return self._show_page_number

    @property
    def page_number(self):
        return self._page_number

    def write_pdf(self, canvas):
        canvas.setFont("Helvetica", 70)
        if self.show_title:
            canvas.drawString(70, 70, self.title)

        canvas.setFont("Helvetica", SUDOKU_FONT_SIZE)
        sudoku_offset = SUDOKU_PDF_OFFSET
        xlist = [sudoku_offset[0] + j *
                 (2 * SUDOKU_XPAD + SUDOKU_FONT_SIZE) for j in range(0, 9 + 1)]
        ylist = [sudoku_offset[1] + j *
                 (2 * SUDOKU_YPAD + SUDOKU_FONT_SIZE) for j in range(0, 9 + 1)]
        canvas.grid(xlist, ylist)
        for x in range(0, 9):
            for y in range(0, 9):
                if self.sudoku.mat[y][x] != UNKNOWN:
                    canvas.drawString(
                        sudoku_offset[0] +
                        (SUDOKU_FONT_SIZE + SUDOKU_XPAD) // 2
                        + x * (2 * SUDOKU_XPAD + SUDOKU_FONT_SIZE) - 4,
                        sudoku_offset[1] + SUDOKU_FONT_SIZE
                        + y * (2 * SUDOKU_YPAD + SUDOKU_FONT_SIZE),
                        str(self.sudoku.mat[y][x])
                    )

        if self.show_page_number:
            canvas.setFont("Helvetica", 10)
            canvas.drawString(280, 800, str(self.page_number))

        # draw a cell
        canvas.setLineWidth(3)
        canvas.grid(xlist[::3], ylist[::3])


def get_option_parser():
    parser = OptionParser()
    parser.add_option(
        '--hidden-page-number',
        action='store_true',
        dest='hidden_page_number',
        help="don't show page number"
    )
    parser.add_option(
        '--hidden-title',
        action='store_true',
        dest='hidden_title',
        help="don't show title (default: Problem or Answer) "
    )
    parser.add_option(
        '-o', '--output',
        action='store',
        dest='out_filename',
        help='output filename'
    )
    parser.add_option(
        '--problem-name',
        action='store',
        dest='problem_name',
        help=('problem_name is used in title of problem page like this:'
              'problem_name {number}')
    )
    parser.add_option(
        '--answer-name',
        action='store',
        dest='answer_name',
        help=('answer_name is used in title of answer page like this:'
              'answer_name {number}')
    )
    return parser


def error(msg):
    """ this function is called in main function """
    print(msg, file=sys.stderr)
    sys.exit()


def main():
    parser = get_option_parser()
    (options, filenames) = parser.parse_args()
    show_page_number = not(bool(options.hidden_page_number))
    show_title = not(bool(options.hidden_title))

    if len(filenames) >= 3:
        error('Filenames are too many.')

    if options.out_filename is None:
        out_filename = os.path.splitext(filenames[0])[0] + '.pdf'
    else:
        out_filename = options.out_filename

    if options.problem_name is None:
        problem_name = 'Problem'
    else:
        problem_name = options.problem_name

    if options.answer_name is None:
        answer_name = 'Answer'
    else:
        answer_name = options.answer_name

    c = canvas.Canvas(
        out_filename, bottomup=False)

    if len(filenames) == 1:  # case: only problem files
        json_filename = filenames[0]
        try:
            with open(json_filename) as f:
                sudokus = Sudoku.load(f)
        except FileNotFoundError:
            error('Filename {} is not found.'.format(json_filename))
        except ValueError:
            error('Illegal format')

        page_infos = []
        for j, sudoku in enumerate(sudokus):
            page_infos.append(SudokuPageInfo(sudoku, '{} {}'.format(
                problem_name, j + 1),
                show_page_number=show_page_number,
                show_title=show_title,
                page_number=j + 1))

    elif len(filenames) == 2:
        prob_filename, ques_filename = filenames
        try:
            with open(prob_filename) as f:
                prob_sudokus = Sudoku.load(f)
        except FileNotFoundError:
            error('Filename {} is not found.'.format(prob_filename))
        except ValueError:
            error('Illegal format')

        try:
            with open(ques_filename) as f:
                ques_sudokus = Sudoku.load(f)
        except FileNotFoundError:
            error('Filename {} is not found'.format(ques_filename))
        except ValueError:
            error('Illegal format')

        page_infos = []
        page_number = 1
        for j, sudoku in enumerate(prob_sudokus):
            page_infos.append(
                SudokuPageInfo(sudoku, '{} {}'.format(problem_name, j + 1),
                               show_page_number=show_page_number,
                               show_title=show_title,
                               page_number=page_number))
            page_number += 1
        for j, sudoku in enumerate(ques_sudokus):
            page_infos.append(
                SudokuPageInfo(sudoku, '{} {}'.format(answer_name, j + 1),
                               show_page_number=show_page_number,
                               show_title=show_title,
                               page_number=page_number))
            page_number += 1

    for i, page_info in enumerate(page_infos):
        page_info.write_pdf(c)
        if i != len(page_infos) - 1:
            c.showPage()

    c.save()

if __name__ == '__main__':
    main()
