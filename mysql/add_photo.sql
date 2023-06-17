DELIMITER //

CREATE PROCEDURE add_photo(
	IN p_category char(36),
    OUT p_generated_id char(36)
)
BEGIN

DECLARE unique_id char(36);
    SET unique_id = UUID();
    SET p_generated_id = unique_id;

	INSERT INTO photo(id, category_name)
    values (unique_id, p_category);

END //

DELIMITER ;
-- select * from photo;

-- DROP PROCEDURE IF EXISTS add_photo;