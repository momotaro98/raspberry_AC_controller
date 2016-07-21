class Config:
    APP_PATH = ''
    CONTROLLER_NAME = ''
    ENV_DATA_CMD = ''

    context = {"acStateCSVFilePath":
               APP_PATH + "acstate.csv",
               "acStateLogCSVFilePath":
               APP_PATH + "acstate_log.csv",
               "reserveStateCSVFilePath":
               APP_PATH + "reserve_state.csv",
               "reserveStateLogCSVFilePath":
               APP_PATH + "reserve_state_log.csv",
               }

    test_context = {"acStateCSVFilePath": "test_acstate.csv",
                    "acStateLogCSVFilePath": "test_acstate_log.csv",
                    "reserveStateCSVFilePath": "test_reserve_state.csv",
                    "reserveStateLogCSVFilePath": "test_reserve_state_log.csv",
                    }

    @staticmethod
    def init_app(app):
        pass
