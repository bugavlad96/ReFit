DELIMITER //

CREATE PROCEDURE add_program_to_patient(
	IN p_program_id char(36),
    IN p_pacient_id char(36)
)
BEGIN
	UPDATE patient
    -- daca resetezi baza de date aici vei avea eroare schima program_ids pe program_id
	SET program_ids = p_program_id
	WHERE id = p_pacient_id;


END //

DELIMITER ;


-- DROP PROCEDURE IF EXISTS add_program_to_patient;