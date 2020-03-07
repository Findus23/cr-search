from sonic import IngestClient, ControlClient

from models import Line

with IngestClient("127.0.0.1", 1491, "SecretPassword") as ingestcl:
    ingestcl.flush_collection("crsearch")
    total = Line.select().count()
    i = 0
    for line in Line.select():
        ingestcl.push("crsearch", "crsearch", str(line.id), line.text,lang="eng")
        if i % 100 == 0: print(i, total)
        i += 1
    print(ingestcl.count("crsearch", "crsearch"))

with ControlClient("127.0.0.1", 1491, "SecretPassword") as controlcl:
    controlcl.trigger("consolidate")
