-- SHOW databases;
-- SHOW TABLES;
-- drop database rehab_app;
-- create database rehab_app;
-- use rehab_app;
CALL create_database();

CALL add_user(0, 'Vlad', 'Buga', 1, '123', 'vb@gmail.com');
select * from user;
CALL add_categories();
CALL add_exercise('mobilitatea bratului', 'inbunatatim mobilitatea bratului', 'shoulders', 'd656dc03-0771-11ee-be55-846993cbe512', 5, 1);
select * from exercises;
select * from photo;

CALL add_user(1, 'Iulia', 'Vrabie', 2, '123', 'iv@gmail.com');

-- 10.06 add program sau step?

