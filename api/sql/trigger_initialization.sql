CREATE TRIGGER rooms_update_modified_timestamp
  BEFORE UPDATE ON pp.rooms
  FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();

CREATE TRIGGER games_update_modified_timestamp
  BEFORE UPDATE ON pp.games
  FOR EACH ROW EXECUTE PROCEDURE set_updated_timestamp();