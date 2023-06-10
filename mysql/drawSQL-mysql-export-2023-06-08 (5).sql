DELIMITER //
CREATE PROCEDURE create_database()
BEGIN

	CREATE TABLE `therapist`(
		`id` CHAR(36) NOT NULL,
		`info` LONGTEXT
	);
	ALTER TABLE
		`therapist` ADD PRIMARY KEY(`id`);
	CREATE TABLE `exercises`(
		`id` CHAR(36) NOT NULL,
		`name` VARCHAR(255) NOT NULL,
		`description` LONGTEXT NOT NULL,
		`photo_id` VARCHAR(255) NOT NULL,
		`category_name` VARCHAR(255) NOT NULL,
		`therapist_id` CHAR(36) NOT NULL,
		`max_count` SMALLINT,
		`exercise_order` SMALLINT,
		`program_id` CHAR(36) default NULL
	);
	ALTER TABLE
		`exercises` ADD PRIMARY KEY(`id`);
	CREATE TABLE `photo`(
		`id` CHAR(36) NOT NULL,
		`path` VARCHAR(255) NOT NULL,
		`category_name` VARCHAR(255) NOT NULL
	);
	ALTER TABLE
		`photo` ADD PRIMARY KEY(`id`);
	CREATE TABLE `user`(
		`id` CHAR(36) NOT NULL,
		`type` SMALLINT(16) NOT NULL,
		`name` VARCHAR(255) NOT NULL,
		`surname` VARCHAR(255) NOT NULL,
		`gender` SMALLINT(16) NOT NULL,
		`pass` VARCHAR(255) NOT NULL,
		`email` VARCHAR(255) NOT NULL,
		`photo_id` VARCHAR(255)
	);
	ALTER TABLE
		`user` ADD PRIMARY KEY(`id`);
	CREATE TABLE `body_part`(
		`name` VARCHAR(255) NOT NULL,
		`value` VARCHAR(255) NOT NULL
	);
	ALTER TABLE
		`body_part` ADD PRIMARY KEY(`name`);
	CREATE TABLE `bp_info`(
		`id` CHAR(36) NOT NULL,
		`step_id` CHAR(36) NOT NULL,
		`bd_name` VARCHAR(255) NOT NULL,
		`angle` SMALLINT NOT NULL
	);
	ALTER TABLE
		`bp_info` ADD PRIMARY KEY(`id`);
	CREATE TABLE `programs`(
		`id` CHAR(36) NOT NULL,
		`name` VARCHAR(255) NOT NULL,
		`description` LONGTEXT NOT NULL,
		`photo_id` CHAR(36),
		`category_name` VARCHAR(255) NOT NULL,
		`therapist_id` CHAR(36) NOT NULL
	);
	ALTER TABLE
		`programs` ADD PRIMARY KEY(`id`);
	CREATE TABLE `patient`(
		`id` CHAR(36) NOT NULL,
		`diagnosis` LONGTEXT,
		`program_id` CHAR(36),
		`therapist_id` CHAR(36)
	);
	ALTER TABLE
		`patient` ADD PRIMARY KEY(`id`);
	CREATE TABLE `category`(
		`name` VARCHAR(255) NOT NULL,
		`description` LONGTEXT NOT NULL
	);
	ALTER TABLE
		`category` ADD PRIMARY KEY(`name`);
	CREATE TABLE `step`(
		`id` CHAR(36) NOT NULL,
		`exercise_id` CHAR(36) NOT NULL,
		`photo_id` CHAR(36) NOT NULL,
		`description` LONGTEXT NOT NULL,
		`permissive_error` SMALLINT NOT NULL DEFAULT 10,
		`step_order` SMALLINT NOT NULL
	);
	ALTER TABLE
		`step` ADD PRIMARY KEY(`id`);
	ALTER TABLE
		`user` ADD CONSTRAINT `user_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`patient` ADD CONSTRAINT `patient_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
	ALTER TABLE
		`programs` ADD CONSTRAINT `programs_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	ALTER TABLE
		`exercises` ADD CONSTRAINT `exercises_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	ALTER TABLE
		`bp_info` ADD CONSTRAINT `bp_info_bd_name_foreign` FOREIGN KEY(`bd_name`) REFERENCES `body_part`(`name`);
	ALTER TABLE
		`step` ADD CONSTRAINT `step_exercise_id_foreign` FOREIGN KEY(`exercise_id`) REFERENCES `exercises`(`id`);
	ALTER TABLE
		`therapist` ADD CONSTRAINT `therapist_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
	ALTER TABLE
		`patient` ADD CONSTRAINT `patient_user_id_foreign` FOREIGN KEY(`id`) REFERENCES `user`(`id`);
	ALTER TABLE
		`exercises` ADD CONSTRAINT `exercises_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`photo` ADD CONSTRAINT `photo_category_name_foreign` FOREIGN KEY(`category_name`) REFERENCES `category`(`name`);
	ALTER TABLE
		`step` ADD CONSTRAINT `step_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`bp_info` ADD CONSTRAINT `bp_info_step_id_foreign` FOREIGN KEY(`step_id`) REFERENCES `step`(`id`);
	ALTER TABLE
		`exercises` ADD CONSTRAINT `exercises_program_id_foreign` FOREIGN KEY(`program_id`) REFERENCES `programs`(`id`);
	ALTER TABLE
		`programs` ADD CONSTRAINT `programs_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
	ALTER TABLE
		`patient` ADD CONSTRAINT `patient_program_ids_foreign` FOREIGN KEY(`program_ids`) REFERENCES `programs`(`id`);
	ALTER TABLE
		`programs` ADD CONSTRAINT `programs_photo_id_foreign` FOREIGN KEY(`photo_id`) REFERENCES `photo`(`id`);
	ALTER TABLE
		`exercises` ADD CONSTRAINT `exercises_therapist_id_foreign` FOREIGN KEY(`therapist_id`) REFERENCES `therapist`(`id`);
		
	END //
DELIMITER ;