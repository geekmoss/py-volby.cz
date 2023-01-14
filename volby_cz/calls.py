from .ElectionsEnum import ChamberOfDeputiesElectionEnum, PresidentElectionEnum
from .models import Ps, President
from xml.etree import cElementTree
from typing import Union
import requests


def get_chamber_of_deputies_election_results(elections: Union[ChamberOfDeputiesElectionEnum, str], timeout: int = 10)\
        -> Ps:
    res = requests.get(f'https://volby.cz/pls/{elections}/vysledky', headers={'User-Agent': 'py-volby.cz'},
                       timeout=timeout)
    res.raise_for_status()

    return Ps.from_xml_node(cElementTree.fromstring(res.content))


def get_president_election_results(elections: Union[PresidentElectionEnum, str], timeout: int = 10) -> President:
    res = requests.get(f'https://www.volby.cz/pls/{elections}/vysledky', headers={'User-Agent': 'py-volby.cz'},
                       timeout=timeout)
    res.raise_for_status()

    return President.from_xml_node(cElementTree.fromstring(res.content))
