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
    IN p_exercise_id CHAR(36),
    IN p_description LONGTEXT,
    IN p_permissive_error smallint,
    IN p_step_order SMALLINT,
    IN p_photo_id CHAR(36),
    IN p_category_name CHAR(36), 
	OUT p_generated_id CHAR(36)
    
)
BEGIN
	DECLARE unique_id char(36);
    SET unique_id = UUID();
    set p_generated_id = unique_id;

		INSERT INTO step (id, exercise_id, description, permissive_error, step_order, photo_id)
		VALUES (unique_id, p_exercise_id, p_description, p_permissive_error, p_step_order, p_photo_id);
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_step;

