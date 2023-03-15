-- name: get-user-by-email^
SELECT id,
       username,
       identifier,
       email,
       salt,
       hashed_password,
       device_id,
       fcm_token, 
       is_subscribed,
       auth_type,
       id_for_apple,
       is_active,
       created_at,
       updated_at
FROM users
WHERE email = :email
LIMIT 1;


-- name: get-user-by-username^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       device_id,
       fcm_token, 
       is_subscribed,
       auth_type,
       is_active,
       created_at,
       updated_at
FROM users
WHERE username = :username
LIMIT 1;


-- name: get-user-by-user_id^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       device_id,
       fcm_token, 
       is_subscribed,
       auth_type,
       is_active,
       created_at,
       updated_at
FROM users
WHERE id = :id
LIMIT 1;


-- name: get-user-by-user_identifier^
SELECT id,
       username,
       identifier,
       email,
       salt,
       hashed_password,
       device_id,
       fcm_token, 
       is_subscribed,
       auth_type,
       is_active,
       created_at,
       updated_at
FROM users
WHERE identifier = :user_identifier
LIMIT 1;



-- name: get-user-by-apple_id^
SELECT id,
       username,
       identifier,
       email,
       salt,
       hashed_password,
       device_id,
       fcm_token, 
       is_subscribed,
       auth_type,
       id_for_apple,
       is_active,
       created_at,
       updated_at
FROM users
WHERE id_for_apple = :id_for_apple
LIMIT 1;


-- name: create-new-user<!
INSERT INTO users (username, identifier, email, salt, device_id, fcm_token, hashed_password, is_subscribed, auth_type, id_for_apple)
VALUES (:username, :identifier, :email, :salt, :device_id, :fcm_token, :hashed_password, :is_subscribed, :auth_type, :id_for_apple)
RETURNING
    id, device_id, fcm_token, auth_type, id_for_apple, created_at, updated_at;


-- name: update-user-by-username<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    salt            = :new_salt,
    hashed_password = :new_password,
    device_id       = :device_id,
    fcm_token       = :fcm_token,
    is_subscribed   = :is_subscribed,
    auth_type       = :auth_type,
WHERE username = :username
RETURNING
    updated_at;


-- name: get-user-tasks<!
SELECT *
FROM tasks
WHERE user_identifier = :user_identifier

-- name: get_user_task_images<!
SELECT 
    url, 
    style

FROM images
WHERE user_identifier= :user_identifier 
AND purchase_id=:purchase_id 
AND type=:type


-- name: get_pack_details<!
SELECT pack_name, images_per_pack
FROM packs
WHERE pack_id =:pack_id


-- name: create_notification<!
INSERT INTO notifications(is_allowed, user_id)
VALUES (:is_allowed, :user_id)
RETURNING is_allowed;


-- name: delete_user<!
DELETE 
FROM users
where identifier = :identifier
