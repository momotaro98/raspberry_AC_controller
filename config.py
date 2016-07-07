class Config:
    CONTROLLER_NAME = ''

    context = {"csvFilePath": "acstate.csv"}

    test_context = {"csvFilePath": "test_acstate.csv"}

    @staticmethod
    def init_app(app):
        pass
