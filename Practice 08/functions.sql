CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    second_name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.second_name, p.phone
    FROM phonebook AS p
    WHERE p.first_name ILIKE '%' || p_pattern || '%'
       OR p.second_name ILIKE '%' || p_pattern || '%'
       OR p.phone ILIKE '%' || p_pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    second_name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit <= 0 OR p_offset < 0 THEN
        RAISE EXCEPTION 'Invalid limit or offset';
    END IF;

    RETURN QUERY
    SELECT p.id, p.first_name, p.second_name, p.phone
    FROM phonebook AS p
    ORDER BY p.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;
