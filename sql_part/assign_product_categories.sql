CREATE OR REPLACE FUNCTION assign_product_categories()
RETURNS void AS $$
BEGIN
    -- Assign categories to products based on description
    UPDATE products
    SET category_id = (
        SELECT id FROM categories WHERE name = 'Картины'
    )
    WHERE description IS NOT NULL;

    UPDATE products
    SET category_id = (
        SELECT id FROM categories WHERE name = 'Свитки'
    )
    WHERE description IS NOT NULL
    AND description ILIKE '%свит%';

    UPDATE products
    SET category_id = (
        SELECT id FROM categories WHERE name = 'Альбомы'
    )
    WHERE description ILIKE '%альбом%';

    UPDATE products
    SET category_id = (
        SELECT id FROM categories WHERE name = 'Жемчужины коллекции'
    )
    WHERE description ILIKE '%жемчуж%';
END;
$$ LANGUAGE plpgsql;