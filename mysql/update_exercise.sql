-- 	CREATE TABLE `exercise`(
-- 		`id` CHAR(36) ,
-- 		`name` VARCHAR(255) ,
-- 		`description` LONGTEXT ,
-- 		`photo_id` CHAR(36) ,
-- 		`category_name` VARCHAR(255) ,
-- 		`therapist_id` CHAR(36) ,
-- 		`max_reps` SMALLINT
-- 	);

-- ALTER TABLE exercise ADD name VARCHAR(255)
-- select * from exercise;

DELIMITER //
CREATE PROCEDURE update_exercise (
	IN p_id CHAR(36) ,
    IN p_name VARCHAR(255),
    IN p_description LONGTEXT,
    IN p_category_name VARCHAR(255),
    IN p_max_reps smallint
)
BEGIN

	UPDATE exercise
    SET name = p_name, description = p_description, category_name = p_category_name, max_reps = p_max_reps
    WHERE id = p_id;
        
END //
DELIMITER ;

-- call update_exercise('0b407b12-0b9a-11ee-8999-846993cbe512', 'cel mai tare exercitiu', 'o mare poveste', 'feet', 100);

-- select * from exercise;

-- DROP PROCEDURE IF EXISTS update_exercise;

