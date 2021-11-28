"""
ATTENTION: This file contains the suggestions displayed.
Only suggestions up to the selected episode are shown on the website,
but you might find spoilers below.
That said, I try to only use phrases that don't contain spoilers themselves.

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Suggestion:
    text: str
    # only show this suggestion to people who have watched at least this episode
    episode: Optional[int] = None


suggestions = {
    "campaign1": [
        Suggestion(
            text="I am Grog, the unintimidated.",
            episode=18
        ),
        Suggestion(
            text="Bidet",
            episode=60
        ),
        Suggestion(
            text="my esteemed panel of extremely mature",
            episode=83
        ),
        Suggestion(
            text="I turn into a goldfish",
            episode=97
        ),
        Suggestion(
            text="No, it's fine! We're gods!",
            episode=97
        ),
        Suggestion(
            text="Life needs things to live",
            episode=63
        ),
        Suggestion(
            text="I'd like to share the news of our Lord and Savior: My axe in your face!",
            episode=29
        ),
        Suggestion(
            text="Your secret is safe with my indifference",
            episode=45
        ),
        Suggestion(
            text="Have you ever had a Blueberry Cupcake",
            episode=93
        ),
        Suggestion(
            text="Okay Okay Okay Okay",
            episode=63
        ),
        Suggestion(
            text="I am your god, long may I reign",
            episode=18
        ),
        Suggestion(
            text="We're running, it's bad",
            episode=45
        )
    ],
    "campaign2": [
        Suggestion(
            text="Tieflings can only see movement.",
            episode=1
        ),
        Suggestion(
            text="Because I'm really fucking strong.",
            episode=1
        ),
        Suggestion(
            text="I use thaumaturgy to open all the windows",
            episode=2
        ),
        Suggestion(
            text="Regular gnoll",
            episode=5
        ),
        Suggestion(
            text="Nudity. It usually works.",
            episode=2
        ),
        Suggestion(
            text="Donuts",
            episode=3
        ),
        Suggestion(
            text="The world does need an asshole",
            episode=4
        ),
        Suggestion(
            text="We'll try to catch you in a jar",
            episode=5
        ),
        Suggestion(
            text="Fjord Explorers",
            episode=6
        ),
        Suggestion(
            text="Eldritch Blast",
            episode=6
        ),
        Suggestion(
            text="You look like a nerd",
            episode=8
        ),
        Suggestion(
            text="The best lay ever",
            episode=8
        ),
        Suggestion(
            text="Only steal from grumpy people",
            episode=9
        ),
        Suggestion(
            text="You can reply to this message",
            episode=11
        ),
        Suggestion(
            text="Be the chaos you want to see in the world",
            episode=12
        ),
        Suggestion(
            text="I'm always ready to make a damn fool of myself",
            episode=12
        ),
        Suggestion(
            text="The metagaming pigeon",
            episode=12
        ),
        Suggestion(
            text="My name is Molly",
            episode=14
        ),
        Suggestion(
            text="A simple tool",
            episode=15
        ),
        Suggestion(
            text="I am your god, long may I reign",
            episode=18
        ),
        Suggestion(
            text="I cast Regret",
            episode=21
        ),
        Suggestion(
            text="The Traveler's bullshit!",
            episode=26
        ),
        Suggestion(
            text="Uk'otoa",
            episode=37
        ),
        Suggestion(
            text="Fluffernutter",
            episode=39
        ),
        Suggestion(
            text="Sleep well with your bad decisions",
            episode=40
        ),
        Suggestion(
            text="Not cool, man",
            episode=44
        ),
        Suggestion(
            text="We're running, it's bad!",
            episode=45
        ),
        Suggestion(
            text="Hello Bees",
            episode=46
        ),
        Suggestion(
            text="Yes. It's a chair. It's a standard chair.",
            episode=48
        ),
        Suggestion(
            text="Are you secretly in love with me?",
            episode=50
        ),
        Suggestion(
            text="It’s a regular fucking turtle",
            episode=60
        ),
        Suggestion(
            text="The rule is that evil dies",
            episode=74
        ),
        Suggestion(
            text="Oh shit, are we a cult?",
            episode=77
        ),
        Suggestion(
            text="I want to role play fish and chips!",
            episode=84
        ),
        Suggestion(
            text="I pick and choose my apologies",
            episode=84
        ),
        Suggestion(
            text="Can I get a hug?",
            episode=87
        ),
        Suggestion(
            text="I smell like a crayon",
            episode=91
        ),
        Suggestion(
            text="Captain, we're being followed by a tiny island.",
            episode=99
        )
    ],
    "campaign3": [
        Suggestion(
            text="Copper's more of an insult",
            episode=1
        ),
        Suggestion(
            text="The rug is more dexterous than I am?",
            episode=1
        ),
        Suggestion(
            text="Optimism is the most optimistic",
            episode=2
        ),
        Suggestion(
            text="Does anyone know how to make things quiet",
            episode=3
        ),
        Suggestion(
            text="This isn't even metagaming",
            episode=4
        )
    ],
    "VoxMachinaVsMightyNein": [
        Suggestion(
            text="Oh, you one of those rich boys?"
        ),
        Suggestion(
            text="Some days you get hit by a T-Rex."
        )
    ],
    "ClubOfMisfits": [
        Suggestion("I'm going to try something weird.")
    ],
    "TheNautilusArk": [
        Suggestion("Rifle with a PhD"),
        Suggestion("It's got a trigger and a little thing")
    ]
}
