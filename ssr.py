"""
do some kind of pseudo SSR, modifying the index.html to contain metadata
"""
import textwrap
from io import BytesIO
from textwrap import shorten
from urllib.parse import unquote

from PIL import Image, ImageFont, ImageDraw
from flask import Blueprint, redirect, render_template, abort, request, send_file
from playhouse.flask_utils import get_object_or_404

from app import cache
from data import series_data_by_slug
from models import Episode, Series

ssr_routes = Blueprint("ssr_routes", __name__, template_folder="templates")

with open("./web/dist/index.html") as f:
    index_html = f.read()

placeholder_token = '<title>CR Search</title>'


def draw_image(text: str, description: str, subtitle=None) -> BytesIO:
    text = text.replace("| CR Search", "").strip()
    text = shorten(text, 25, placeholder=" ...")
    if subtitle:
        text += "\n" + subtitle
    width, height = (1200, 600)
    img = Image.open("./web/src/assets/background_small.png")

    mr_eves = ImageFont.truetype("web/fonts/Mr Eaves/Mr Eaves Small Caps.otf", 50)
    title_font = ImageFont.truetype("web/fonts/Nodesto Caps Condensed/Nodesto Caps Condensed.otf", 120)
    small_font = ImageFont.truetype("web/fonts/Scaly Sans/Scaly Sans.otf", 30)
    draw = ImageDraw.Draw(img)
    w, h = draw.multiline_textsize(text, title_font)

    draw.multiline_text(((width - w) / 2, (height - h) / 4), text,
                        font=title_font, align="center",
                        fill="#58180d")
    description = textwrap.fill(description, 50)
    w, h = draw.multiline_textsize(description, mr_eves)
    draw.multiline_text(((width - w) / 2, (height - h) / 3 * 2), description,
                        font=mr_eves, align="center",
                        fill="black")
    footer_text = "Critical Role Search"
    w, h = draw.multiline_textsize(footer_text, small_font)
    draw.multiline_text(((width - w - 10), (height - h - 10)), footer_text,
                        font=small_font, align="center",
                        fill="black")
    url = request.url.split("?")[0]
    url = unquote(url)
    if len(url) > 50:
        url = "/".join(url.split("/")[:-1])
    w, h = draw.multiline_textsize(url, small_font)
    draw.multiline_text((10, (height - h - 10)), url,
                        font=small_font, align="center",
                        fill="black")

    byte_io = BytesIO()
    img.save(byte_io, "PNG", optimize=True)
    byte_io.seek(0)
    return byte_io


@ssr_routes.route("/", defaults={'something': None})
@ssr_routes.route("/<string:something>/")
def home_redirect(something):
    return redirect("/campaign3/10/")


@ssr_routes.route("/episodes")
@cache.cached(timeout=60 * 60 * 24 * 30, query_string=True)
def episodes():
    num = Episode.select().count()
    description = f"Overview over {num} imported episodes of Critical Role"
    title = "Episode Overview | CR Search"
    if request.args.get("image", None) == "true":
        return send_file(draw_image(title, description), mimetype="image/png")

    additional_html = render_template(
        "header.html",
        description=description,
        title=title,
        url=request.url
    )
    return index_html.replace(placeholder_token, additional_html)


@ssr_routes.route("/transcript/<string:series>/<string:episode_number>/")
@cache.cached(timeout=60 * 60 * 24 * 30, query_string=True)
def transcript(series, episode_number):
    episode = get_object_or_404(Episode.select(Episode, Series).where(
        (Episode.episode_number == episode_number)
        &
        (Episode.series.slug == series)
    ).join(Series))
    description = f"Browse through the transcript of episode {episode_number} of {episode.series.title} (“{episode.pretty_title}”)"
    title = f"{episode.pretty_title} | Transcript | CR Search"
    if request.args.get("image", None) == "true":
        return send_file(draw_image(episode.pretty_title, description, subtitle="Transcript"), mimetype="image/png")

    additional_html = render_template(
        "header.html",
        description=description,
        title=title,
        url=request.url
    )
    return index_html.replace(placeholder_token, additional_html)


@ssr_routes.route("/<string:series_slug>/<string:episodes>/<string:keyword>")
@ssr_routes.route("/<string:series_slug>/<string:episodes>", defaults={'keyword': None})
@ssr_routes.route("/<string:series_slug>/<string:episodes>/", defaults={'keyword': None})
@cache.cached(timeout=60 * 60 * 24 * 30, query_string=True)
def search(series_slug, episodes, keyword):
    one_shot = Episode.select(Episode, Series).where(
        Episode.series.slug == series_slug
    ).join(Series).count() == 1
    try:
        series = series_data_by_slug[series_slug]
    except KeyError:
        return abort(404)
    if keyword:
        if one_shot:
            description = f"Search for “{keyword}” in {series.name}"
        else:
            description = f"Search for “{keyword}” up to episode {episodes} of {series.name}"
        title = f"{keyword} | CR Search"
    else:
        description = f"Search through {series.name} of Critical Role"
        title = f"{series.name} | CR Search"
    if request.args.get("image", None) == "true":
        return send_file(draw_image(title, description), mimetype="image/png")
    additional_html = render_template(
        "header.html",
        description=description,
        title=title,
        url=request.url
    )
    print(additional_html)
    return index_html.replace(placeholder_token, additional_html)
