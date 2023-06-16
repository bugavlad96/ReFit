-- 	CREATE TABLE `program`(
-- 		`id` CHAR(36) ,
-- 		`name` VARCHAR(255) ,
-- 		`description` LONGTEXT ,
-- 		`photo_id` CHAR(36) ,
-- 		`category_name` VARCHAR(255) ,
-- 		`therapist_id` CHAR(36)
-- 	);
-- 	ALTER TABLE
-- 		`program` ADD PRIMARY KEY(`id`);
DELIMITER //
CREATE PROCEDURE update_program (
	IN p_id char(36),
    IN p_name VARCHAR(255),
	IN p_description LONGTEXT,
    IN p_category_name VARCHAR(255)    
)
BEGIN

	update program
        SET name = p_name, description = p_description, category_name = p_category_name
        where id = p_id;
	
END //
DELIMITER ;
-- select * from body_part_angle;
-- DROP PROCEDURE IF EXISTS update_body_part_angle;


