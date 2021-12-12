"""
Module for Block object
"""


class Block:
    """
    Class for Student
    """

    def __init__(self, fields):
        """
        :param fields:
        """
        self.Block_Id = fields.get("Block_Id")
        self.Start_Date = fields.get("Start_Date")
        self.End_Date = fields.get("End_Date")
        self.pg_year = fields.get("PG_YEAR")
        self.Work_Days_hol = fields.get("Work_Days_hol")
        self.Work_Days = fields.get("Work_Days")
        self.Days = fields.get("Days")

    def get_block(self):
        block = {
            "Block_Id": self.Block_Id,
            "Start_Date": self.Start_Date,
            "End_Date": self.End_Date,
            "Work_Days_hol": self.Work_Days_hol,
            "Work_Days": self.Work_Days,
            "Days": self.Days
        }
        return block
