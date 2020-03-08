from collections import Counter

import spacy as spacy
from progress.bar import IncrementalBar
from spacy.lang.en import English
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from models import Episode, Line, db, Phrase
from stopwords import STOP_WORDS

nlp: English = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
nlp.Defaults.stop_words = STOP_WORDS
campaign = 2
for episode in Episode.select().where(Episode.season == campaign):
    print(f"Episode {episode}")
    person = None
    text = ""
    line_select = Line.select().where(Line.episode == episode)
    with IncrementalBar('Parsing lines', max=line_select.count(), suffix="%(percent).1f%% - %(eta)ds") as bar:
        for line in Line.select().where(Line.episode == episode):
            bar.next()
            if line.person == person:
                text += " " + line.text
            else:
                person = line.person
                text += "\n"

    delete = ["\"", "--", "(", ")", "[", "]"]
    for string in delete:
        text = text.replace(string, "")
    print("run nlp")
    doc = nlp(text)
    nouns = set()
    span: Span
    for span in doc.noun_chunks:
        tok: Token
        noun_chunk = "".join([tok.text_with_ws for tok in span if not tok.is_stop]).strip()
        nouns.add(noun_chunk)
    cnt = Counter(nouns)
    with db.atomic():
        with IncrementalBar('inserting phrases', max=len(cnt)) as bar:
            for phrase, count in cnt.items():
                bar.next()
                if "\n" in phrase:
                    continue
                if len(phrase) < 4:
                    continue
                Phrase.create(text=phrase, count=count, episode=episode)
