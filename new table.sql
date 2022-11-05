CREATE TABLE IF NOT EXISTS purchase (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	symbol text NOT NULL,
    price NUMERIC NOT NULL,
    shares integer NOT NULL,
	date text NOT NULL,
	user_id integer NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (id)
);