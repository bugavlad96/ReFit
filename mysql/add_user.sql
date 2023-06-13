-- Create the stored procedure
DELIMITER //
-- type: 0 - Terapeut
-- 		 1 - Pacient
-- Genul: 1 - Barbat
--        2 - Femeie
--        3 - "prefer sa nu spun" 
CREATE PROCEDURE add_user (
    IN p_type SMALLINT,
    IN p_name VARCHAR(255),
    IN p_surname VARCHAR(255),
    IN p_gender SMALLINT,
    IN p_pass VARCHAR(255),
    IN p_email VARCHAR(255)
--     IN p_Therapist_information LONGTEXT,
--     IN p_diagnosis LONGTEXT
)
BEGIN
	DECLARE unique_id char(36);
    SET unique_id = UUID();


	-- Insert into user table
	INSERT INTO user (id, type, name, surname, gender, pass, email)
	VALUES (unique_id, p_type, p_name, p_surname, p_gender, p_pass, p_email);
	-- if user_type = to 0 then therapist
    IF p_type = 0 then
		-- Insert into therapist table
		INSERT INTO therapist (id)
		VALUES (unique_id);
    end if;
    -- if user_type = to 1 then patient
    IF p_type = 1 then
		-- Insert into therapist table
		INSERT INTO patient (id)
		VALUES (unique_id);
    end if;
END //
DELIMITER ;
-- DROP PROCEDURE IF EXISTS insert_therapist;
