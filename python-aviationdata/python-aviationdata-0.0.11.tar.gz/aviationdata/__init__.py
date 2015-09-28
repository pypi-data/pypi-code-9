# coding: latin-1
from blocks import BlockFactory
from receiver import MetarReceiver, TafReceiver, AirportReceiver, HbAircraftReceiver
from presenter import JsonPresenter, HumanPresenter

def retreiveReport(airport=None):
    data = []
    r = AirportReceiver(airport)
    airports = r.receive()
    for airport in airports:
        detail_data = {'airport': airport, 'reports': []}
        reports = []
        metar = MetarReceiver(airport['icao'])
        reports += metar.receive()
        taf = TafReceiver(airport['icao'])
        reports += taf.receive()

        for report in reports:
            f = BlockFactory(report)
            detail_data['reports'].append(f.parse())

        data.append(detail_data)
    return data

if __name__ == "__main__":
    print HumanPresenter(retreiveReport('LSZI'))
