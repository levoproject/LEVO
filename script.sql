\SET ON_ERROR_STOP ON
\c ai5749
DROP DATABASE IF EXISTS db_levo;
CREATE DATABASE db_levo;
REVOKE ALL PRIVILEGES ON DATABASE db_levo FROM PUBLIC;
\c db_levo;

CREATE TABLE users (
    email       TEXT NOT NULL,
    username    VARCHAR(25) PRIMARY KEY,
    pass        BYTEA NOT NULL,
    profile_img BYTEA NOT NULL
);

CREATE TABLE recipes (
    recipe_id   TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    image_url   TEXT NOT NULL,
    source_url  TEXT NOT NULL,
    category    TEXT NOT NULL
);

CREATE TABLE saved_recipes (
    username    VARCHAR(25),
    recipe_id   TEXT NOT NULL,

    PRIMARY KEY (username, recipe_id),

    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aj0402, aj2601, aj1993, ai8303;
GRANT CONNECT ON DATABASE db_levo TO aj0402, aj2601, aj1993, ai8303;


-----------------------------------------values-----------------------------------------
