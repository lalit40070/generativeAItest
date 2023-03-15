-- name: update_notification<!
UPDATE notifications
SET 
    is_allowed  = :is_allowed
WHERE
    user_id = :user_id

RETURNING updated_at;


-- name: get_notification<!
SELECT is_allowed, user_id
FROM notifications
WHERE 
     user_id= :user_id