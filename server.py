import random
from typing import List

from flask import request, jsonify, Response, abort
from peewee import fn, Alias, SQL, DoesNotExist, Expression, ModelSelect, JOIN
from playhouse.postgres_ext import TS_MATCH
from playhouse.shortcuts import model_to_dict
from psycopg2._psycopg import cursor

from app import app, db, cache
from models import *
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)
from stats import TotalWords, MostCommonNounChunks, LongestNounChunks, LinesPerPerson, aggregate_stats
from suggestions import suggestions


def add_cors(response: Response) -> Response:
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


def suggest(query: str, until: int, series: str, limit: int = 10) -> ModelSelect:
    return Phrase.select(Phrase.text, Alias(fn.SUM(Phrase.count), "total_count")).join(Episode).join(Series).where(
        (Episode.series.slug == series) &
        (Episode.episode_number <= until) &
        (Phrase.text.contains(query))
    ).group_by(Phrase.text).order_by(SQL("total_count DESC")).limit(limit)


def search(query: str, until: int, series: str, limit: int = 50) -> ModelSelect:
    a = Alias(fn.ts_rank_cd(Line.search_text, fn.websearch_to_tsquery('english', query), 1 + 4), "rank")

    return Line.select(Line, Person, Episode, Series, a).where(
        Expression(Line.search_text, TS_MATCH, fn.websearch_to_tsquery('english', query))
        &
        (Episode.episode_number <= until)
        &
        (Episode.series.slug == series)
    ).order_by(SQL("rank DESC")) \
        .join(Person, join_type=JOIN.FULL).switch(Line) \
        .join(Episode).join(Series) \
        .limit(limit)


def exact_search(query: str, until: int, series: str, limit: int = 50) -> ModelSelect:
    return Line.select(Line, Person, Episode, Series).where(
        (Episode.episode_number <= until)
        &
        (Episode.series.slug == series)
        &
        (Line.text.contains(query))
    ).order_by(Episode.video_number, Line.order) \
        .join(Person).switch(Line) \
        .join(Episode).join(Series) \
        .limit(limit)


global_excludes = [Line.search_text, Episode.phrases_imported, Episode.text_imported, Person.series, Episode.title]


@app.route("/api/suggest")
def api_question():
    query: str = request.args.get('query')
    until = request.args.get('until')
    if until == "-":
        until = 1000
    series = request.args.get('series')
    if not query or not until or not series:
        return "no suggest query", 400
    if len(query) > 500:
        return "too long query", 400
    cache_key = f"suggest_{until}_{series}_{query}"
    if len(query) < 3:
        result = cache.get(cache_key)
        if result:
            return jsonify(result)
    phrases = suggest(query, until, series)
    result = [p.text for p in phrases]
    if len(query) < 3:
        cache.set(cache_key, result, timeout=60 * 60 * 24 * 7)
    return jsonify(result)


@app.route("/api/search")
def api_search():
    query = request.args.get('query')
    until = request.args.get('until')
    if until == "-":
        until = 1000
    series = request.args.get('series')
    exact = request.args.get('exact', False)
    exact = False  # don't allow exact searches
    if not query or not until or not series:
        return "no search query", 400
    if len(query) > 500:
        return "too long query", 400

    if exact:
        results = exact_search(query, until, series)
    else:
        results = search(query, until, series)

        if len(results) == 0:
            result: cursor = db.execute_sql("select websearch_to_tsquery('english',%s)", [query])
            parsed = result.fetchone()[0]
            if not parsed:
                return jsonify({
                    "status": "warning",
                    "message": "Only stop words were used. Please try to add a less common word to the search."
                })
            else:
                resp: Response = jsonify({"status": "warning", "message": f"No results were found for {parsed}"})
                resp.status_code = 404
                return resp

    data = []
    d: Line
    ri = 0
    for d in results:
        entry = model_to_dict(d, extra_attrs=[] if exact else ["rank"],
                              exclude=global_excludes + [Episode.subtitle_hash])
        if not exact:
            entry["rank"] = float(entry["rank"])
        data.append({"centerID": d.id, "resultID": ri, "offset": 1, "lines": [entry]})
        ri += 1

    return jsonify(data)


@app.route("/api/expand")
def api_expand():
    center_id = request.args.get('centerID')
    offset = int(request.args.get('offset', 1))
    if not center_id:
        return "no central line ID", 400

    try:
        center: Line = Line.select().where(Line.id == center_id).get()

    except DoesNotExist:
        return "not found", 404

    lines = Line.select().where(
        (Line.episode == center.episode) & (Line.order << [center.order - offset, center.order + offset])
    )
    l: Line
    data = []
    for l in lines:
        entry = model_to_dict(l, exclude=global_excludes)
        data.append(entry)

    return jsonify(data)


@app.route("/api/series")
@cache.cached(timeout=60 * 60 * 24)
def series():
    series_list = []
    for series in Series.select().order_by(Series.order):
        last_episode: Episode = Episode.select().where(Episode.series == series).order_by(
            Episode.upload_date.desc()).limit(
            1).get()
        series_data = model_to_dict(series, exclude=[Series.order])
        series_data["last_upload"] = last_episode.upload_date.strftime("%Y-%m-%d")
        series_data["length"] = Episode.select().where(Episode.series == series).count()
        series_list.append(series_data)
    return jsonify({
        "series": series_list
    })


@app.route("/api/episodes")
@cache.cached(timeout=60 * 60 * 24)
def api_episodes():
    all_series: List[Series] = Series.select().order_by(Series.order)
    data = []
    for series in all_series:

        episodes: List[Episode] = Episode.select().where(Episode.series == series).order_by(Episode.video_number)

        series_data = []
        for episode in episodes:
            entry = model_to_dict(episode, exclude=[Episode.series, Episode.title])
            if entry["upload_date"]:
                entry["upload_date"] = entry["upload_date"].strftime("%Y-%m-%d")
            series_data.append(entry)
        data.append({
            "meta": model_to_dict(series),
            "episodes": series_data
        })

    return jsonify(data)


@app.route("/api/suggestion")
def api_suggestion():
    until = request.args.get('until')
    series = request.args.get('series')
    if series not in suggestions:
        abort(404)
    all_suggestions = suggestions[series]
    if until == "-":
        possible_suggestions = [s.text for s in all_suggestions]
    else:
        possible_suggestions = [s.text for s in all_suggestions if s.episode <= int(until)]
    chosen_suggestion = random.choice(possible_suggestions)
    return Response(chosen_suggestion, mimetype='text/plain')


@app.route("/api/transcript")
@cache.cached(timeout=60 * 60 * 24)
def transcript():
    series = request.args.get('series')
    episode_number = request.args.get('episode')

    episode = Episode.select(Episode, Series).where(
        (Episode.episode_number == episode_number)
        &
        (Episode.series.slug == series)
    ).join(Series).get()

    lines: List[Line] = Line.select(Line, Person).where(
        (Episode.episode_number == episode_number)
        &
        (Episode.series.slug == series)
    ).order_by(Line.order) \
        .join(Person, join_type=JOIN.FULL).switch(Line) \
        .join(Episode).join(Series)

    line_data = []
    for line in lines:
        entry = model_to_dict(line, exclude=global_excludes + [Line.episode])

        line_data.append(entry)

    return jsonify({
        "episode": model_to_dict(episode, exclude=global_excludes),
        "lines": line_data
    })


@app.route("/api/stats")
@cache.cached(timeout=60 * 60 * 24)
def stats():
    return jsonify(aggregate_stats(plaintext=False))


@app.route("/api/stats/text")
@cache.cached(timeout=60 * 60 * 24)
def stats_text():
    return Response(aggregate_stats(plaintext=True), mimetype='text/plain')


if __name__ == "__main__":
    import logging

    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    app.debug = True
    app.after_request(add_cors)
    app.run()
