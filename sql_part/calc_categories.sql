CREATE OR REPLACE FUNCTION public.calc_categories()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN

update products
set category_id =  4;

update products
set category_id =  5
where description ilike '%свит%';

update products
set category_id =  3
where description ilike '%япон%';

update products
set category_id =  6
where description ilike '%япон%'
and description ilike '%свит%';

END;
$function$
;
