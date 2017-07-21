#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Command line utility to analyze the news database."""
import psycopg2
import argparse


def query_db(query):
    """Query handler for the news database."""
    db = psycopg2.connect(database="news")
    cursor = db.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return data


def most_read_articles():
    """Display the most read articles."""
    articles = query_db("SELECT * FROM most_read;")
    for article, views in articles:
        print(u"%s — %d views" % (article, views))


def most_popular_authors():
    """Display the most popular authors."""
    authors = query_db("SELECT * FROM most_popular;")
    for author, views in authors:
        print(u"%s — %d views" % (author, views))


def most_error_days():
    """Display the days where errors were more than 1%% of total requests."""
    days = query_db("SELECT * FROM most_error_days;")
    for day, percentage in days:
        # %.1f%%: %.1f designates a 1 decimal place float.
        #         %% is percentage escape.
        print(u"%s — %.1f%%" % (day, percentage))


def analyze():
    """Parse arguments, execute queries and print results."""
    # Initialize the argparser with help text.
    parser = argparse.ArgumentParser(
        description="Data analysis from the log database."
    )
    # store_true is used to store a True const
    # as a default argument to the argument
    # see: https://stackoverflow.com/a/8259080
    parser.add_argument(
        "-reads",
        help="Display articles with the most read on top.",
        action='store_true',
    )
    parser.add_argument(
        "-authors",
        help="Display popular authors, those with the"
             "most article reads on top.",
        action='store_true',
    )
    parser.add_argument(
        "-errors",
        help="Display dates where more than 1%% of requests were errors.",
        action='store_true',
    )

    args = parser.parse_args()
    if args.reads:
        most_read_articles()
    elif args.authors:
        most_popular_authors()
    elif args.errors:
        most_error_days()
    else:
        parser.error("Please specify an argument :/")


if __name__ == "__main__":
    analyze()
