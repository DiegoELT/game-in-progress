DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS ranking;
DROP TABLE IF EXISTS list_entries;

CREATE TABLE game (
  app_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE ranking (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rating INTEGER NOT NULL, 
  description TEXT NOT NULL
);

CREATE TABLE list_entries (
  id INTEGER NOT NULL,
  app_id INTEGER NOT NULL,
  position INTEGER NOT NULL,

  CONSTRAINT fk_ids
    FOREIGN KEY (id)
    REFERENCES ranking(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_app_ids
    FOREIGN KEY (app_id)
    REFERENCES game(app_id)
    ON DELETE CASCADE
);