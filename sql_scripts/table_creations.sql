DROP DATABASE IF EXISTS schedular;

CREATE DATABASE schedular;

use schedular;

CREATE TABLE rotations (
	Rotation_Id int NOT NULL auto_increment,
    Rotation_Name varchar(255) NOT NULL,
    Can_Leave varchar(255) NOT NULL,
    On_Call varchar(255) NOT NULL,
    On_Site varchar(255) NOT NULL,
    Compliance int NOT NULL,
    Selective varchar(255) DEFAULT Null,
    PG_YEAR varchar(255) DEFAULT Null,
    primary key(Rotation_Id));

CREATE TABLE students (
	student_id int NOT NULL auto_increment,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    PG_YEAR varchar(255) NOT NULL,
    primary key(student_id));
    
CREATE TABLE blocks(
	Block_Id int NOT NULL auto_increment,
    Start_Date DATE DEFAULT NULL,
    End_Date DATE DEFAULT NULL,
    Work_Days_hol int DEFAULT NULL,
    Work_Days int default null,
    Days int default null,
    primary key(Block_Id));
    
	