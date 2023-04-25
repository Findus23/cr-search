from abc import ABC, abstractmethod
from typing import List, Dict, Any

from prettytable import PrettyTable
from psycopg2._psycopg import cursor

from app import db


class Stats(ABC):
    query: str

    def execute(self) -> cursor:
        return db.execute_sql(self.query)

    @abstractmethod
    def as_data(self):
        ...

    def as_plaintext(self) -> str:
        cur = self.execute()
        x = PrettyTable()
        x.add_rows(cur.fetchall())
        x.field_names = [d.name for d in cur.description]
        return x.get_string()


class MultiColumnStats(Stats):

    def as_data(self) -> list[dict[str, Any]]:
        data = []
        cur = self.execute()
        column_names = [d.name for d in cur.description]
        for row in cur.fetchall():
            single_stat = {}
            for i, value in enumerate(row):
                single_stat[column_names[i]] = value
            data.append(single_stat)
        return data


class SingleValueStats(Stats):

    def as_data(self) -> int:
        result = self.execute().fetchone()
        return result[-1]


class LinesPerPerson(MultiColumnStats):
    query = """
select name, count(name) as count, sum(length(text)) as count_chars
from line
         join person p on line.person_id = p.id
group by name
order by count_chars desc;
"""


class MostCommonNounChunks(MultiColumnStats):
    query = """
select text, sum(count) as num_occurrence
from phrase
group by text
order by num_occurrence desc
limit 1000;
"""


class LongestNounChunks(MultiColumnStats):
    query = """
select text, char_length(phrase.text) as length
from phrase
order by length desc
limit 100;
;
"""


class TotalWords(SingleValueStats):
    query = """
select sum(array_length(regexp_split_to_array(text,'\\s'),1)) from line
"""


class TotalLines(SingleValueStats):
    query = """
select count(1) from line
"""


class TotalPhrases(SingleValueStats):
    query = """
select count(1) from phrase
"""


class PhraseTableSize(SingleValueStats):
    query = "SELECT pg_size_pretty(pg_relation_size('phrase')) as size;"


class LineTableSize(SingleValueStats):
    query = "SELECT pg_size_pretty(pg_relation_size('line')) as size;"


class TotalVideoTime(SingleValueStats):
    query = """select (sum(endtime)::float / 1000/60/60) as hours
from (select distinct on (episode_id) endtime from line order by episode_id, "order" desc) as subquery  
"""


def aggregate_stats(plaintext: bool):
    text = ""
    data = {}
    for stats_class in [TotalLines, TotalWords, TotalPhrases, PhraseTableSize, LineTableSize, TotalVideoTime,
                        MostCommonNounChunks,
                        LongestNounChunks, LinesPerPerson]:
        name = type(stats_class()).__name__
        if plaintext:
            text += f" {name} ".center(80, "#") + "\n"
            text += stats_class().as_plaintext() + "\n\n"
        else:
            data[name] = stats_class().as_data()
    if plaintext:
        return text
    else:
        return data
