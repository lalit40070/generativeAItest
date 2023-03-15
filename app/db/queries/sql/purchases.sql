
-- name: create-new-purchase<!
INSERT
INTO purchases (purchase_id, user_identifier, pack_id, styles_list, purchase_status)
VALUES (:purchase_id, :user_id, :pack_id, :styles_list, :purchase_status)
RETURNING
    purchase_id,
    user_identifier,
    pack_id,
    styles_list,
    purchase_status,
    created_at,
    updated_at;


-- name: update-purchase<!
UPDATE purchases
SET 
    purchase_status       = :purchase_status

WHERE
    purchase_id = :purchase_id
RETURNING updated_at;

-- name: get-purchase<!
SELECT *
FROM purchases
WHERE purchase_id = :purchase_id


-- name: get-all-purchases<!
SELECT *
FROM purchases



-- name: delete-purchase!
DELETE
FROM purchases
WHERE purchase_id = :purchase_id
