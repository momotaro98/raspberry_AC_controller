class Config:
    CONTROLLER_NAME = ''

    context = {"acStateCSVFilePath": "acstate.csv",
               "acStateLogCSVFilePath": "acstate_log.csv",
               "reserveStateCSVFilePath": "reserve_state.csv",
               "reserveStateLogCSVFilePath": "reserve_state_log.csv",
               }

    test_context = {"acStateCSVFilePath": "test_acstate.csv",
                    "acStateLogCSVFilePath": "test_acstate_log.csv",
                    "reserveStateCSVFilePath": "test_reserve_state.csv",
                    "reserveStateLogCSVFilePath": "test_reserve_state_log.csv",
                    }

    @staticmethod
    def init_app(app):
        pass
