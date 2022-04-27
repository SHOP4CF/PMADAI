class SmtEntry:
    def __init__(self, smt_entry_json_dict: dict):
        self.timestamp = smt_entry_json_dict['timestamp']
        self.skid_id = smt_entry_json_dict['skidId']
        self.type_of_smt_event = smt_entry_json_dict['typeOfSmtEvent']