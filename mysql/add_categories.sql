-- add categories
DELIMITER //
CREATE PROCEDURE add_categories()
BEGIN

	INSERT INTO category (name, description)
	VALUES ('hands','Exerciții pentru mâini');
	INSERT INTO category (name, description)
	VALUES ('shoulders','Exerciții pentru umeri');
    INSERT INTO category (name, description)
	VALUES ('hips','Exerciții pentru șolduri');
    INSERT INTO category (name, description)
	VALUES ('feet','Exerciții pentru picioare');
	INSERT INTO category (name, description)
	VALUES ('users','Poze utilizator');
    
END //
DELIMITER ;
-- select * from category;
-- call add_categories();
-- DROP PROCEDURE IF EXISTS add_categories;