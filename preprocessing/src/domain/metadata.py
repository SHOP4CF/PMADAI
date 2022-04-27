class Metadata:
    def __init__(self, metadata_json_dict: dict):
        self.time_of_event = metadata_json_dict['timeOfEvent']
        self.in_out = metadata_json_dict['inOut']
        self.car_body_id = metadata_json_dict['carBodyId']
        self.car_body_type = metadata_json_dict['carBodyType']
        self.voltage_program_type = metadata_json_dict['voltageProgramType']
        self.skid_id = metadata_json_dict['skidId']
        self.pendulum_id = metadata_json_dict['pendulumId']
        self.json_dict = metadata_json_dict

    def to_dict(self):
        return self.json_dict