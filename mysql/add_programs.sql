-- 	CREATE TABLE `programs`(
-- 		`id` CHAR(36) NOT NULL,
-- 		`name` VARCHAR(255) NOT NULL,
-- 		`description` LONGTEXT NOT NULL,
-- 		`photo_id` CHAR(36),
-- 		`category_name` VARCHAR(255) NOT NULL,
-- 		`therapist_id` CHAR(36) NOT NULL
-- 	);
-- 	ALTER TABLE
-- 		`programs` ADD PRIMARY KEY(`id`);

DELIMITER //
CREATE PROCEDURE add_program(
	IN p_name varchar(255),
    IN p_description longtext,
    IN p_category_name varchar(255),
    IN p_therapist_id char(36)
)
BEGIN
	DECLARE unique_id_program char(36);
    DECLARE unique_id_photo char(36);
    DECLARE path_to_photo VARCHAR(255);
    SET unique_id_program = UUID();
    SET unique_id_photo = UUID();
    SET path_to_photo = CONCAT('path/to/', p_name, '.jpg');

	INSERT INTO photo (id, path, category_name)
		values(unique_id_photo, path_to_photo, p_category_name);
        
	INSERT INTO programs(id, name, description, photo_id, category_name, therapist_id)
    values (unique_id_program, p_name, p_description, unique_id_photo, p_category_name, p_therapist_id);
        

END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_program;
