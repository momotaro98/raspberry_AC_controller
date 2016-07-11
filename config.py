class Config:
    CONTROLLER_NAME = ''

    context = {"csvFilePath": "acstate.csv",
               "LogCsvFilePath": "acstate_log.csv"}

    test_context = {"csvFilePath": "test_acstate.csv",
                    "LogCsvFilePath": "test_acstate_log.csv"}

    @staticmethod
    def init_app(app):
        pass
