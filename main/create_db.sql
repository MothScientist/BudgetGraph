CREATE TABLE IF NOT EXISTS Users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    token text NOT NULL
);