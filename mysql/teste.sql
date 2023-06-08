
SHOW databases;
drop database rehab_app;
create database rehab_app;
use rehab_app;
SELECT * FROM `user`;
/*type: dorctor = 1 user = 0; gender: male = 1, female = 0*/
INSERT INTO `category` (`id`, `name`, `description`) VALUES (UUID(), 'user_photo', 'user can upload photo');
select * from category;
INSERT INTO `photo` (`id`, `path`, `category_id`) VALUES (UUID(), '/path/to/user1.jpg', 'd24bf2ab-0634-11ee-9596-846993cbe512');
select * from photo;
-- for type 1 means therapist, gender male = 1
INSERT INTO `user` (`id`, `type`, `name`, `surname`, `gender`, `pass`, `email`, `photo`) VALUES (UUID(), 1, 'Vlad', 'Buga', 1, 'password123', 'vlad.buga@example.com', 'fbc74e2f-0634-11ee-9596-846993cbe512');
select * from user;
INSERT INTO `therapist` (`id`, `info`, `patient_ids`) VALUES (5a47a308-0635-11ee-9596-846993cbe512, 'specialized in all body parts', 'patient_id_1');
INSERT INTO `pacient` (`id`, `diagnosis`, `program_ids`) VALUES (UUID(), 'Diagnosis 1', 'program_id_1');
INSERT INTO `therapist` (`id`, `info`, `patient_ids`) VALUES (uuid(), 'Therapist info 1', 'patient_id_1');
INSERT INTO `exercises` (`id`, `name`, `description`, `photo_id`, `category_id`, `therapist_id`, `max_count`, `exercise_order`) VALUES (uuid(), 'Exercise 1', 'Exercise 1 description', 'photo_id_1', 'category_id_1', 'therapist_id_1', 10, 1);


INSERT INTO `body_part` (`id`, `name`, `value`) VALUES ('body_part_id_1', 'Body Part 1', 100);
INSERT INTO `bp_info` (`id`, `step_id`, `bd_id`, `angle`) VALUES ('bp_info_id_1', 'step_id_1', 'body_part_id_1', 90);
INSERT INTO `programs` (`id`, `name`, `description`, `exercise_ids`, `photo_id`, `category_id`, `therapist_id`) VALUES ('program_id_1', 'Program 1', 'Program 1 description', 'exercise_id_1', 'photo_id_1', 'category_id_1', 'therapist_id_1');


INSERT INTO `step` (`id`, `exercise_id`, `photo`, `description`, `permissive_error`, `step_order`) VALUES ('step_id_1', 'exercise_id_1', 'photo_id_1', 'Step 1 description', 1, 1);
