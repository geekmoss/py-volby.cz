import enum


class ChamberOfDeputiesElectionEnum(enum.Enum):
    year_2021 = 'ps2021'
    year_2017_by_court = 'ps2017nss'
    year_2017 = 'ps2017'

    def __str__(self):
        return self.value


class PresidentElectionEnum(enum.Enum):
    year_2013 = 'prez2013'
    year_2018 = 'prez2018'
    year_2023 = 'prez2023'

    def __str__(self):
        return self.value
