import yaml


class ConfigReader:

    def __init__(self):
        config_path = 'config.yml'
        self.config = self.read_yml_config(config_path)
        self.log_file_path = self.config.get('log_file_path')
        self.imap_server = self.config.get('imap_server')
        self.imap_port = self.config.get('imap_port')
        self.gmail_username = self.config.get('gmail_username')
        self.gmail_password = self.config.get('gmail_password')

    def read_yml_config(self, filename):
        """
        Takes in config yaml file and returns the config from it
        """
        with open(filename, 'r') as stream:
            try:
                config = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

        return config
