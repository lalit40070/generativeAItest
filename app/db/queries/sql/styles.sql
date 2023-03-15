
-- name: create_new_style<!
INSERT
INTO style (style_id, name, prompt_positive, prompt_negative, seed, type, gender, sample_image, diffusion_version)
VALUES (:style_id, :name, :prompt_positive, :prompt_negative, :seed, :type, :gender, :sample_image, :diffusion_version)
RETURNING
    style_id,
    name,
    prompt_positive,
    prompt_negative,
    seed,
    type,
    gender,
    sample_image,
    diffusion_version,
    created_at,
    updated_at;



-- name: update-style<!
UPDATE style
SET 
    name = :name,
    prompt_positive = :prompt_positive,
    prompt_negative = :prompt_negative,
    seed = :seed,
    type = :type,
    gender = :gender,
    sample_image = :sample_image,
    diffusion_version = :diffusion_version

WHERE
    style_id = :style_id
RETURNING updated_at;



-- name: get-style<!
SELECT *
FROM style
WHERE style_id = :style_id


-- name: delete-style!
DELETE
FROM style
WHERE style_id = :style_id