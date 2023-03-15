
-- name: create-new-pack<!
INSERT
INTO packs (pack_id, pack_name, pack_price, images_per_pack)
VALUES (:pack_id, :pack_name, :pack_price, :images_per_pack)
RETURNING
    id,
    pack_id,
    pack_name,
    pack_price,
    images_per_pack,
    created_at,
    updated_at;


-- name: update-pack<!
UPDATE packs
SET 
    pack_name       = :pack_name,
    pack_price        = :pack_price,
    images_per_pack = :images_per_pack

WHERE
    pack_id = :pack_id
RETURNING updated_at;

-- name: get-pack<!
SELECT *
FROM packs
WHERE pack_id = :pack_id


-- name: get-all-packs<!
SELECT *
FROM packs



-- name: delete-pack!
DELETE
FROM packs
WHERE pack_id = :pack_id
