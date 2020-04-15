from collections import Counter

import spacy as spacy
from alive_progress import alive_bar
from spacy.lang.en import English
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from models import Episode, Line, db, Phrase
from stopwords import STOP_WORDS

nlp: English = spacy.load("en_core_web_sm", disable=["ner", "textcat"])
nlp.Defaults.stop_words = STOP_WORDS
for episode in Episode.select().where((Episode.phrases_imported == False) & (Episode.text_imported == True)):
    print(episode.video_number, episode.title)
    person = None
    text = ""
    line_select = Line.select().where(Line.episode == episode)
    with alive_bar(line_select.count(), title='Parsing lines') as bar:
        for line in Line.select().where(Line.episode == episode):
            bar()
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
        with alive_bar(len(cnt), title='inserting phrases') as bar:
            for phrase, count in cnt.items():
                bar()
                if "\n" in phrase:
                    continue
                if len(phrase) < 4:
                    continue
                Phrase.create(text=phrase, count=count, episode=episode)
    episode.phrases_imported = True
    episode.save()
