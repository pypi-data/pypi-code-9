bind = 'unix://${prefix}/var/run/adagucserver.socket'
workers = 3

# environment
raw_env = [
    "ADAGUC_CONFIG=${prefix}/etc/adagucserver/autowms.xml",
    "ADAGUC_LOGFILE=${prefix}/var/log/adaguc.log",
    "ADAGUC_ERRORFILE=${prefix}/var/log/adaguc.log",
    "ADAGUC_DATARESTRICTION=ALLOW_WCS|ALLOW_GFI|ALLOW_METADATA|SHOW_QUERYINFO",
    "PATH=${prefix}/bin:/usr/bin:/bin:/usr/local/bin",
    "GDAL_DATA=${prefix}/share/gdal",
    ]                                                                                                              

# logging
errorlog = '-'
accesslog = '-'
