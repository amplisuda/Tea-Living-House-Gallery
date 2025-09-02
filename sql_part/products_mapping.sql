CREATE OR REPLACE FUNCTION public.products_mapping()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
	truncate table products;
    INSERT INTO products (name, image_url, description, hash)
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
        i.title,
		md5(i.title) as hash
    FROM images i
    LEFT JOIN names n ON i.title = n.title
    GROUP BY name, i.title
    ORDER BY name;
	delete from products where hash ='d41d8cd98f00b204e9800998ecf8427e';
END;
$function$
;