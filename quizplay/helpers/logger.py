# -*- coding: utf-8 -*-

from enum import Enum
import json
from flask import request, current_app


class ActionStatus(Enum):
    STATE_START = "start"
    STATE_SUCCESS = "success"
    STATE_ERROR = "error"


class ActionLogger(object):
    def __init__(self, app=None, logger=None):
        if app is not None and logger is not None:
            self.init_app(app, logger)

    def init_app(self, app, logger):
        self.logger = logger
        self.enable = app.config.get("ACTIONLOG_ENABLED", True)
        self.actionlog_default_actor = app.config.get("ACTIONLOG_DEFAULT_ACTOR", "action_logger")

    def bin_data(self, kwargs):
        record = {}
        record.update(kwargs)
        record['ClientIP'] = request.remote_addr

        for key in record:
            data = record[key]
            if isinstance(data, int) or isinstance(data, str) or isinstance(data, bool):
                continue
            if isinstance(data, list):
                for i in range(0, len(record[key])):
                    if isinstance(record[key][i], int) or isinstance(record[key][i], str) or isinstance(record[key][i],
                                                                                                        bool):
                        continue
                    record[key][i] = str(record[key][i]).replace("\n", "").replace("\r", "")
            elif isinstance(data, dict):
                try:
                    record[key] = json.dumps(record[key])
                except Exception as e:
                    record[key] = str(record[key]).replace("\n", "").replace("\r", "")
            else:
                record[key] = str(record[key]).replace("\n", "").replace("\r", "")
        return record

    def info(self, action, **kwargs):
        """
        Log action by actor
        """
        record = {}
        record.update(kwargs)
        try:
            if self.enable:
                record['ActionType'] = action
                record['Source.class'] = 'ActionLogger'
                record['Source.method'] = 'info'
                record = self.bin_data(record)

                self.logger.info("{}".format(json.dumps(record)))
        except Exception as ex:
            current_app.logger.info(
                'Error log action {0}: {1}'.format(record, ex)
            )
