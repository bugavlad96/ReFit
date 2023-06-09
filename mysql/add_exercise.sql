-- CREATE TABLE `exercises`(
--     `id` CHAR(36) NOT NULL,
--     `name` VARCHAR(255) NOT NULL,
--     `description` LONGTEXT NOT NULL,
--     `photo_id` VARCHAR(255) NOT NULL,
--     `category_name` VARCHAR(255) NOT NULL,
--     `therapist_id` CHAR(36) NOT NULL,
--     `max_count` SMALLINT,
--     `exercise_order` SMALLINT,
--     `program_id` CHAR(36)
-- );
-- CREATE TABLE `photo`(
--     `id` CHAR(36) NOT NULL,
--     `path` VARCHAR(255) NOT NULL,
--     `category_name` VARCHAR(255) NOT NULL
-- );


DELIMITER //
CREATE PROCEDURE add_exercise (
    IN p_name VARCHAR(255),
    IN p_description LONGTEXT,
    -- IN p_photo_id CHAR(36),
    IN p_category_name VARCHAR(255),
    IN p_therapist_id CHAR(36),
    IN p_max_count INT,
    IN p_exercise_order SMALLINT
)
BEGIN
	DECLARE unique_id_ex char(36);
    DECLARE unique_id_photo char(36);
    DECLARE path_to_photo VARCHAR(255);
    SET unique_id_ex = UUID();
    SET unique_id_photo = UUID();
    SET path_to_photo = CONCAT('path/to', p_name, '.jpg');

	INSERT INTO photo (id, path, category_name)
		values(unique_id_photo, path_to_photo, p_category_name);
	
		INSERT INTO exercises (id, name, description, photo_id, category_name, therapist_id, max_count, exercise_order)
		VALUES (unique_id_ex, p_name, p_description, unique_id_photo, p_category_name, p_therapist_id, p_max_count, p_exercise_order);
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_exercise;

