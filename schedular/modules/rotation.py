"""
Module for Rotation object
"""


class Rotation:
    """
    Class for Rotation
    """

    def __init__(self, fields):
        """
        :param fields:
        """
        self.rotation_id = fields.get("Rotation_Id")
        self.rotation_name = fields.get("Rotation_Name")
        self.can_leave = fields.get("Can_Leave")
        self.on_call = fields.get("On_Call")
        self.on_site = fields.get("On_Site")
        self.capacity_min = fields.get("Capacity_Min")
        self.capacity_max = fields.get("Capacity_Max")
        self.compliance = fields.get("Compliance")
        self.pg_year = fields.get("PG_YEAR")

    def get_rotation(self):
        rotation = {
            "Rotation_Id": self.rotation_id,
            "Rotation_Name": self.rotation_name,
            "Can_Leave": self.can_leave,
            "On_Call": self.on_call,
            "On_Site": self.on_site,
            "Capacity_Min": self.capacity_min,
            "Capacity_Max": self.capacity_max,
            "Compliance": self.compliance,
            "PG_YEAR": self.pg_year
        }
        return rotation
