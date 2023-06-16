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
CREATE PROCEDURE update_step(
	IN p_id CHAR(36),
    IN p_description LONGTEXT,
    IN p_permissive_error smallint
)
BEGIN

		update step
        SET description = p_description, permissive_error = p_permissive_error
        where id = p_id;

END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS update_step;

