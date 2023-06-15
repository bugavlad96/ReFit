	-- CREATE TABLE `step`(
-- 		`id` CHAR(36) NOT NULL,
-- 		`exercise_id` CHAR(36) NOT NULL,
-- 		`photo_id` CHAR(36) NOT NULL,
-- 		`description` LONGTEXT NOT NULL,
-- 		`permissive_error` SMALLINT NOT NULL DEFAULT 10,
-- 		`step_order` SMALLINT NOT NULL
-- 	);
-- 	ALTER TABLE
-- 		`step` ADD PRIMARY KEY(`id`);

-- 	CREATE TABLE `bp_info`(
-- 		`id` CHAR(36) NOT NULL,
-- 		`step_id` CHAR(36) NOT NULL,
-- 		`bd_name` VARCHAR(255) NOT NULL,
-- 		`angle` SMALLINT NOT NULL
-- 	);
-- 	ALTER TABLE
-- 		`bp_info` ADD PRIMARY KEY(`id`);


DELIMITER //
CREATE PROCEDURE add_step(
    p_exercise_id CHAR(36),
 --    p_photo_name CHAR(36),
    p_description LONGTEXT,
    p_permissive_error smallint,
    p_step_order SMALLINT
    
)
BEGIN
	DECLARE unique_id char(36);
 --    DECLARE unique_id_photo char(36);
--     DECLARE path_to_photo VARCHAR(255);
    SET unique_id = UUID();
 --    SET unique_id_photo = UUID();
--     SET path_to_photo = CONCAT('path/to/', p_photo_name, '.jpg');

	-- INSERT INTO photo (id, path, category_name)
-- 		values(unique_id_photo, path_to_photo, p_exercise_category);
-- 	
		INSERT INTO step (id, exercise_id, description, permissive_error, step_order)
		VALUES (unique_id, p_exercise_id, p_description, p_permissive_error, p_step_order);
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_step;

