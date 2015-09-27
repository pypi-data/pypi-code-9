import re
sub = re.sub

try: # python3
    from io import StringIO
except ImportError: # python2
    from StringIO import StringIO

def format_df_string(df_string):

    df_string = sub(" +", "\t", sub("^ +", "", df_string, flags=re.MULTILINE))

    return df_string
