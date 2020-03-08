import logging

from flask import request, jsonify, Response
from peewee import fn, Alias, SQL, DoesNotExist
from playhouse.shortcuts import model_to_dict
from psycopg2._psycopg import cursor

from app import app
from models import *

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def add_cors(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/api/suggest")
def question():
    query: str = request.args.get('query')
    until = request.args.get('until')
    season = request.args.get('season')
    if not query or not until or not season:
        return "no suggest query", 400
    if len(query) > 50:
        return "too long query", 400
    phrases = Phrase.select(Phrase.text, Alias(fn.SUM(Phrase.count), "total_count")).join(Episode).where(
        (Episode.season == season) &
        (Episode.episode_number <= until) &
        (fn.LOWER(Phrase.text) % ("%" + query.lower() + "%"))
    ).group_by(Phrase.text).order_by(SQL("total_count DESC")).limit(10)
    return jsonify([p.text for p in phrases])


@app.route("/api/search")
def search():
    query = request.args.get('query')
    until = request.args.get('until')
    season = request.args.get('season')
    if not query or not until or not season:
        return "no suggest query", 400
    if len(query) > 50:
        return "too long query", 400

    a = Alias(fn.ts_rank(Line.search_text, fn.plainto_tsquery('english', query)), "rank")

    results = Line.select(Line, Person, Episode, a).where(
        (Line.search_text.match(query, language="english", plain=True))
        &
        (Episode.episode_number <= until)
        &
        (Episode.season == season)
    ).order_by(SQL("rank DESC")).join(Person).switch(Line).join(Episode).limit(20)

    if len(results) == 0:
        result: cursor = db.execute_sql("select plainto_tsquery('english',%s)", [query])
        parsed = result.fetchone()[0]
        if not parsed:
            return jsonify({"status": "warning", "message": "Only stop words were used"})
        else:
            resp: Response = jsonify({"status": "warning", "message": f"No results were found for \"{parsed}\""})
            resp.status_code = 404
            return resp

    data = []
    d: Line
    ri = 0
    for d in results:
        entry = model_to_dict(d, extra_attrs=["rank"], exclude=[Line.search_text])
        entry["rank"] = float(entry["rank"])
        data.append({"centerID": d.id, "resultID": ri, "offset": 1, "lines": [entry]})
        ri += 1

    return jsonify(data)


@app.route("/api/expand")
def expand():
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
        entry = model_to_dict(l, exclude=[Line.search_text])
        data.append(entry)

    return jsonify(data)


if __name__ == "__main__":
    app.debug = True
    app.after_request(add_cors)
    app.run()
