-- add categories
DELIMITER //
CREATE PROCEDURE add_categories()
BEGIN

	INSERT INTO category (name, description)
	VALUES ('hands','hand related exercises');
	INSERT INTO category (name, description)
	VALUES ('shoulders','shoulder related exercises');
    INSERT INTO category (name, description)
	VALUES ('hips','hip related exercises');
    INSERT INTO category (name, description)
	VALUES ('feet','feet related exercises');
	INSERT INTO category (name, description)
	VALUES ('user','user photo');
    
END //
DELIMITER ;
-- DROP PROCEDURE IF EXISTS add_categories;