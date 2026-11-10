CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_second_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE first_name = p_first_name
          AND second_name = p_second_name
    ) THEN

        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND second_name = p_second_name;

    ELSE

        INSERT INTO phonebook(first_name, second_name, phone)
        VALUES (p_first_name, p_second_name, p_phone);

    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    IN p_contacts JSONB,
    INOUT p_invalid JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    item JSONB;
    v_first_name VARCHAR;
    v_second_name VARCHAR;
    v_phone VARCHAR;
BEGIN
    p_invalid := '[]'::JSONB;

    FOR item IN
        SELECT value
        FROM jsonb_array_elements(p_contacts)
    LOOP
        v_first_name := item->>'first_name';
        v_second_name := item->>'second_name';
        v_phone := item->>'phone';

        IF v_phone IS NULL OR v_phone !~ '^\+?[0-9]{10,15}$' THEN

            p_invalid := p_invalid || jsonb_build_array(item);

        ELSE

            INSERT INTO phonebook(first_name, second_name, phone)
            VALUES (v_first_name, v_second_name, v_phone);

        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_type = 'name' THEN

        DELETE FROM phonebook
        WHERE first_name = p_value;

    ELSIF p_type = 'phone' THEN

        DELETE FROM phonebook
        WHERE phone = p_value;

    ELSE

        RAISE EXCEPTION 'Invalid delete type';

    END IF;
END;
$$;
