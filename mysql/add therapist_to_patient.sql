DELIMITER //

CREATE PROCEDURE add_therapist_to_patient(
	IN therapist_id char(36),
    IN p_pacient_id char(36),
    IN p_diagnosis longtext
)
BEGIN
	UPDATE patient
	SET therapist_id = therapist_id, diagnosis = p_diagnosis
	WHERE id = p_pacient_id;


END //

DELIMITER ;

-- DROP PROCEDURE IF EXISTS add_therapist_to_patient;