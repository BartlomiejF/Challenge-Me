CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE games (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  gamename TEXT NOT NULL
  );

CREATE TABLE challenges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  gamedate DATE NOT NULL,
  place_lat REAL NOT NULL,
  place_lng REAL NOT NULL,
  body TEXT NOT NULL,
  format INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (game_id) REFERENCES games (id)
);

CREATE TABLE answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chal_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  post TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (chal_id) REFERENCES challenges (id)
);
