DROP FUNCTION IF EXISTS get_contacts_by_pattern(TEXT);
DROP FUNCTION IF EXISTS get_contacts_page(INTEGER, INTEGER);


CREATE OR REPLACE FUNCTION get_contacts_by_pattern(
    p_pattern TEXT
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    second_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.first_name,
        c.second_name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.second_name ILIKE '%' || p_pattern || '%'
       OR c.email ILIKE '%' || p_pattern || '%'
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
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_limit <= 0 OR p_offset < 0 THEN
        RAISE EXCEPTION 'Invalid limit or offset';
    END IF;

    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.second_name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    second_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.first_name,
        c.second_name,
        c.email,
        c.birthday,
        g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.second_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;
