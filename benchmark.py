import json
import shutil
from statistics import mean, stdev
from typing import Tuple

from alive_progress import alive_bar
from peewee import SelectQuery
from psycopg2._psycopg import cursor

from models import db
from server import search, suggest


def benchmark_query(query: SelectQuery, filename: str = None) -> Tuple[float, float]:
    query, params = test_search.sql()

    query = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON) " + query

    cur: cursor = db.execute_sql(query, params=params)

    result = cur.fetchone()[0][0]
    if filename:
        with open(f"benchmark/{filename}.json", "w") as f:
            json.dump(result, f, indent=2)
        with open(f"benchmark/{filename}.txt", "w") as f:
            f.write(query)

    return result["Planning Time"], result["Execution Time"]


def statistics(query: SelectQuery, filename: str, repeats: int = 500):
    ts = shutil.get_terminal_size((80, 20))
    print(filename.center(ts.columns, "-"))
    planning_times = []
    execution_times = []
    benchmark_query(query, filename=filename)

    with alive_bar(repeats) as bar:
        for i in range(repeats):
            plantime, exetime = benchmark_query(query)
            planning_times.append(plantime)
            execution_times.append(exetime)
            bar()
    print(mean(planning_times), stdev(planning_times))
    print(mean(execution_times), stdev(execution_times))


test_search = search("hello", 1000, 1, 200)
statistics(test_search, filename="search_hello")
test_search = search("a very long search query with a lot of stop word", 1000, 1, 200)
statistics(test_search, filename="search_long")

test_search = suggest("gnoll", 1000, 1)
statistics(test_search, filename="suggest_simple")
test_search = suggest("gu", 1000, 1)
statistics(test_search, filename="suggest_two_letter", repeats=100)
