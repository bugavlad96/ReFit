-- SHOW databases;
-- SHOW TABLES;
-- drop database rehab_app;
-- create database rehab_app;
-- use rehab_app;
-- CALL create_database();

-- CALL add_user(0, 'Vlad', 'Buga', 1, '123', 'vb@gmail.com');
-- select * from user;

-- CALL add_categories();
-- CALL add_bodyparts();
-- select * from body_part;
-- CALL add_exercise('mobilitatea bratului', 'inbunatatim mobilitatea bratului', 'shoulders', '05b11bfd-0788-11ee-93b8-846993cbe512', 5, 1);
-- select * from exercises;
-- select * from photo;
-- CALL add_user(1, 'Iulia', 'Vrabie', 2, '123', 'iv@gmail.com');


-- step 0
-- CALL add_step('39fc9837-0788-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 90 degrees', 10, 1);
-- step 1
-- CALL add_step('39fc9837-0788-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 120 degrees', 10, 2);
-- step 2
-- CALL add_step('39fc9837-0788-11ee-93b8-846993cbe512', 'shoulders', 'right_shoulder_180', 'raise your right shoulder at 180 degrees', 10, 3);

select * from step;
select * from body_part;
-- step 0 
CALL add_bp_info('a63f0220-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 90);
CALL add_bp_info('a63f0220-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);
-- step 1
CALL add_bp_info('a640693d-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 120);
CALL add_bp_info('a640693d-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);
-- step 2
CALL add_bp_info('a6416033-0788-11ee-93b8-846993cbe512', 'RIGHT_SHOULDER', 180);
CALL add_bp_info('a6416033-0788-11ee-93b8-846993cbe512', 'RIGHT_ELBOW', 180);


select *  from bp_info;



-- 10.06 add program sau step?

