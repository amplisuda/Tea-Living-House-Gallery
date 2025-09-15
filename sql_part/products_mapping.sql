CREATE OR REPLACE FUNCTION products_mapping()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
	truncate table products;
    INSERT INTO products (name, image_url, description, hash, main_url)
    WITH names AS (
        SELECT
            COALESCE(
                REGEXP_REPLACE(title, '^(.*?)"([^"]+)"(.*)$', '\2'),
                SPLIT_PART(title, '.', 1)
            ) AS name,
            title
        FROM images
    ), main_urls as (
SELECT
    title,
    url AS main_url
FROM (
    SELECT
        title,
        url,
        vk_id,
        ROW_NUMBER() OVER (PARTITION BY title ORDER BY vk_id ASC) AS rn
    FROM images
) t
WHERE rn = 1
)
    SELECT
        name,
        JSONB_AGG(distinct url) AS image_urls,
        i.title,
		md5(i.title) as hash,
		max(mu.main_url) as main_url
    FROM images i
	JOIN main_urls mu on i.title = mu.title
    LEFT JOIN names n ON i.title = n.title
    GROUP BY name, i.title
    ORDER BY name;
	delete from products where hash ='d41d8cd98f00b204e9800998ecf8427e';
END;
$function$
;
