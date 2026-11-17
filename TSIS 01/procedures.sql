
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_second_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_phone_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE first_name = p_first_name
      AND second_name = p_second_name;

    IF v_contact_id IS NOT NULL THEN

        IF EXISTS (
            SELECT 1
            FROM phones
            WHERE contact_id = v_contact_id
              AND phone = p_phone
        ) THEN
            RETURN;
        END IF;

        SELECT id
        INTO v_phone_id
        FROM phones
        WHERE contact_id = v_contact_id
          AND type = 'mobile'
        ORDER BY id
        LIMIT 1;

        IF v_phone_id IS NOT NULL THEN
            UPDATE phones
            SET phone = p_phone
            WHERE id = v_phone_id;
        ELSE
            INSERT INTO phones(contact_id, phone, type)
            VALUES (v_contact_id, p_phone, 'mobile');
        END IF;

    ELSE
        INSERT INTO contacts(first_name, second_name)
        VALUES (p_first_name, p_second_name)
        RETURNING id INTO v_contact_id;

        INSERT INTO phones(contact_id, phone, type)
        VALUES (v_contact_id, p_phone, 'mobile');
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
            CALL upsert_contact(
                v_first_name,
                v_second_name,
                v_phone
            );
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
        DELETE FROM contacts
        WHERE first_name = p_value;

    ELSIF p_type = 'phone' THEN
        DELETE FROM phones
        WHERE phone = p_value;

    ELSE
        RAISE EXCEPTION 'Invalid delete type';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE first_name || ' ' || second_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE first_name || ' ' || second_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;
