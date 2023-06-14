DELIMITER //
CREATE PROCEDURE create_database()
BEGIN
	CREATE TABLE `therapist`(
		`id` CHAR(36),
		`info` LONGTEXT
	);
	ALTER TABLE
		`therapist` ADD PRIMARY KEY(`id`);
	CREATE TABLE `patient_program`(
		`patient_id` CHAR(36) ,
		`therapist_id` CHAR(36) ,
		`program_id` CHAR(36)
	);
	ALTER TABLE
		`patient_program` ADD PRIMARY KEY(`patient_id`, `therapist_id`, `program_id`);
    CREATE TABLE `exercise`(
		`id` CHAR(36) ,
		`description` LONGTEXT ,
		`photo_id` CHAR(36) ,
		`category_name` VARCHAR(255) ,
		`therapist_id` CHAR(36) ,
		`max_reps` SMALLINT
	);
	ALTER TABLE
		`exercise` ADD PRIMARY KEY(`id`);
	CREATE TABLE `photo`(
		`id` CHAR(36) ,
		`category_name` VARCHAR(255)
	);
	ALTER TABLE
		`photo` ADD PRIMARY KEY(`id`);
	CREATE TABLE `user`(
		`id` CHAR(36) ,
		`type` SMALLINT ,
		`name` VARCHAR(255) ,
		`surname` VARCHAR(255) ,
		`gender` SMALLINT ,
		`pass` VARCHAR(255) ,
		`email` VARCHAR(255) ,
		`photo_id` VARCHAR(255)
	);
	ALTER TABLE
		`user` ADD PRIMARY KEY(`id`);
	CREATE TABLE `exercise_to_prog`(
		`program_id` CHAR(36) ,
		`exercise_id` CHAR(36)
	);
	ALTER TABLE
		`exercise_to_prog` ADD PRIMARY KEY(`program_id`, `exercise_id`);
        
	CREATE TABLE `body_part`(
		`name` VARCHAR(255) ,
		`value` VARCHAR(255)
	);
	ALTER TABLE
		`body_part` ADD PRIMARY KEY(`name`);
        
	CREATE TABLE `body_part_angle`(
		`id` CHAR(36) ,
		`step_id` CHAR(36) ,
		`bd_name` VARCHAR(255) ,
		`angle` SMALLINT
	);
	ALTER TABLE
		`body_part_angle` ADD PRIMARY KEY(`id`);
        
	CREATE TABLE `program`(
		`id` CHAR(36) ,
		`name` VARCHAR(255) ,
		`description` LONGTEXT ,
		`photo_id` CHAR(36) ,
		`category_name` VARCHAR(255) ,
		`therapist_id` CHAR(36)
	);
	ALTER TABLE
		`program` ADD PRIMARY KEY(`id`);
        
	CREATE TABLE `patient`(
		`id` CHAR(36) ,
		`diagnosis` LONGTEXT
	);
	ALTER TABLE
		`patient` ADD PRIMARY KEY(`id`);
        
	CREATE TABLE `category`(
		`name` VARCHAR(255) ,
		`description` LONGTEXT
	);
	ALTER TABLE
		`category` ADD PRIMARY KEY(`name`);
        
	CREATE TABLE `step`(
		`id` CHAR(36) ,
		`exercise_id` CHAR(36) ,
		`photo_id` CHAR(36) ,
		`description` LONGTEXT ,
		`permissive_error` SMALLINT ,
		`step_order` SMALLINT
	);
	ALTER TABLE
		`step` ADD PRIMARY KEY(`id`);
        
	ALTER TABLE
		`user` ADD CONSTRAINT `user_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`therapist` ADD CONSTRAINT `therapist_to_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
	ALTER TABLE
		`patient` ADD CONSTRAINT `patient_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
	ALTER TABLE
		`exercise_to_prog` ADD CONSTRAINT `exercise_to_prog_to_program_id_foreign` FOREIGN KEY(`program_id`) REFERENCES `program`(`id`);
	ALTER TABLE
		`exercise_to_prog` ADD CONSTRAINT `exercise_to_prog_to_exercise_id_foreign` FOREIGN KEY(`exercise_id`) REFERENCES `exercise`(`id`);
	ALTER TABLE
		`body_part_angle` ADD CONSTRAINT `body_part_angle_bd_name_foreign` FOREIGN KEY(`bd_name`) REFERENCES `body_part`(`name`);
	ALTER TABLE
		`body_part_angle` ADD CONSTRAINT `body_part_angle_step_id_foreign` FOREIGN KEY(`step_id`) REFERENCES `step`(`id`);
	ALTER TABLE
		`program` ADD CONSTRAINT `program_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	ALTER TABLE
		`program` ADD CONSTRAINT `program_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
	ALTER TABLE
		`program` ADD CONSTRAINT `program_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`patient_program` ADD CONSTRAINT `patient_program_to_program_id_foreign` FOREIGN KEY(`program_id`) REFERENCES `program`(`id`);
	ALTER TABLE
		`patient_program` ADD CONSTRAINT `patient_program_t_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
	ALTER TABLE
		`patient_program` ADD CONSTRAINT `patient_program_patient_id_foreign` FOREIGN KEY(`patient_id`) REFERENCES `patient`(`id`);
	ALTER TABLE
		`exercise` ADD CONSTRAINT `exercise_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	ALTER TABLE
		`exercise` ADD CONSTRAINT `exercise_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`exercise` ADD CONSTRAINT `exercise_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
	ALTER TABLE
		`step` ADD CONSTRAINT `step_exercise_id_foreign` FOREIGN KEY(`exercise_id`) REFERENCES `exercise`(`id`);
	ALTER TABLE
		`step` ADD CONSTRAINT `step_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`photo` ADD CONSTRAINT `photo_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	END //
DELIMITER ;
