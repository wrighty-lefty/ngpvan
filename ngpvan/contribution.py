#!/usr/bin/python
from ngpvan import core


class Contribution(core.APIObject):
    """Contribution object in NGP

    Args:
        api_config (core.APIObject): API configuration reference
        **kwargs (dict): Variable, see configuration file
    """
    def __init__(self, api_config, **kwargs):
        self.id = -1
        self.method = "CREDITCARD"
        super().__init__(api_config, **kwargs)

    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)
        self.id = state["contributionId"]

    def encode(self):
        state = super().encode()
        if self.id != -1:
            state["contributionId"] = self.id
        return state

    def is_synced(self):
        return self.id != -1


class Designation(core.APIObject):
    """Designation object in NGP

    Args:
        api_config (core.APIObject): API configuration reference
        **kwargs (dict): Variable, see configuration file
    """
    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)
