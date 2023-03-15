-- name: create-images<!
INSERT
INTO images (type, url, style, user_identifier, purchase_id)
VALUES (:type, :url, :style, :user_id, :purchase_id)
RETURNING
    type,
    url,
    style,
    user_identifier,
    purchase_id,
    created_at,
    updated_at;