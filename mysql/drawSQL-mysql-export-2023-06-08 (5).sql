CREATE TABLE `therapist`(
    `id` CHAR(36) NOT NULL,
    `info` LONGTEXT NOT NULL
);
ALTER TABLE
    `therapist` ADD PRIMARY KEY(`id`);
CREATE TABLE `exercises`(
    `id` CHAR(36) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `photo_id` VARCHAR(255),
    `category_id` CHAR(36),
    `therapist_id` CHAR(36) NOT NULL,
    `max_count` INT NOT NULL,
    `exercise_order` SMALLINT NOT NULL,
    `program_id` CHAR(36)
);
ALTER TABLE
    `exercises` ADD PRIMARY KEY(`id`);
CREATE TABLE `photo`(
    `id` CHAR(36)  NOT NULL,
    `path` VARCHAR(255) NOT NULL,
    `category_id` CHAR(36)
);
ALTER TABLE
    `photo` ADD PRIMARY KEY(`id`);
CREATE TABLE `user`(
    `id` CHAR(36) NOT NULL,
    `type` SMALLINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `surname` VARCHAR(255) NOT NULL,
    `gender` SMALLINT NOT NULL,
    `pass` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `photo_id` VARCHAR(255)
);
ALTER TABLE
    `user` ADD PRIMARY KEY(`id`);
CREATE TABLE `body_part`(
    `id` CHAR(36) NOT NULL,
    `name` BIGINT NOT NULL,
    `value` BIGINT NOT NULL
);
ALTER TABLE
    `body_part` ADD PRIMARY KEY(`id`);
CREATE TABLE `bp_info`(
    `id` CHAR(36) NOT NULL,
    `step_id` CHAR(36) NOT NULL,
    `bd_id` CHAR(36) NOT NULL,
    `angle` BIGINT NOT NULL
);
ALTER TABLE
    `bp_info` ADD PRIMARY KEY(`id`);
CREATE TABLE `programs`(
    `id` CHAR(36) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `photo_id` CHAR(36),
    `category_id` CHAR(36),
    `therapist_id` CHAR(36) NOT NULL
);
ALTER TABLE
    `programs` ADD PRIMARY KEY(`id`);
CREATE TABLE `patient`(
    `id` CHAR(36) NOT NULL,
    `diagnosis` LONGTEXT,
    `program_ids` CHAR(36),
    `therapist_id` CHAR(36)
);
ALTER TABLE
    `patient` ADD PRIMARY KEY(`id`);
CREATE TABLE `category`(
    `id` CHAR(36) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL
);
ALTER TABLE
    `category` ADD PRIMARY KEY(`id`);
CREATE TABLE `step`(
    `id` CHAR(36) NOT NULL,
    `exercise_id` CHAR(36) NOT NULL,
    `photo` VARCHAR(255),
    `description` LONGTEXT NOT NULL,
    `permissive_error` SMALLINT NOT NULL,
    `step_order` SMALLINT NOT NULL
);
ALTER TABLE
    `step` ADD PRIMARY KEY(`id`);
ALTER TABLE
    `programs` ADD CONSTRAINT `programs_category_id_foreign` FOREIGN KEY(`category_id`) REFERENCES `category`(`id`);
ALTER TABLE
    `user` ADD CONSTRAINT `user_photo_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
ALTER TABLE
    `patient` ADD CONSTRAINT `patient_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
ALTER TABLE
    `bp_info` ADD CONSTRAINT `bp_info_bd_id_foreign` FOREIGN KEY(`bd_id`) REFERENCES `body_part`(`id`);
ALTER TABLE
    `step` ADD CONSTRAINT `step_exercise_id_foreign` FOREIGN KEY(`exercise_id`) REFERENCES `exercises`(`id`);
ALTER TABLE
    `therapist` ADD CONSTRAINT `therapist_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
ALTER TABLE
    `patient` ADD CONSTRAINT `patient_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
ALTER TABLE
    `photo` ADD CONSTRAINT `photo_category_id_foreign` FOREIGN KEY(`category_id`) REFERENCES `category`(`id`);
ALTER TABLE
    `exercises` ADD CONSTRAINT `exercises_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
ALTER TABLE
    `step` ADD CONSTRAINT `step_photo_foreign` FOREIGN KEY(`photo`) REFERENCES `photo`(`id`);
ALTER TABLE
    `bp_info` ADD CONSTRAINT `bp_info_step_id_foreign` FOREIGN KEY(`step_id`) REFERENCES `step`(`id`);
ALTER TABLE
    `exercises` ADD CONSTRAINT `exercises_program_id_foreign` FOREIGN KEY(`program_id`) REFERENCES `programs`(`id`);
ALTER TABLE
    `programs` ADD CONSTRAINT `programs_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
ALTER TABLE
    `patient` ADD CONSTRAINT `patient_program_ids_foreign` FOREIGN KEY(`program_ids`) REFERENCES `programs`(`id`);
ALTER TABLE
    `exercises` ADD CONSTRAINT `exercises_category_id_foreign` FOREIGN KEY(`category_id`) REFERENCES `category`(`id`);
ALTER TABLE
    `programs` ADD CONSTRAINT `programs_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
ALTER TABLE
    `exercises` ADD CONSTRAINT `exercises_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
    
    
    
-- Create the stored procedure
DELIMITER //
CREATE PROCEDURE insert_user (
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

-- add categories 
DELIMITER //
CREATE PROCEDURE add_categories()
BEGIN
	DECLARE unique_id_hands char(36);
    DECLARE unique_id_shoulders char(36);
    DECLARE unique_id_hips char(36);
    DECLARE unique_id_feet char(36);
    SET unique_id_hands = UUID();
    SET unique_id_shoulders = UUID();
    SET unique_id_hips = UUID();
    SET unique_id_feet = UUID();

    
	INSERT INTO category (id, name, description)
	VALUES (unique_id_hands, 'hands','hand related exercises');
	INSERT INTO category (id, name, description)
	VALUES (unique_id_shoulders, 'shoulders','shoulder related exercises');
    INSERT INTO category (id, name, description)
	VALUES (unique_id_hips, 'hips','hip related exercises');
    INSERT INTO category (id, name, description)
	VALUES (unique_id_feet, 'feet','feet related exercises');
END //
DELIMITER ;
-- DROP PROCEDURE IF EXISTS add_categories;



DELIMITER //
CREATE PROCEDURE insert_user (
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
