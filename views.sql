CREATE VIEW most_popular AS (
  SELECT authors.name,
         count(ip) AS total_views
  FROM articles
  JOIN log
  ON path = CONCAT('/article/', articles.slug)
  JOIN authors
  ON authors.id = articles.author
  GROUP BY authors.name
  ORDER BY total_views DESC
);

/* for CONCAT function reference check:
   https://www.postgresql.org/docs/9.1/static/functions-string.html
 */
CREATE VIEW most_read AS (
  SELECT title AS title,
         count(log.ip) AS views
  FROM articles
  JOIN log
  ON (path = CONCAT('/article/', articles.slug))
  GROUP BY title
  ORDER BY views DESC
  LIMIT 3
);

CREATE VIEW most_error_days AS (
  SELECT count_date, round(percentage, 1) FROM
    (SELECT visits.visit_date as count_date,
      /* casting integers to numeric and calculating error percentage
         formula: (errors / (errors + hits) ) * 100
         https://www.postgresql.org/docs/9.5/static/typeconv-oper.html
      */
      (
        (
          cast(errors.errors_total AS NUMERIC) /
          cast((visits.visits_total + errors.errors_total) AS NUMERIC)
        ) * 100
      ) AS percentage
     FROM
        (
          /* The valid visits table
             returns: visits_total | date
          */
          SELECT count(path) AS visits_total, CAST(time AS DATE) as visit_date
          FROM log
          WHERE status = '200 OK'
          GROUP BY visit_date
        ) visits,
        (
          /* The errors table
             returns: errors_total | date
          */
          SELECT count(path) AS errors_total, CAST(time AS DATE) as error_date
          FROM log
          WHERE status = '404 NOT FOUND'
          GROUP BY error_date
        ) errors

    WHERE (visits.visit_date = errors.error_date)
    ORDER BY percentage DESC
  ) percentages
  WHERE (percentage > 1.0)
);
