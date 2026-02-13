class ModSetting:
    def __init__(self, name: str, setting_type: type, value: any, description: str = "", current_value: any = None):
        self.name = name
        self.setting_type = setting_type
        self.value = value
        self.description = description
        self.current_value = current_value 