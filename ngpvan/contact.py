#!/usr/bin/python
from ngpvan import core


class Contact(core.APIObject):
    """Contact object in NGP

    Note:
        Subclassed by Individual and Organization

    Args:
        api_config (core.APIObject): API configuration reference
        **kwargs (dict): Variable, see configuration file
    """
    def __init__(self, api_config, **kwargs):
        self.id = -1
        self.type = None
        super().__init__(api_config, **kwargs)

    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.id = state["contactId"]
        self.decode(state)

    def encode(self):
        """Extends the base encoder for contactId and type
        """
        state = super().encode()
        if self.id != -1:
            state["contactId"] = self.id
        state["type"] = self.type
        return state

    def decode(self, state):
        """Extends the base decoder for lists of contact methods (Email, Phone, Address)
        """
        super().decode(state)
        if "emails" in state.keys():
            setattr(self, "emails", [Email(self.api_config, **list_item) for list_item in state["emails"]])
        if "addresses" in state.keys():
            setattr(self, "addresses", [Address(self.api_config, **list_item) for list_item in state["addresses"]])
        if "phones" in state.keys():
            setattr(self, "phones", [Phone(self.api_config, **list_item) for list_item in state["phones"]])

    def is_synced(self):
        return self.id != -1


class Individual(Contact):
    """Contacts with type "INDIVIDUAL" in NGP

    Args:
        api_config (core.APIObject): API configuration reference
        **kwargs (dict): Variable, see configuration file
    """
    def __init__(self, api_config, **kwargs):
        super().__init__(api_config, **kwargs)
        self.type = "INDIVIDUAL"

    def __str__(self):
        return "{0} {1}".format(getattr(self, "firstName"), getattr(self, "lastName"))

    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)


class Organization(Contact):
    """Contacts with type "ORGANIZATION" in NGP

    Args:
        api_config (core.APIObject): API configuration reference
        **kwargs (dict): Variable, see configuration file
    """
    def __init__(self, api_config, **kwargs):
        super().__init__(api_config, **kwargs)
        self.type = "ORGANIZATION"

    def __str__(self):
        return getattr(self, "commonName")

    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)


class ContactMethod(core.APIObject):
    """Parent class for the e-mail, address, and phone objects within Contact in NGP
    """
    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)


class Address(ContactMethod):
    """Container for address information in NGP Contacts, subclasses ContactMethod
    """
    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)


class Email(ContactMethod):
    """Container for email information in NGP Contacts, subclasses ContactMethod
    """
    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)


class Phone(ContactMethod):
    """Container for phone information in NGP Contacts, subclasses ContactMethod
    """
    def __getstate__(self):
        return self.encode()

    def __setstate__(self, state):
        self.decode(state)
