from dataclasses import dataclass
from typing import Optional, List

colors = {
    "campaign1": {
        "Travis": "#7592a4",
        "Marisha": "#bd6b1e",
        "Taliesin": "#3c487d",
        "Ashley": "#fdd9be",
        "Sam": "#781485",
        "Liam": "#3d7580",
        "Laura": "#28607d",
        "Orion": "#933326",
        "Matt": "#005d73",  # random color
    },
    "campaign2": {
        "Laura": "#59c3f9",
        "Marisha": "#00146e",
        "Liam": "#fe8413",
        "Taliesin": "#be1c0d",
        "Ashley": "#868984",
        "Sam": "#dae1dd",
        "Travis": "#076708",
        "Matt": "#005d73",  # random color
        "Khary": "#bcc9e3"
    },
    "campaign3": {
        "Matt": "#005d73",  # random color
        "Robbie": "#3b4660",
        "Laura": "#584f67",
        "Marisha": "#47343f",
        "Taliesin": "#512f30",
        "Sam": "#3f5963",
        "Ashley": "#855b52",
        "Liam": "#33413a",
        "Travis": "#5f283e",
    }

}

single_speaker = {
    "Handbooker Helper": {
        1: "Matt",
        2: "Marisha",
        3: "Matt",
        4: "Rachel Seeley",
        5: "Dani Carr",
        6: "Bryan Forrest",
        7: "Bryan Forrest",
        8: "Liam",
        9: "Dani Carr",
        10: "Marisha",
        11: "Matt",
        12: "Sumalee Montano",
        13: "Laura",
        14: "Bryan Forrest",
        15: "Bryan Forrest",
        16: "Krystina Arielle",
        17: "Dani Carr",
        18: "Matt",
        19: "Marisha",
        20: "Taliesin",
        21: "Dani Carr",
        22: "Ashley",
        23: "Caleb",
        24: "Laura",
        25: "Travis",
        26: "Ashley",
        27: "Taliesin",
        28: "Marisha",
        29: "Sam",
        30: "Chris Lockey",
        31: "Brian W. Foster",
        32: "Mary Elizabeth McGlynn",
        33: "Liam",
        34: "Marisha",
        35: "Taliesin",
        36: "Will Friedle",
        37: "Satine Phoenix",
        38: "Liam",
        39: "Chris Lockey",
        40: "Sam",
        41: "Laura Bailey",
        42: "Travis",
        43: "Matt",
        44: "Matt",
    }
}

assert set(single_speaker["Handbooker Helper"].keys()) == set(range(1, 44 + 1))


@dataclass
class SeriesData:
    name: str
    slug: str
    playlist_id: Optional[str] = None
    videos: Optional[List[str]] = None
    single_speaker: bool = False
    initial_speaker: Optional[str] = None


series_data = [
    SeriesData(
        name="Campaign 1",
        slug="campaign1",
        playlist_id="PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_"
    ),
    SeriesData(
        name="Campaign 2",
        slug="campaign2",
        playlist_id="PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"
    ),
    SeriesData(
        name="Campaign 3",
        slug="campaign3",
        playlist_id="PL1tiwbzkOjQydg3QOkBLG9OYqWJ0dwlxF"
    ),
    SeriesData(
        name="Exandria Unlimited",
        slug="ExandriaUnlimited",
        playlist_id="PL1tiwbzkOjQzSnYHVT8X4pyMIbSX3i4gz"
    ),
    SeriesData(
        name="Exandria Unlimited: Kymal",
        slug="ExandriaUnlimitedKymal",
        playlist_id="PL1tiwbzkOjQwgI-BPd0nujKfVkCag3xFf"
    ),
    SeriesData(
        name="Exandria Unlimited: Calamity",
        slug="ExandriaUnlimitedCalamity",
        playlist_id="PL1tiwbzkOjQwzhdskYekmjr0h2tsbKaZw"
    ),
    SeriesData(
        name="The Nautilus Ark",
        slug="TheNautilusArk",
        videos=["LaKl58BUASo"]
    ),
    SeriesData(
        name="Handbooker Helper",
        slug="HandbookerHelper",
        playlist_id="PL1tiwbzkOjQyr6-gqJ8r29j_rJkR49uDN",
        single_speaker=True
    ),
    SeriesData(
        name="Mini Primetime",
        slug="MiniPrimetime",
        playlist_id="PL1tiwbzkOjQz9kKDaPRPrX2E7RPTaxEZd",
        initial_speaker="Will"
    ),
    SeriesData(
        name="The Legend of The Legend of Vox Machina",
        slug="TheLegendofTheLegendofVoxMachina",
        playlist_id="PL1tiwbzkOjQwJdoNetaNJE1zZVOE7xi8u"
    ),
    SeriesData(
        name="Crit Recap Animated",
        slug="CritRecapAnimated",
        playlist_id="PL1tiwbzkOjQy8yF8esjgVomDXKD-XmG20",
        initial_speaker="?"
    ),
    SeriesData(
        name="Critter Hug",
        slug="CritterHug",
        playlist_id="PL1tiwbzkOjQw6CxZVgtRsY_0WqK5DsNE1",
        single_speaker=True  # no names in subtitles
    ),
    SeriesData(
        name="UnDeadwood",
        slug="UnDeadwood",
        # playlist_id="PL1tiwbzkOjQwuwLkGnqVdJnzQ-YNX2_qz"
        videos=["AEIGOY6WDoA", "JlAW2qeLsL0", "jSGw5L9xds0", "WHxuuQ-P2Cg"]
    ),
    SeriesData(
        name="The Adventures of the Darrington Brigade",
        slug="darringtonBrigade",
        videos=["pVu_Ib1fpVI"]
    ),
    SeriesData(
        name="Dalen's Closet",
        slug="DalensCloset",
        videos=["0oclW3MXABA"]
    ),
    SeriesData(
        name="Call of Cthulhu: Shadow of the Crystal Palace",
        slug="CallOfCthulhu",
        videos=["0uhqZdJ8swQ"],
        single_speaker=True  # no names in subtitles
    ),
    SeriesData(
        name="The Search For Bob",
        slug="TheSearchForBob",
        videos=["AfEZF5G9HV4"]
    ),
    # Tails of Equestria One-Shot
    SeriesData(
        name="Stephen Colbert's D&D Adventure with Matthew Mercer",
        slug="StephenColbertOneShot",
        videos=["3658C2y4LlA"],
        single_speaker=True  # no names in subtitles
    ),
    SeriesData(
        name="The Search For Grog",
        slug="TheSearchForGrog",
        videos=["hi5pEHs76TE"]
    ),
    SeriesData(
        name="The Night Before Critmas",
        slug="TheNightBeforeCritmas",
        videos=["8zxeGydXY98"],
        single_speaker=True  # no names in subtitles
    ),
    SeriesData(
        name="Honey Heist",
        slug="HoneyHeist",
        videos=["9jbGshiuFs4", "MSNK4ThPHqc", "whbc64O0Yik"]
    ),
    SeriesData(
        name="Epic Level Battle Royale One-Shot",
        slug="EpicLevelBattleRoyaleOneShot",
        videos=["q3BGg0d8DvU"]
    ),
    SeriesData(
        name="Sam's One-Shot",
        slug="SamsOneShot",
        videos=["LfeAYN8f1AU"]
    ),
    SeriesData(
        name="Hearthstone One-Shot",
        slug="HearthstoneOneShot",
        videos=["qA4-q4gk_yY"]
    ),
    SeriesData(
        name="Grog's One-Shot",
        slug="GrogsOneShot",
        videos=["kLnvrocetq8"]
    ),
    SeriesData(
        name="Bar Room Blitz",
        slug="BarRoomBlitz",
        videos=["rnq3VBQu_kI"]
    ),
    SeriesData(
        name="Thursday By Night",
        slug="ThursdayByNight",
        videos=["rnq3VBQu_kI", "eXPu1wk-Ev4"]
    ),
    SeriesData(
        name="Shadow of War",
        slug="ShadowofWar",
        videos=["c9lC5_qjkFE", "Mk21j54rX-M"]
    ),
    SeriesData(
        name="Battle Royale One-Shot",
        slug="BattleRoyaleOneShot",
        videos=["tasz1xUVLhg"]
    ),
    SeriesData(
        name="Liam's Quest: Full Circle",
        slug="LiamsQuestFullCircle",
        videos=["LHita2t54xY"]
    ),
    SeriesData(
        name="The Return of Liam!",
        slug="TheReturnofLiam",
        videos=["LgHm3Ct0Zh0"]
    ),
    SeriesData(
        name="Show Q&A and Battle Royale",
        slug="ShowQnAandBattleRoyale",
        videos=["4FI8qB-yh-w"]
    ),
    SeriesData(
        name="Liam's Quest!",
        slug="LiamsQuest",
        videos=["7Tdl6GhiSI8"]
    ),
    SeriesData(
        name="Deadlands One-Shot",
        slug="DeadlandsOneShot",
        videos=["q0hjGf2bK08"]
    ),
    SeriesData(
        name="TO THE POOP! - The Goblins",
        slug="ToThePoop",
        videos=["u8MRyyFDX3c"]
    ),
    SeriesData(
        name="Critical Trolls",
        slug="CriticalTrolls",
        videos=["EjimabBvZgw"]
    ),
    SeriesData(
        name="Cinderbrush: A Monsterhearts Story",
        slug="Cinderbrush",
        videos=["51ykIVq9KcM"]
    ),
    SeriesData(
        name="DOOM Eternal One-Shot",
        slug="DOOMEternalOneShot",
        videos=["CX8I4M7MPo4"]
    ),
    SeriesData(
        name="Diablo One Shot",
        slug="DiabloOneShot",
        videos=["yODMT1m85FQ"]
    ),
    SeriesData(
        name="The Elder Scrolls Online",
        slug="TheElderScrollsOnline",
        videos=["E-YCzpYDIyA", "MX5qmiUJYBo", "y6GpnRz6RPo"]
    ),
    SeriesData(
        name="Vox Machina vs. Mighty Nein",
        slug="VoxMachinaVsMightyNein",
        videos=["LpBIQhWAhuM"]
    ),
    SeriesData(
        name="Critical Role and the Club of Misfits",
        slug="ClubOfMisfits",
        videos=["PRmVQKOy9Bo"]
    ),
    SeriesData(
        name="Guest Battle Royale",
        slug="GuestBattleRoyale",
        videos=["jE7wB2JG190"]
    ),
    # FIXME: temporarily removed as the video is age-restricted
    # SeriesData(
    #     name="Tiny Tina's Wonderlands One-Shot",
    #     slug="TinyTinasWonderlands",
    #     videos=["nJrLQHo9rW0"]
    # ),
    SeriesData(
        name="Dignity: An Adventure with Stephen Colbert",
        slug="Dignity",
        videos=["FdqcUTNHwyo"]
    ),
    SeriesData(
        name="A Familiar Problem: Sprinkle’s Incredible Journey!",
        slug="AFamiliarProblem",
        videos=["dDQTNGvRH4Q"]
    ),
    SeriesData(
        name="Game Masters of Exandria Roundtable",
        slug="GameMastersOfExandriaRoundtable",
        videos=["LmZSWKPXhZ4"]
    ),
    SeriesData(
        name="4-Sided Dive",
        slug="4SidedDive",
        playlist_id="PL1tiwbzkOjQyUQ7J7Bg_OY6AFybns1pIk"
    ),
    SeriesData(
        name="The Mighty Nein Reunited",
        slug="MightyNeinReunited",
        playlist_id="PL1tiwbzkOjQxLSFOtwuzl-c6wEkjaqsv5"
    ),

]

series_data_by_slug = {}

for series in series_data:
    series_data_by_slug[series.slug] = series
