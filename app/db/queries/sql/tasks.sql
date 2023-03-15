
-- name: create-new-task<!
INSERT
INTO tasks (purchase_id, user_identifier, style_list, gender, pack_id, task_status)
VALUES (:purchase_id, :user_identifier, :style_list, :gender, :pack_id, :task_status)
RETURNING
    id,
    purchase_id,
    user_identifier,
    style_list,
    gender,
    pack_id,
    task_status,
    created_at,
    updated_at;

-- name: update-task<!
UPDATE tasks
SET 
    task_status       = :task_status

WHERE
    id = :task_id
RETURNING updated_at;

-- name: get_task_by_id<!
SELECT *
FROM tasks
WHERE id = :task_id


-- name: get-all-purchases<!
SELECT *
FROM purchases

-- name: get_pack_details<!
SELECT *
FROM packs
WHERE pack_id=:pack_id
LIMIT 1;

-- name: get_images_row<!
SELECT *
from images
WHERE type=:type AND user_identifier=:user_identifier AND purchase_id=:purchase_id


-- name: delete-purchase!
DELETE
FROM purchases
WHERE purchase_id = :purchase_id
