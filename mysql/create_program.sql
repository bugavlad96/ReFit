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

-- CREATE TABLE `exercise_to_prog`(
-- 		`program_id` CHAR(36) ,
-- 		`exercise_id` CHAR(36)
-- 	);
-- 	ALTER TABLE
-- 		`exercise_to_prog` ADD PRIMARY KEY(`program_id`, `exercise_id`);

DELIMITER //
CREATE PROCEDURE add_program(
	IN p_name varchar(255),
    IN p_description longtext,
    IN p_category_name varchar(255),
    IN p_therapist_id char(36),
    OUT p_generated_id CHAR(36)
    
)
BEGIN
	DECLARE unique_id_program char(36);
    SET unique_id_program = UUID();
    SET p_generated_id = unique_id_program;

	INSERT INTO program(id, name, description, category_name, therapist_id)
    values (unique_id_program, p_name, p_description, p_category_name, p_therapist_id);
            
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_program;
