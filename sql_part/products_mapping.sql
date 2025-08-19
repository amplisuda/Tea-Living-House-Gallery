CREATE OR REPLACE FUNCTION products_mapping()
RETURNS VOID AS $$
BEGIN
	delete from products;
    INSERT INTO products (name, image_url, description)
    WITH names AS (
        SELECT
            COALESCE(
                REGEXP_REPLACE(title, '^(.*?)"([^"]+)"(.*)$', '\2'),
                SPLIT_PART(title, '.', 1)
            ) AS name,
            title
        FROM images
    )
    SELECT
        name,
        JSONB_AGG(distinct url) AS image_urls,
        i.title
    FROM images i
    LEFT JOIN names n ON i.title = n.title
    GROUP BY name, i.title
    ORDER BY name;
END;
$$ LANGUAGE plpgsql;