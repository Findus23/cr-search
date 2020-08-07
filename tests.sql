select name, count(name) as count, sum(length(text)) as chars
from line
         join person p on line.person_id = p.id
group by name
order by chars desc;

select text, sum(count) as count
from phrase
group by text
order by count desc;

select text, char_length(phrase.text) as len
from phrase
order by len desc;

-- delete
-- from phrase;

EXPLAIN analyse
SELECT text, sum(count) as total_count
FROM phrase
where text ilike '%head%'
group by text
ORDER BY total_count DESC;

-- query made by suggestion
-- debug with https://dalibo.github.io/pev2/
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)
SELECT "t1"."text", SUM("t1"."count") AS "total_count"
FROM "phrase" AS "t1"
         INNER JOIN "episode" AS "t2" ON ("t1"."episode_id" = "t2"."id")
WHERE ((("t2"."series_id" = 1) AND ("t2"."episode_number" <= 30)) AND ("t1"."text" ILIKE '%head%'))
GROUP BY "t1"."text"
ORDER BY total_count DESC
LIMIT 10;


CREATE EXTENSION pg_trgm;


CREATE INDEX phrases_text_index ON phrase USING gin (text gin_trgm_ops);
drop index phrases_text_index;


-- query made by full text search
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)
SELECT "t1"."id",
       "t1"."text",
       "t1"."search_text",
       "t1"."person_id",
       "t1"."isnote",
       "t1"."ismeta",
       "t1"."starttime",
       "t1"."endtime",
       "t1"."episode_id",
       "t1"."order",
       "t2"."id",
       "t2"."name",
       "t2"."color",
       "t2"."season",
       "t3"."id",
       "t3"."season",
       "t3"."episode_number",
       "t3"."video_number",
       "t3"."youtube_id",
       "t3"."text_imported",
       "t3"."phrases_imported",
       ts_rank("t1"."search_text", websearch_to_tsquery('english', 'house')) AS "rank"
FROM "line" AS "t1"
         INNER JOIN "person" AS "t2" ON ("t1"."person_id" = "t2"."id")
         INNER JOIN "episode" AS "t3" ON ("t1"."episode_id" = "t3"."id")
WHERE ((("t1"."search_text" @@ websearch_to_tsquery('english', 'house')) AND ("t3"."episode_number" <= 1000)) AND
       ("t3"."season" = 1))
ORDER BY rank DESC
LIMIT 20
