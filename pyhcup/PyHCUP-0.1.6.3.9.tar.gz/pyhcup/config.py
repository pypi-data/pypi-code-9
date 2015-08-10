import os
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, BigInteger, String, Numeric

dir_here = os.path.dirname(os.path.abspath(__file__))
BUNDLED_LOADFILE_DIR = os.path.join(dir_here, 'data', 'loadfiles')
BUNDLED_SID_SAMPLES_DIR = os.path.join(dir_here, 'data', 'sid_samples')
BUNDLED_UFLAGDEF = os.path.join(dir_here, 'data', 'uflags', 'uflag_definitions.csv')

DEFAULT_DATA_SOURCES = [
    {
    'name': 'HCUP',
    'description': 'Healthcare Cost and Utilization Project',
    'content': 'contentnh_uncompressed', #this can be omitted
    'patterns': [
        '(?P<state_abbr>[A-Z]{2})_(?P<file>[A-Z]+)_(?P<year>[0-9]{4})_(?P<category>[A-Z_]+)\.(?P<file_extension>asc)',
        ]
    },
    {
    'name': 'HCUP',
    'description': 'Healthcare Cost and Utilization Project',
    'content': 'contentnh_zipcompressed',
    'patterns': [
        '(?P<state_abbr>[A-Z]{2})_(?P<file>[A-Z]+)_(?P<year>[0-9]{4})_(?P<category>[A-Z_]+)\.(?P<file_extension>exe|zip)',
        ]
    },
    {
    'name': 'HCUP',
    'description': 'Healthcare Cost and Utilization Project',
    'content': 'load_uncompressed',
    'patterns': [
        '(?P<state_abbr>[A-Z]{2})_(?P<file>[A-Z]+)_(?P<year>[0-9]{4})_(?P<category>[A-Z_]+)\.(?P<file_extension>sas)',
        ],
    },
    {
    'name': 'HCUP',
    'description': 'Healthcare Cost and Utilization Project',
    'content': 'contenth_uncompresed',
    'patterns': [
        '(?P<state_abbr>[A-Z]{2})_(?P<year>[0-9]{4})_(?P<category>daystoevent)\.(?P<file_extension>csv)',
        ],
    },
    {
    'name': 'PUDF',
    'description': 'Texas Inpatient Public Use Data File',
    'content': 'load_uncompressed',
    'patterns': [
        '(?P<state_abbr>tx)_(?P<file>pudf)_(?P<year>[0-9]{4})_(?P<category>base|charges|facility)_definition\.(?P<file_extension>txt)',
        ],
    },
    ]


# Some files have bonus content, which should be skipped for loading
SKIP_ROWS = {
        ('SID', 'AR', 2010, 'AHAL'): 2,
        ('SID', 'AR', 2010, 'CHGS'): 2,
        ('SID', 'AR', 2010, 'CORE'): 2,
        ('SID', 'AR', 2010, 'DX_PR_GRPS'): 2,
        ('SID', 'AR', 2010, 'SEVERITY'): 2,
        ('SID', 'AR', 2011, 'AHAL'): 2,
        ('SID', 'AR', 2011, 'CHGS'): 2,
        ('SID', 'AR', 2011, 'CORE'): 2,
        ('SID', 'AR', 2011, 'DX_PR_GRPS'): 2,
        ('SID', 'AR', 2011, 'SEVERITY'): 2,
        ('SID', 'AR', 2012, 'AHAL'): 2,
        ('SID', 'AR', 2012, 'CHGS'): 2,
        ('SID', 'AR', 2012, 'CORE'): 2,
        ('SID', 'AR', 2012, 'DX_PR_GRPS'): 2,
        ('SID', 'AR', 2012, 'SEVERITY'): 2,
        ('SID', 'AZ', 2012, 'AHAL'): 2,
        ('SID', 'CO', 2012, 'AHAL'): 2,
        ('SID', 'FL', 2012, 'AHAL'): 2,
        ('SID', 'KY', 2012, 'AHAL'): 2,
        ('SID', 'IA', 2012, 'AHAL'): 2,
        ('SID', 'IA', 2012, 'CORE'): 2,
        ('SID', 'IA', 2012, 'DX_PR_GRPS'): 2,
        ('SID', 'IA', 2012, 'SEVERITY'): 2,
        ('SID', 'MA', 2012, 'AHAL'): 2,
        ('SID', 'MD', 2012, 'AHAL'): 2,
        ('SID', 'NC', 2012, 'AHAL'): 2,
        ('SID', 'NC', 2012, 'CHGS'): 2,
        ('SID', 'NC', 2012, 'CORE'): 2,
        ('SID', 'NC', 2012, 'DX_PR_GRPS'): 2,
        ('SID', 'NC', 2012, 'SEVERITY'): 2,
        ('SID', 'NJ', 2012, 'AHAL'): 2,
        ('SID', 'NV', 2012, 'AHAL'): 2,
        ('SID', 'NY', 2012, 'AHAL'): 2,
        ('SID', 'OR', 2012, 'AHAL'): 2,
        ('SID', 'RI', 2012, 'AHAL'): 2,
        ('SID', 'VT', 2012, 'AHAL'): 2,
        ('SID', 'WA', 2012, 'AHAL'): 2,
        ('SID', 'WI', 2012, 'AHAL'): 2,
        ('SID', 'WV', 2012, 'AHAL'): 2,
    }


# these loading programs are simply not available, even from HCUP
KNOWN_MISSING_LOADFILES = [
    {'state_abbr': 'RI', 'year': '2009', 'category': 'AHAL', 'file': 'SID'}
    ]


# definitions for replacing missing values down the line
MISSING_PATTERNS = {
        #'missing':        '-9*\.?9*[^-\.]| |\.',
        #'invalid':        '-8*\.?8*[^-\.]|A',
        #'unavailable':    '-7*\.?7*[^-\.]',
        #'inconsistent':   '-6*\.?6*[^-\.]',
        #'notapplicable':  '-5*\.?5*[^-\.]',
        'missing':        '-9*\.?9*',
        'invalid':        '-8*\.?8*',
        'unavailable':    '-7*\.?7*',
        'inconsistent':   '-6*\.?6*',
        'notapplicable':  '-5*\.?5*',
        'tx_cell_too_sm': '-?999+8',
        'tx_invalid':     '\*',
        'tx_missing':     '\.|`',
        }


# long table definitions (static)
# tuples; convert to SQLAlchemy objects as Column(*tuple)
LONG_TABLE_BASE_COLUMNS = [
        ('KEY', BigInteger()),
        ('VISITLINK', BigInteger()),
        ('DAYSTOEVENT', BigInteger()),
        ('YEAR', Integer()),
        ('STATE', String(2))
    ]

LONG_TABLE_COLUMNS = {
    'CHGS': LONG_TABLE_BASE_COLUMNS + [
        ('UNITS', Numeric(precision=11, scale=2)),
        ('REVCODE', String(4)),
        ('RATE', Numeric(precision=9, scale=2)),
        ('CHARGE', Numeric(precision=12, scale=2)),
        ('CPTHCPCS', String(5)),
        ('CPTMOD1', String(2)),
        ('CPTMOD2', String(2)),
        ('GROUP_NUMBER', Integer())
        ],
    'DX': LONG_TABLE_BASE_COLUMNS + [
        ('DX', String(10)),
        ('DXV', String(2)),
        ('DXCCS', String(5)),
        ('DXPOA', String(1)),
        ('DXatAdmit', String(1)),
        ('TMDX', String(1)),
        ('GROUP_NUMBER', Integer())
        ],
    'PR': LONG_TABLE_BASE_COLUMNS + [
        ('PR', String(10)),
        ('PRCCS', String(5)),
        ('PRDATE', String(6)),
        ('PRDAY', String(2)),
        ('PRMONTH', String(2)),
        ('PRYEAR', String(4)),
        ('PRV', String(2)),
        ('PRCLASS', String(1)),
        ('PRMCCS', String(8)),
        ('GROUP_NUMBER', Integer()),
        ],
    'UFLAGS': LONG_TABLE_BASE_COLUMNS + [
        ('NAME', String(50)),
        ('VALUE', Integer())
        ]
    }
