colors_c1 = {
    "Travis": "#7592a4",
    "Marisha": "#bd6b1e",
    "Taliesin": "#3c487d",
    "Ashley": "#fdd9be",
    "Sam": "#781485",
    "Liam": "#3d7580",
    "Laura": "#28607d",
    "Orion": "#933326"
}

colors_c2 = {
    "Laura": "#59c3f9",
    "Marisha": "#00146e",
    "Liam": "#fe8413",
    "Taliesin": "#be1c0d",
    "Ashley": "#868984",
    "Sam": "#dae1dd",
    "Travis": "#076708",
    "Matt": "#005d73",  # random color
    "Khary": "#bcc9e3"
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

series_data = [
    {
        "name": "Campaign 1",
        "playlist_id": "PL1tiwbzkOjQz7D0l_eLJGAISVtcL7oRu_",
    },
    {
        "name": "Campaign 2",
        "playlist_id": "PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"

    },
    {
        "name": "Handbooker Helper",
        "playlist_id": "PL1tiwbzkOjQyr6-gqJ8r29j_rJkR49uDN",
        "single_speaker": True
    },
    {
        "name": "Mini Primetime",
        "playlist_id": "PL1tiwbzkOjQz9kKDaPRPrX2E7RPTaxEZd",
        "initial_speaker": "Will"
    }
]
