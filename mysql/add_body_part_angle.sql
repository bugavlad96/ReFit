-- 	CREATE TABLE `body_part_angle`(
-- 		`id` CHAR(36) ,
-- 		`step_id` CHAR(36) ,
-- 		`bd_name` VARCHAR(255) ,
-- 		`angle` SMALLINT
-- 	);
-- 	ALTER TABLE
-- 		`body_part_angle` ADD PRIMARY KEY(`id`);
DELIMITER //
CREATE PROCEDURE add_body_part_angle (
    IN p_step_id CHAR(36),
    IN p_bd_name VARCHAR(255),
    IN p_angle SMALLINT

)
BEGIN
	DECLARE unique_id char(36);
    SET unique_id = UUID();
	
	INSERT INTO body_part_angle (id, step_id, bd_name, angle)
		VALUES (unique_id, p_step_id, p_bd_name, p_angle);
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_body_part_angle;


