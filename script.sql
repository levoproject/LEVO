\SET ON_ERROR_STOP ON
\c ai5749
DROP DATABASE IF EXISTS db_levo;
CREATE DATABASE db_levo;
REVOKE ALL PRIVILEGES ON DATABASE db_levo FROM PUBLIC;
\c db_levo;

CREATE TABLE users (
    username    VARCHAR(25) PRIMARY KEY,
    pass        BYTEA
);

CREATE TABLE recipes (
    recipe_id   VARCHAR(25) PRIMARY KEY,
    title       VARCHAR(25),
    image_url   TEXT NOT NULL,
    source_url  TEXT NOT NULL
);

CREATE TABLE saved_recipes (
    username    VARCHAR(25),
    recipe_id   TEXT NOT NULL,

    PRIMARY KEY (username, recipe_id),

    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
);

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aj0402;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aj2601;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aj1993;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ai8303;


-----------------------------------------values-----------------------------------------