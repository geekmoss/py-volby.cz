from .ElectionsEnum import ChamberOfDeputiesElectionEnum
from .models.PS import Ps
from xml.etree import cElementTree
from typing import Union
import requests


def get_chamber_of_deputies_election_results(elections: Union[ChamberOfDeputiesElectionEnum, str]) -> Ps:
    res = requests.get(f'https://volby.cz/pls/{elections}/vysledky', headers={'User-Agent': 'py-volby.cz'})
    res.raise_for_status()

    return Ps.from_xml_node(cElementTree.fromstring(res.content))
