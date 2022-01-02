CREATE TABLE rotations (
	Rotation_Id int NOT NULL auto_increment,
    Rotation_Name varchar(255) NOT NULL,
    Can_Leave varchar(255) NOT NULL,
    On_Call varchar(255) NOT NULL,
    On_Site varchar(255) NOT NULL,
    Compliance int NOT NULL,
    Capacity_Min int Not Null,
    Capacity_Max int Not Null,
    PG_YEAR varchar(255) DEFAULT Null,
    primary key(Rotation_Id));

INSERT INTO rotations (Rotation_Name, Can_Leave, On_Call, On_Site, Compliance, Capacity_Min, Capacity_Max, PG_YEAR)
	Values("Medicine", "Very Unlikely", "No", "Yes", 3, 2, 4, "PYG1-CORE"),
    ("Intensive Care Unit", "Very Unlikely", "No", "Yes", 1, 0, 2, "PYG1-CORE"),
    ("7W", "Unlikely", "Yes", "Yes", 2, 4, 6, "PYG1-CORE"),
    ("PCLS", "Likely", "Yes", "Yes", 1,2,4, "PYG1-CORE"),
    ("Neurology (VA)", "Likely", "Yes", "No", 1, 1,2, "PYG1-CORE"),
    ("Geriatrics", "Likely", "Yes", "Yes", 1,0,2, "PYG1-CORE"),
    ("Addictions", "Likely", "Yes", "No", 1,0,2, "PYG1-CORE"),
    ("Selective", "Likely", "Yes", "Maybe", 3,0,10, "PYG1-CORE");
