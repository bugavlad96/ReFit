
-- execute once when the databse is created call add_categories();
select * from category;

SELECT * FROM `user`;
/*type: therapist = 0 user = 1; 
  gender: male = 1, female = 2*/
CALL add_user(0, 'Vlad', 'Buga', 1, '123', 'vb@gmail.com');
CALL add_user(1, 'Iulia', 'Vrabie', 2, '123', 'iv@gmail.com');

select * from therapist;
select * from patient;

SELECT u.*, t.*
FROM user u
JOIN therapist t ON u.id = t.id
WHERE u.id = 'fa3b7a9b-06f9-11ee-9596-846993cbe512';

SELECT u.*, p.*
FROM user u
JOIN patient p ON u.id = p.id
WHERE u.id = 'd37be053-06fb-11ee-9596-846993cbe512';


-- INSERT INTO `category` (`id`, `name`, `description`) VALUES (UUID(), 'user_photo', 'user can upload photo');
select * from category;

-- INSERT INTO `photo` (`id`, `path`, `category_id`) VALUES (UUID(), 'VladBuga.jpg', '9e8cf99e-06e8-11ee-9596-846993cbe512');
select * from photo;
select * from exercises;




-- INSERT INTO `exercises` (`id`, `name`, `description`, `photo_id`, `category_id`, `therapist_id`, `max_count`, `exercise_order`) VALUES (uuid(), 'Exercise 1', 'Exercise 1 description', 'photo_id_1', 'category_id_1', 'therapist_id_1', 10, 1);
-- INSERT INTO `body_part` (`id`, `name`, `value`) VALUES ('body_part_id_1', 'Body Part 1', 100);
-- INSERT INTO `bp_info` (`id`, `step_id`, `bd_id`, `angle`) VALUES ('bp_info_id_1', 'step_id_1', 'body_part_id_1', 90);
-- INSERT INTO `programs` (`id`, `name`, `description`, `exercise_ids`, `photo_id`, `category_id`, `therapist_id`) VALUES ('program_id_1', 'Program 1', 'Program 1 description', 'exercise_id_1', 'photo_id_1', 'category_id_1', 'therapist_id_1');


-- INSERT INTO `step` (`id`, `exercise_id`, `photo`, `description`, `permissive_error`, `step_order`) VALUES ('step_id_1', 'exercise_id_1', 'photo_id_1', 'Step 1 description', 1, 1);
