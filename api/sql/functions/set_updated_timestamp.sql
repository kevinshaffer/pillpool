CREATE FUNCTION set_updated_timestamp()
  RETURNS TRIGGER
  LANGUAGE plpgsql
AS $$
BEGIN
  NEW.date_modified := extract(epoch from now());
  RETURN NEW;
END;
$$;