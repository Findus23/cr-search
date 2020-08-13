import os

import spacy as spacy
from alive_progress import alive_bar
from peewee import chunked
from spacy.lang.en import English
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from models import Episode, Line, db, Phrase
from stopwords import STOP_WORDS

os.nice(15)

nlp: English = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
nlp.Defaults.stop_words = STOP_WORDS
for episode in Episode.select().where((Episode.phrases_imported == False) & (Episode.text_imported == True)).order_by(
        Episode.id):
    print(episode.video_number, episode.title)
    person = None
    text = ""
    line_select = Line.select().where(Line.episode == episode)
    with alive_bar(line_select.count(), title='Parsing lines') as bar:
        for line in Line.select().where(Line.episode == episode).order_by(Line.order):
            bar()
            if line.person == person:
                text += " " + line.text
            else:
                person = line.person
                text += "\n" + line.text

    delete = ["\"", "--", "(", ")", "[", "]"]
    for string in delete:
        text = text.replace(string, "")
    print("run nlp")
    doc = nlp(text)
    print("nlp finished")
    nouns = {}
    chunk: Span
    noun_chunks=list(doc.noun_chunks)
    with alive_bar(len(noun_chunks), title='lemmatizing and counting') as bar:
        for chunk in noun_chunks:
            bar()
            tok: Token
            noun_chunk = "".join([tok.text_with_ws for tok in chunk if not tok.is_stop]).strip()
            lemmas = "|".join([token.lemma_ for token in nlp(noun_chunk)])
            if lemmas not in nouns:
                nouns[lemmas] = {
                    "count": 1,
                    "name": noun_chunk
                }
            else:
                nouns[lemmas]["count"] += 1
    with db.atomic():
        phrases = []
        for lemmas, data in nouns.items():
            phrase = data["name"]
            count = data["count"]
            if "\n" in phrase:
                continue
            if len(phrase) < 4:
                continue
            phrases.append(Phrase(text=phrase, count=count, episode=episode))

        num_per_chunk = 100
        chunks = chunked(phrases, num_per_chunk)
        with alive_bar(len(phrases) // num_per_chunk + 1) as bar:
            for chunk in chunks:
                bar()
                Phrase.bulk_create(chunk)

        episode.phrases_imported = True
        episode.save()
