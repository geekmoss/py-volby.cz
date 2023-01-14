from xml.etree.cElementTree import Element
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ElectedStatus(Enum):
    ELECTED = 'ZVOLEN'
    NOT_ELECTED = 'NEZVOLEN'
    SECOND_ROUND = '2.KOLO'




@dataclass
class Candidate:  # NODE - KANDIDAT
    ordinal_number: int  # Attr - PORADOVE_CISLO
    name: str  # Attr - JMENO
    surname: str  # Attr - PRIJMENI
    prefix: str  # Attr - TITULPRED
    suffix: str  # Attr - TITULZA
    first_round_vote_count: int  # Attr - HLASY_1KOLO
    first_round_vote_percent: float  # Attr - HLASY_PROC_1KOLO
    first_round_elected: Optional[ElectedStatus]  # Attr - ZVOLEN_1KOLO
    second_round_vote_count: Optional[int] = None  # Attr - HLASY_2KOLO
    second_round_vote_percent: Optional[float] = None  # Attr - HLASY_PROC_2KOLO
    second_round_elected: Optional[ElectedStatus] = None  # Attr - ZVOLEN_2KOLO


    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        first_round_elected = xml_node.attrib.get('ZVOLEN_1KOLO')
        candidate = Candidate(
            ordinal_number=int(xml_node.attrib.get('PORADOVE_CISLO')),
            name=xml_node.attrib.get('JMENO'),
            surname=xml_node.attrib.get('PRIJMENI'),
            prefix=xml_node.attrib.get('TITULPRED'),
            suffix=xml_node.attrib.get('TITULZA'),
            first_round_vote_count=int(xml_node.attrib.get('HLASY_1KOLO')),
            first_round_vote_percent=float(xml_node.attrib.get('HLASY_PROC_1KOLO')),
            first_round_elected=ElectedStatus(first_round_elected) if first_round_elected is not None else None,
        )

        if candidate.first_round_elected == ElectedStatus.SECOND_ROUND:
            candidate.second_round_vote_count = int(xml_node.attrib.get('HLASY_2KOLO'))
            candidate.second_round_vote_percent = float(xml_node.attrib.get('HLASY_PROC_2KOLO'))
            candidate.second_round_elected = ElectedStatus(xml_node.attrib.get('ZVOLEN_2KOLO'))

        return candidate
    pass

@dataclass
class VoterTurnout:  # Node - UCAST
    round: int  # Attr - KOLO
    election_district_count: int  # Attr - OKRSKY_CELKEM
    election_district_done_count: int  # Attr - OKRSKY_ZPRAC
    election_district_done_percent: float  # Attr - OKRSKY_ZPRAC_PROC
    registered_voters: int  # Attr - ZAPSANI_VOLICI
    issued_envelopes: int  # Attr - VYDANE_OBALKY
    voter_turnout_percent: float  # Attr - UCAST_PROC
    cast_vote_count: int  # Attr - ODEVZDANE_OBALKY
    valid_vote_count: int  # Attr - PLATNE_HLASY
    valid_vote_percent: float  # Attr - PLATNE_HLASY_PROC

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        voter_turnout = VoterTurnout(
            round=int(xml_node.attrib.get('KOLO')),
            election_district_count=int(xml_node.attrib.get('OKRSKY_CELKEM')),
            election_district_done_count=int(xml_node.attrib.get('OKRSKY_ZPRAC')),
            election_district_done_percent=float(xml_node.attrib.get('OKRSKY_ZPRAC_PROC')),
            registered_voters=int(xml_node.attrib.get('ZAPSANI_VOLICI')),
            issued_envelopes=int(xml_node.attrib.get('VYDANE_OBALKY')),
            voter_turnout_percent=float(xml_node.attrib.get('UCAST_PROC')),
            cast_vote_count=int(xml_node.attrib.get('ODEVZDANE_OBALKY')),
            valid_vote_count=int(xml_node.attrib.get('PLATNE_HLASY')),
            valid_vote_percent=float(xml_node.attrib.get('PLATNE_HLASY_PROC')),
        )
        return voter_turnout
    pass


@dataclass
class CzechRepublic:  # Node - CR
    voter_turnout_first_round: VoterTurnout  # Node - UCAST[kolo=1]
    voter_turnout_second_round: Optional[VoterTurnout]  # Node - UCAST[kolo=2]
    candidates: List[Candidate]  # Nodes - Kandidat

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        vt_first_round = xml_node.find(f'{namespace}UCAST[@KOLO="1"]')
        vt_second_round = xml_node.find(f'{namespace}UCAST[@KOLO="2"]')

        candidates = xml_node.iter(f'{namespace}KANDIDAT')

        return CzechRepublic(
            VoterTurnout.from_xml_node(vt_first_round, namespace),
            VoterTurnout.from_xml_node(vt_second_round, namespace) if vt_second_round is not None else None,
            [Candidate.from_xml_node(c, namespace) for c in candidates],
        )
    pass


@dataclass
class Results:
    cr: CzechRepublic  # Node - CR

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        print(f'Results -> {xml_node}')
        cr = xml_node.find(f'{namespace}CR')
        return Results(
            CzechRepublic.from_xml_node(cr, namespace),
        )
    pass


@dataclass
class President:
    generated: datetime  # Attribute - DATUM_CAS_GENEROVANI
    results: Results  # Node - VYSLEDKY

    @staticmethod
    def from_xml_node(xml_node: Element, namespace='{http://www.volby.cz/prezident/}'):
        ps = President(
            datetime.strptime(xml_node.attrib.get('DATUM_CAS_GENEROVANI'), '%Y-%m-%dT%H:%M:%S'),
            Results.from_xml_node(xml_node, namespace)
        )
        return ps
    pass
