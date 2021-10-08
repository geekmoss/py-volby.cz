from xml.etree.cElementTree import Element
from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class VoterTurnout:  # Node - UCAST
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
class Deputy:  # Node - POSLANEC
    region_number: int  # Attr - CIS_KRAJ
    ordinal_number: int  # Attr - PORADOVE_CISLO
    name: str  # Attr - JMENO
    surname: str  # Attr - PRIJMENI
    prefix: str  # Attr - TITULPRED
    suffix: str  # Attr - TITULZA
    prefer_vote_count: int  # Attr - PREDNOSTNI_HLASY
    prefer_vote_percent: float  # Attr - PREDNOSTNI_HLASY

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        deputy = Deputy(
            region_number=int(xml_node.attrib.get('CIS_KRAJ')),
            ordinal_number=int(xml_node.attrib.get('PORADOVE_CISLO')),
            name=xml_node.attrib.get('JMENO'),
            surname=xml_node.attrib.get('PRIJMENI'),
            prefix=xml_node.attrib.get('TITULPRED'),
            suffix=xml_node.attrib.get('TITULZA'),
            prefer_vote_count=int(xml_node.attrib.get('PREDNOSTNI_HLASY')),
            prefer_vote_percent=float(xml_node.attrib.get('PREDNOSTNI_HLASY')),
        )
        return deputy
    pass


@dataclass
class PartyResult:  # Node - HODNOTY_STRANA
    vote_count: int  # Attr - HLASY
    vote_percent: float  # Attr - PROC_HLASU
    mandate_count: int  # Attr - MANDATY
    mandate_percent: float  # Attr - PROC_MANDATU

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        if xml_node is None:
            return PartyResult(0, 0, 0, 0)

        party_result = PartyResult(
            vote_count=int(xml_node.attrib.get('HLASY')),
            vote_percent=float(xml_node.attrib.get('PROC_HLASU')),
            mandate_count=int(xml_node.attrib.get('MANDATY', 0)),
            mandate_percent=float(xml_node.attrib.get('PROC_MANDATU', 0)),
        )
        return party_result
    pass


@dataclass
class Party:  # Node - STRANA
    k_party: int  # Attr - KSTRANA
    party_name: str  # Attr - NAZ_STR
    party_result: PartyResult  # Node - HODNOTY_STRANA
    deputies: List[Deputy]  # Nodes - POSLANEC

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        party_result_node = xml_node.find(f'{namespace}HODNOTY_STRANA')
        deputy_nodes = xml_node.iter(f'{namespace}POSLANEC')

        party = Party(
            k_party=int(xml_node.attrib.get('KSTRANA')),
            party_name=xml_node.attrib.get('NAZ_STR'),
            party_result=PartyResult.from_xml_node(party_result_node, namespace),
            deputies=[Deputy.from_xml_node(d, namespace) for d in deputy_nodes],
        )
        return party
    pass


@dataclass
class CzechRepublic:  # Node - CR
    voter_turnout: VoterTurnout  # Node - UCAST
    parties: List[Party]  # Nodes - STRANA

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        voter_turnout_node = xml_node.find(f'{namespace}UCAST')
        party_nodes = xml_node.iter(f'{namespace}STRANA')

        cr = CzechRepublic(
            VoterTurnout.from_xml_node(voter_turnout_node, namespace),
            [Party.from_xml_node(p, namespace) for p in party_nodes]
        )
        return cr
    pass


@dataclass
class Region:
    region_number: int  # Attr - CIS_KRAJ
    region_name: str  # Attr - NAZ_KRAJ
    total_mandate_count: int  # Attr - POCMANDATU
    voter_turnout: VoterTurnout  # Node - UCAST
    parties: List[Party]  # Nodes - STRANA

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        voter_turnout = xml_node.find(f'{namespace}UCAST')
        parties = xml_node.iter(f'{namespace}STRANA')
        region = Region(
            region_number=int(xml_node.attrib.get('CIS_KRAJ')),
            region_name=xml_node.attrib.get('NAZ_KRAJ'),
            total_mandate_count=int(xml_node.attrib.get('POCMANDATU', 0)),
            voter_turnout=VoterTurnout.from_xml_node(voter_turnout, xml_node),
            parties=[Party.from_xml_node(p, xml_node) for p in parties],
        )
        return region
    pass


@dataclass
class Results:
    regions: List[Region]  # Nodes - KRAJE
    cr: CzechRepublic  # Node - CR

    @staticmethod
    def from_xml_node(xml_node: Element, namespace):
        regions = xml_node.iter(f'{namespace}KRAJ')
        cr = xml_node.find(f'{namespace}CR')
        return Results(
            [Region.from_xml_node(r, namespace) for r in regions],
            CzechRepublic.from_xml_node(cr, namespace),
        )
    pass


@dataclass
class Ps:
    generated: datetime  # Attribute - DATUM_CAS_GENEROVANI
    results: Results  # Node - VYSLEDKY

    @staticmethod
    def from_xml_node(xml_node: Element, namespace='{http://www.volby.cz/ps/}'):
        ps = Ps(
            datetime.strptime(xml_node.attrib.get('DATUM_CAS_GENEROVANI'), '%Y-%m-%dT%H:%M:%S'),
            Results.from_xml_node(xml_node, namespace),
        )

        return ps
    pass
