CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

-- CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    category TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    amount NUMERIC NOT NULL,
    description TEXT,
    year NUMRIC NOT NULL,
    month NUMRIC NOT NULL,
    day NUMRIC NOT NULL,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX username ON users (username);
    -- FOREIGN KEY (category_id) REFERENCES categories (id)
-- CREATE UNIQUE INDEX user_id_cat ON categories (user_id);
-- CREATE UNIQUE INDEX user_id_ent ON entries (user_id);

