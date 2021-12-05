# ("Medicine", "Intensive Care Unit", "7W", "PCLS", "Neurology (VA)", "Geriatrics", "Addictions")
INSERT INTO rotations (Rotation_Name, Can_Leave, On_Call, On_Site, PG_YEAR)
	Values("Medicine", "Very Unlikely", "No", "Yes", "PYG1-CORE"),
    ("Intensive Care Unit", "Very Unlikely", "No", "Yes", "PYG1-CORE"),
    ("7W", "Unlikely", "Yes", "Yes", "PYG1-CORE"),
    ("PCLS", "Likely", "Yes", "Yes", "PYG1-CORE"),
    ("Neurology (VA)", "Likely", "Yes", "No", "PYG1-CORE"),
    ("Geriatrics", "Likely", "Yes", "Yes", "PYG1-CORE"),
    ("Addictions", "Likely", "Yes", "No", "PYG1-CORE");

select * from rotations;
select * from blocks;
select * from students;

INSERT INTO blocks (Start_Date, End_Date, Work_Days_hol, Work_Days, Days)
	Values(20210701, 20210725, 17, 17, 24),
	(20210726, 20210822, 20, 20, 27),
    (20210821, 20210919, 19, 20, 27),
    (20210920, 20211017, 19, 20, 27),
    (20211018, 20211114, 19, 20, 27),
    (20211115, 20211212, 19, 20, 27),
    (20211213, 20220116, 23, 25, 34),
    (20220117, 20220213, 19, 20, 27),
    (20220214, 20220313, 19, 20, 27),
    (20220314, 20220410, 20, 20, 27),
    (20220411, 20220508, 20, 20, 27),
    (20220509, 20220605, 19, 20, 27),
    (20220606, 20220630, 19, 19, 24)