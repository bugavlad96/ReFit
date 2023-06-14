-- 	CREATE TABLE `exercise`(
-- 		`id` CHAR(36) ,
-- 		`name` VARCHAR(255) ,
-- 		`description` LONGTEXT ,
-- 		`photo_id` CHAR(36) ,
-- 		`category_name` VARCHAR(255) ,
-- 		`therapist_id` CHAR(36) ,
-- 		`max_reps` SMALLINT
-- 	);


DELIMITER //
CREATE PROCEDURE add_exercise (
    IN p_name VARCHAR(255),
    IN p_description LONGTEXT,
    IN p_category_name VARCHAR(255),
    IN p_therapist_id CHAR(36),
    IN p_max_reps INT
)
BEGIN
	DECLARE unique_id_ex char(36);
    SET unique_id_ex = UUID();
	
	INSERT INTO exercise (id, name, description, category_name, therapist_id, max_reps)
		VALUES (unique_id_ex, p_name, p_description, p_category_name, p_therapist_id, p_max_reps);
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_exercise;
