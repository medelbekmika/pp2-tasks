CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be: home, work, or mobile';
    END IF;

    IF EXISTS (
        SELECT 1 FROM phones
        WHERE contact_id = v_contact_id AND phone = p_phone
    ) THEN
        RAISE NOTICE 'Phone % already exists for contact %', p_phone, p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to contact %', p_phone, p_type, p_contact_name;
END;
$$;

-- ----------------------------------------------------------------
-- 2. Procedure move_to_group
--    Moves a contact to a group; creates the group if it does not exist
-- ----------------------------------------------------------------
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'New group created: %', p_group_name;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;

    RAISE NOTICE 'Contact "%" moved to group "%"', p_contact_name, p_group_name;
END;
$$;

-- ----------------------------------------------------------------
-- 3. Function search_contacts
--    Extended pattern search: matches name, email, and ALL phone
--    numbers from the phones table (extends Practice 8 version)
-- ----------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    username   VARCHAR,
    firstname  VARCHAR,
    lastname   VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones_list TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.firstname,
        c.lastname,
        c.email,
        c.birthday,
        g.name                                              AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones_list
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE
        c.username  ILIKE '%' || p_query || '%'
        OR c.firstname ILIKE '%' || p_query || '%'
        OR c.lastname  ILIKE '%' || p_query || '%'
        OR c.email     ILIKE '%' || p_query || '%'
        OR c.phone     ILIKE '%' || p_query || '%'   -- legacy field
        OR p.phone     ILIKE '%' || p_query || '%'   -- new phones table
    GROUP BY c.id, c.username, c.firstname, c.lastname,
             c.email, c.birthday, g.name
    ORDER BY c.username;
END;
$$;
