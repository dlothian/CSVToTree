#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Command: sqlite3 -csv michif.sqlite3 '.header on' 'SELECT * FROM verb' > michif.csv


import json
import sqlite3

with open("michif.json", encoding="UTF-8") as f:
    json_db = json.load(f)

conn = sqlite3.connect("michif.sqlite3")

"""
    "person": "1",
    "tense": "PST",
    "type": "VAIT",
    "mood": "INDIC",
    "order": "IND",
    "subject": "1SG",
    "object": "3SG",
    "text": "gii-ayaan",
    "gloss": "1-PST-null-have-VAIT-IND-1SG-",
    "p": "2.03e-8"
"""

conn.executescript(
    """
    DROP TABLE IF EXISTS verb;

    CREATE TABLE verb (
        text    TEXT NOT NULL,
        type    TEXT NOT NULL,
        person  TEXT,
        tense   TEXT,
        mood    TEXT NOT NULL,
        `order` TEXT NOT NULL,
        subject TEXT NOT NULL,
        object TEXT,
        gloss   TEXT NOT NULL
    );
    """
)


def generate_rows():
    for entry in json_db:
        for key in "person", "tense", "type", "mood", "order", "subject", "object", "gloss":
            entry.setdefault(key, None)
        yield entry


with conn:
    conn.executemany(
        """
        INSERT INTO verb (text, person, tense, type, mood, `order`, subject, object, gloss)
        VALUES (:text, :person, :tense, :type, :mood, :order, :subject, :object, :gloss);
        """,
        generate_rows(),
    )
