DELIMITER //
CREATE PROCEDURE add_bp_info(
	IN p_step_id char(36),
    IN p_bd_name varchar(255),
    IN p_angle SMALLINT
)
BEGIN
	DECLARE unique_id char(36);
    SET unique_id = UUID();
    
    INSERT into bp_info (id, step_id, bd_name, angle)
    VALUES (unique_id, p_step_id, p_bd_name, p_angle);

END //
DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_bd_info;
