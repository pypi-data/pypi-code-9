#!/usr/bin/python
#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
from pylab import *

if __name__ == "__main__":
    koppen_zone = sys.argv[1]
    filename = sys.argv[2]
    print koppen_zone, filename
    with open(filename) as fp:
        data = json.load(fp)
    xlabel("Days")
    ylabel("Rainfall, mm/day")
    plot(range(0, len(data["Channels"]["Rainfall"]["Data"])), data["Channels"]["Rainfall"]["Data"])
    savefig("%s_rainfall.png" % koppen_zone)
    show()

    ###############################################
    if len(data["Channels"]["Rainfall"]["Data"]) > 729:
        xlabel("Days")
        ylabel("Rainfall, mm/day")
        plot(range(0, 730), data["Channels"]["Rainfall"]["Data"][0:730])
        savefig("%s_rainfall_2y.png" % koppen_zone)
        show()

    ##################################################
    xlabel("Days")
    ylabel("Temperature, C")
    plot(range(0, len(data["Channels"]["Rainfall"]["Data"])), data["Channels"]["Air Temperature"]["Data"])
    savefig("%s_temperature.png" % koppen_zone)
    show()

    if len(data["Channels"]["Rainfall"]["Data"]) > 729:
        xlabel("Days")
        ylabel("Temperature, C")
        plot(range(0, 730), data["Channels"]["Air Temperature"]["Data"][0:730])
        savefig("%s_temperature_2y.png" % koppen_zone)
        show()