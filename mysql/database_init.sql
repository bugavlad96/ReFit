-- SHOW databases;
-- SHOW TABLES;
-- drop database refit;
-- create database refit;
-- use refit;
-- CALL create_database();
select * from exercise;
-- CALL add_user(0, 'Vlad', 'Buga', 1, '123', 'vb@gmail.com');
-- 0a7d8329-0b84-11ee-8999-846993cbe512 
-- select * from user;
-- select * from programs;
select * from step where exercise_id = '4d314208-0b84-11ee-8999-846993cbe512';
-- CALL add_categories();
-- CALL add_bodyparts();
-- select * from body_part;
-- CALL add_exercise('mobilitatea umarului', 'inbunatatim mobilitatatii umarului', 'shoulders', 'b49dd32f-0a1d-11ee-93b8-846993cbe512', 5);
-- CALL add_exercise('mobilitatea cotului', 'inbunatatim mobilitatatii cotului', 'hands', 'b49dd32f-0a1d-11ee-93b8-846993cbe512', 5);
-- CALL add_exercise('mobilitatea cotului', 'inbunatatim mobilitatatii cotului 2', 'hands', 'b49dd32f-0a1d-11ee-93b8-846993cbe512', 5);
-- CALL add_exercise('mobilitatea cotului', 'inbunatatim mobilitatatii cotului 3', 'hands', 'b49dd32f-0a1d-11ee-93b8-846993cbe512', 5);
-- select * from exercise;
-- select * from program; -- 29997d4a-0a85-11ee-a04a-846993cbe512 facut de b8 Vlad 
-- select * from user; -- b8
-- select * from program
-- call add_program('Vlad Program', 'very good program',  'shoulders', 'b49dd32f-0a1d-11ee-93b8-846993cbe512','265003a5-0a20-11ee-93b8-846993cbe512','6f919689-0ac4-11ee-a04a-846993cbe512','fc667798-0a1f-11ee-93b8-846993cbe512')
-- select * from exercise_to_prog;
-- select * from photo;
-- CALL add_user(1, 'Iulia', 'Vrabie', 2, '123', 'iv@gmail.com');
-- DELETE FROM exercise_to_prog;
select * from exercise;
select * from step;
select * from body_part;
-- step 0
-- CALL add_step('961983ba-0a0b-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 90 degrees', 10, 1);
-- step 1
-- CALL add_step('961983ba-0a0b-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 120 degrees', 10, 2);
-- step 2
-- CALL add_step('961983ba-0a0b-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 180 degrees', 10, 3);

-- select * from step;
-- select * from body_part;
-- -- step 0 
-- CALL add_bp_info('a63f0220-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 90);
-- CALL add_bp_info('a63f0220-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);
-- -- step 1
-- CALL add_bp_info('a640693d-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 120);
-- CALL add_bp_info('a640693d-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);
-- -- step 2
-- CALL add_bp_info('a6416033-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 180);
-- CALL add_bp_info('a6416033-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);
use refit;
select * from exercise;

-- select *  from bp_info;
-- select * from category;
-- select * from therapist;
-- CALL add_program('shoulder plane mobility ex', 'one is testing and extending the range of shoulder mobility', 'shoulders', 'b49dd32f-0a1d-11ee-93b8-846993cbe512');
-- CALL add_program('shoulder vertical mobility ex', 'one is testing and extending the range of shoulder mobility', 'shoulders', '4cad0129-0a85-11ee-a04a-846993cbe512');
-- select * from program;

-- select * from user;
-- CALL add_therapist_to_patient(
-- 	'05b11bfd-0788-11ee-93b8-846993cbe512',
--     '450467f2-0788-11ee-93b8-846993cbe512',
-- 	'bad right shoulder'
--     );
-- select * from patient;
delete from exercise_to_prog;
-- select * from programs;
-- CALL add_program_to_patient(
-- 	'bdcd7711-078b-11ee-93b8-846993cbe512',
--     '450467f2-0788-11ee-93b8-846993cbe512');
select * from user;
select * from exercise where name = 'tralala tralala';
select * from body_part_angle where step_id = '1d09112c-0b6f-11ee-8999-846993cbe512';
select * from step;
-- delete from body_part_angle;
-- delete from step;
-- delete from exercise;


-- associate a program to a patient 