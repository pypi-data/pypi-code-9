# coding: utf-8


__author__ = 'vadim'


# Extension presets

#: This just contains plain text files (.txt).
TEXT = ('txt',)

#: This contains various office document formats (.rtf, .odf, .ods, .gnumeric,
#: .abw, .doc, .docx, .xls, and .xlsx). Note that the macro-enabled versions
#: of Microsoft Office 2007 files are not included.
DOCUMENTS = tuple('pdf rtf odf ods gnumeric abw doc docx xls xlsx'.split())

#: This contains basic image types that are viewable from most browsers (.jpg,
#: .jpe, .jpeg, .png, .gif, .svg, and .bmp).
IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())

#: This contains audio file types (.wav, .mp3, .aac, .ogg, .oga, and .flac).
AUDIO = tuple('wav mp3 aac ogg oga flac'.split())

#: This is for structured data files (.csv, .ini, .json, .plist, .xml, .yaml,
#: and .yml).
DATA = tuple('csv ini json plist xml yaml yml'.split())

#: This contains various types of scripts (.js, .php, .pl, .py .rb, and .sh).
#: If your Web server has PHP installed and set to auto-run, you might want to
#: add ``php`` to the DENY setting.
SCRIPTS = tuple('js php pl py rb sh'.split())

#: This contains archive and compression formats (.gz, .bz2, .zip, .tar,
#: .tgz, .txz, and .7z).
ARCHIVES = tuple('gz bz2 zip tar tgz txz 7z'.split())

#: This contains shared libraries and executable files (.so, .exe and .dll).
#: Most of the time, you will not want to allow this - it's better suited for
#: use with `AllExcept`.
EXECUTABLES = tuple('so exe dll'.split())

#: The default allowed extensions - `TEXT`, `DOCUMENTS`, `DATA`, and `IMAGES`.
DEFAULTS = TEXT + DOCUMENTS + IMAGES + DATA
