-- Create a trigger to run the code when the suburbs table is updated
CREATE OR REPLACE FUNCTION update_location_options()
RETURNS TRIGGER AS $$
BEGIN
    -- Drop the location_options table
    DROP TABLE IF EXISTS location_options;
    
    -- Recreate the location_options table
    CREATE TABLE location_options AS
    SELECT DISTINCT suburb, state, postcode
    FROM suburbs
    ORDER BY state, suburb;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_location_options_trigger
AFTER INSERT OR UPDATE OR DELETE ON suburbs
FOR EACH STATEMENT
EXECUTE FUNCTION update_location_options();

