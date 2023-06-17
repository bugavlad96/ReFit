DELIMITER //

CREATE PROCEDURE add_patient_to_therapist(
	IN p_patient_id char(36),
    IN p_therapist_id char(36),
    IN p_default_program char(36)
)
BEGIN

	INSERT INTO patient_program (patient_id, therapist_id, program_id)
		VALUES (p_patient_id, p_therapist_id, p_default_program);
        
END //

DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_patient_to_therapist;