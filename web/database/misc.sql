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


"""
BELOW CODE IS FOR FUTURE USE

DROP VIEW IF EXISTS less_than_five_br;
DROP VIEW IF EXISTS five_plus_br;
DROP VIEW IF EXISTS All_br;

-- Suburb summary - Less than 5 bedroom types
CREATE OR REPLACE VIEW less_than_five_br AS
WITH RecentTransactions AS (
    SELECT suburb, 
            state, 
            postcode,
            beds,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
            COUNT(*) as num_tranx
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '1 year'
        AND beds < 5
    GROUP BY suburb, state, postcode, beds
),
TransactionsFiveYearsAgo AS (
    SELECT suburb, 
            state, 
            postcode,
            beds,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price_five_years_ago,
            COUNT(*) as num_tranx_five_years_ago
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '6 years' 
        AND "soldDate" < CURRENT_DATE - INTERVAL '5 years'
        AND beds < 5
    GROUP BY suburb, state, postcode, beds
)
SELECT DISTINCT p.suburb, 
        p.state,
        p.postcode,
        p.beds::TEXT AS beds,
        t1.median_price, 
        t1.num_tranx, 
        t2.median_price_five_years_ago, 
        t2.num_tranx_five_years_ago,
        CASE 
            WHEN t1.median_price IS NOT NULL AND t2.median_price_five_years_ago IS NOT NULL AND t2.median_price_five_years_ago > 0 
            THEN (POWER(t1.median_price / t2.median_price_five_years_ago, 1.0/5) - 1) * 100
            ELSE NULL 
        END AS annual_growth_rate,
        CASE 
            WHEN t1.num_tranx IS NOT NULL AND t2.num_tranx_five_years_ago IS NOT NULL AND t2.num_tranx_five_years_ago > 0
            THEN (POWER(t1.num_tranx::FLOAT / t2.num_tranx_five_years_ago::FLOAT, 1.0/5) - 1) * 100
            ELSE NULL 
        END AS annual_vol_growth_rate
FROM properties p
LEFT JOIN RecentTransactions t1 ON p.suburb = t1.suburb AND p.state = t1.state AND p.postcode = t1.postcode AND p.beds = t1.beds
LEFT JOIN TransactionsFiveYearsAgo t2 ON p.suburb = t2.suburb AND p.state = t2.state AND p.postcode = t2.postcode AND p.beds = t2.beds
WHERE p.beds < 5
ORDER BY p.suburb, beds;


-- Suburb summary - 5+ bedroom type
CREATE OR REPLACE VIEW five_plus_br AS
WITH RecentTransactions AS (
    SELECT suburb,
            state, 
            postcode,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
            COUNT(*) as num_tranx
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '1 year'
        AND beds >= 5
    GROUP BY suburb, state, postcode
),
TransactionsFiveYearsAgo AS (
    SELECT suburb,
            state, 
            postcode,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price_five_years_ago,
            COUNT(*) as num_tranx_five_years_ago
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '6 years' 
        AND "soldDate" < CURRENT_DATE - INTERVAL '5 years'
        AND beds >= 5
    GROUP BY suburb, state, postcode
)
SELECT DISTINCT p.suburb, 
        p.state,
        p.postcode,
        '5+' AS beds,
        t1.median_price, 
        t1.num_tranx, 
        t2.median_price_five_years_ago, 
        t2.num_tranx_five_years_ago,
        CASE 
            WHEN t1.median_price IS NOT NULL AND t2.median_price_five_years_ago IS NOT NULL AND t2.median_price_five_years_ago > 0 
            THEN (POWER(t1.median_price / t2.median_price_five_years_ago, 1.0/5) - 1) * 100
            ELSE NULL 
        END AS annual_growth_rate,
        CASE 
            WHEN t1.num_tranx IS NOT NULL AND t2.num_tranx_five_years_ago IS NOT NULL AND t2.num_tranx_five_years_ago > 0
            THEN (POWER(t1.num_tranx::FLOAT / t2.num_tranx_five_years_ago::FLOAT, 1.0/5) - 1) * 100
            ELSE NULL 
        END AS annual_vol_growth_rate
FROM properties p
LEFT JOIN RecentTransactions t1 ON p.suburb = t1.suburb AND p.state = t1.state AND p.postcode = t1.postcode
LEFT JOIN TransactionsFiveYearsAgo t2 ON p.suburb = t2.suburb AND p.state = t2.state AND p.postcode = t2.postcode
WHERE p.beds >= 5
ORDER BY p.suburb, beds;


-- Suburb summary - All bedroom types
CREATE OR REPLACE VIEW All_br AS
WITH RecentTransactions AS (
    SELECT suburb,
            state, 
            postcode,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price,
            COUNT(*) as num_tranx
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '1 year'
    GROUP BY suburb, state, postcode
),
TransactionsFiveYearsAgo AS (
    SELECT suburb,
            state, 
            postcode,
            percentile_cont(0.5) WITHIN GROUP (ORDER BY price) AS median_price_five_years_ago,
            COUNT(*) as num_tranx_five_years_ago
    FROM properties
    WHERE "soldDate" > CURRENT_DATE - INTERVAL '6 years' 
        AND "soldDate" < CURRENT_DATE - INTERVAL '5 years'
    GROUP BY suburb, state, postcode
)
SELECT DISTINCT p.suburb, 
        p.state,
        p.postcode,
        'All' AS beds,
        t1.median_price, 
        t1.num_tranx, 
        t2.median_price_five_years_ago, 
        t2.num_tranx_five_years_ago,
        CASE 
            WHEN t1.median_price IS NOT NULL AND t2.median_price_five_years_ago IS NOT NULL AND t2.median_price_five_years_ago > 0 
            THEN (POWER(t1.median_price / t2.median_price_five_years_ago, 0.2) - 1) * 100
            ELSE NULL 
        END AS annual_growth_rate,
        CASE 
            WHEN t1.num_tranx IS NOT NULL AND t2.num_tranx_five_years_ago IS NOT NULL AND t2.num_tranx_five_years_ago > 0
            THEN (POWER(t1.num_tranx::FLOAT / t2.num_tranx_five_years_ago::FLOAT, 1.0/5) - 1) * 100
            ELSE NULL 
        END AS annual_vol_growth_rate
FROM properties p
LEFT JOIN RecentTransactions t1 ON p.suburb = t1.suburb AND p.state = t1.state AND p.postcode = t1.postcode
LEFT JOIN TransactionsFiveYearsAgo t2 ON p.suburb = t2.suburb AND p.state = t2.state AND p.postcode = t2.postcode
WHERE p.beds >= 5
ORDER BY p.suburb, beds;


-- Suburb summary
DROP TABLE IF EXISTS suburb_summ;
SELECT * INTO suburb_summ from (
    SELECT * FROM less_than_five_br
    UNION ALL
    SELECT * FROM five_plus_br
    UNION ALL
    SELECT * FROM All_br
)
ORDER BY state, suburb, beds;

"""
