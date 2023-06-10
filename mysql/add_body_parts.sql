-- add body_parts
DELIMITER //
CREATE PROCEDURE add_bodyparts()
BEGIN

	
	INSERT INTO body_part (name, value)
	VALUES ('RIGHT_ELBOW', '[12, 14, 16]');
    INSERT INTO body_part (name, value)
	VALUES ('LEFT_ELBOW', '[11, 13, 15]');
    INSERT INTO body_part (name, value)
	VALUES ('RIGHT_SHOULDER', '[11, 12, 14]');
    INSERT INTO body_part (name, value)
	VALUES ('LEFT_SHOULDER', '[12, 11, 13]');
    INSERT INTO body_part (name, value)
	VALUES ('LEFT_HIP', '[11, 23, 25]');
    INSERT INTO body_part (name, value)
	VALUES ('RIGHT_HIP', '[12, 24, 26]');
    INSERT INTO body_part (name, value)
	VALUES ('LEFT_KNEE', '[23, 25, 27]');
    INSERT INTO body_part (name, value)
	VALUES ('RIGHT_KNEE', '[24, 26, 28]');
    
    
    
    
END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_bodyparts;