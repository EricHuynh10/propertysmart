--create PostgreSQL tables

--create table for storing property data
CREATE TABLE IF NOT EXISTS properties (
    "tranx_id" SERIAL PRIMARY KEY, -- not from domain.com
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