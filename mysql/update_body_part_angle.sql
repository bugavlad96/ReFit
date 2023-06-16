-- 	CREATE TABLE `body_part_angle`(
-- 		`id` CHAR(36) ,
-- 		`step_id` CHAR(36) ,
-- 		`bd_name` VARCHAR(255) ,
-- 		`angle` SMALLINT
-- 	);
-- 	ALTER TABLE
-- 		`body_part_angle` ADD PRIMARY KEY(`id`);
DELIMITER //
CREATE PROCEDURE update_body_part_angle (
	IN p_id char(36),
    IN p_angle SMALLINT
)
BEGIN

	update body_part_angle
        SET angle = p_angle
        where id = p_id;
	
-- 	INSERT INTO body_part_angle (id, step_id, bd_name, angle)
-- 		VALUES (unique_id, p_step_id, p_bd_name, p_angle);
    
END //
DELIMITER ;
-- select * from body_part_angle;
-- DROP PROCEDURE IF EXISTS update_body_part_angle;


