--create PostgreSQL tables

--create table for storing property data, used in the second run development
CREATE TABLE IF NOT EXISTS properties (
    "tranx_id" SERIAL, -- not from domain.com
    "property_id" BIGINT,
    "beds" INT,
    "baths" INT,
    "parking" INT,
    "propertyType" VARCHAR(255),
    "propertyTypeFormatted" VARCHAR(255),
    "isRural" BOOLEAN,
    "landSize" INT,
    "landUnit" VARCHAR(255),
    "isRetirement" BOOLEAN,
    "street" VARCHAR(255),
    "suburb" VARCHAR(255),
    "state" VARCHAR(255),
    "postcode" VARCHAR(4),
    "lat" FLOAT,
    "lng" FLOAT,
    "price" BIGINT,
    "tagText" VARCHAR(255),
    "tagClassName" VARCHAR(255),
    "soldDate" DATE,
    "url" VARCHAR(255),
    PRIMARY KEY ("property_id", "soldDate")
);

--create table for storing school data
CREATE TABLE IF NOT EXISTS schools (
    "id" SERIAL,
    "school" VARCHAR(255),
    "suburb" VARCHAR(255),
    "state" VARCHAR(255),
    "postcode" VARCHAR(4),
    "schoolType" VARCHAR(255),
    "educationLevel" VARCHAR(255),
    "score" FLOAT,
    PRIMARY KEY ("school", "suburb", "state", "postcode", "educationLevel")
);


-- Create table for storing suburb data
CREATE TABLE IF NOT EXISTS suburbs (
    "id" SERIAL,
    "state" VARCHAR(255),
    "suburb" VARCHAR(255),
    "postcode" VARCHAR(4),
    "beds" INT,
    "propertyType" VARCHAR(255),
    "medianPrice" FLOAT,
    "medianRent" FLOAT,
    "avgDaysOnMarket" FLOAT,
    "soldThisYear" INT,
    "entryLevelPrice" FLOAT,
    "luxuryLevelPrice" FLOAT,
    "annualGrowth" FLOAT,
    "rentalYield" FLOAT,
    "totalYield" FLOAT,
    "remoteness" VARCHAR(255),
    "remoteness_code" VARCHAR(2),
    PRIMARY KEY ("state", "suburb", "postcode", "beds", "propertyType")
);


-- Create table for storing location options
CREATE TABLE IF NOT EXISTS location_options (
    "state" VARCHAR(255),
    "suburb" VARCHAR(255),
    "postcode" VARCHAR(4),
    PRIMARY KEY ("state", "suburb", "postcode")
);

-- add postgis extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- add geometry column to properties table
ALTER TABLE properties ADD COLUMN location GEOGRAPHY(POINT, 4326);
UPDATE properties SET ST_MakePoint(CAST(lng AS FLOAT), CAST(lat AS FLOAT))::geography;

-- index location column
CREATE INDEX location_idx ON properties USING GIST(location);

