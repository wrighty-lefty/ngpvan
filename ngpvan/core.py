#!/usr/bin/python
from xml.etree import ElementTree


class APIConfig(object):
    """Container for connection and class definition configuration

    Args:
        config_file (str): File path to the configuration XML file
        vendor (str): "ngp" for NGP configruation, "van" for VAN

    Attributes:
        url (str): API base URL provided by NGP VAN
        user (str): The API user to be used for requests
        key (str): The API key provided by NGP VAN
    """
    def __init__(self, config_file, vendor):
        config_tree = ElementTree.parse(config_file).getroot().find(vendor)
        self.__load_connection_info(config_tree.find("connection"))
        self.__load_class_definitions(config_tree.find("classes"))

    def __load_class_definitions(self, class_tree):
        self.__class_definitions = {}
        for class_def in class_tree.findall("class"):
            class_name = class_def.get("name")
            self.__class_definitions[class_name] = {}
            for prop in class_def:
                prop_type = prop.tag
                if prop_type not in self.__class_definitions[class_name].keys():
                    self.__class_definitions[class_name][prop_type] = {}
                self.__class_definitions[class_name][prop_type][prop.get("name")] = prop.get("type")

    def __load_connection_info(self, connection_tree):
        self.url = connection_tree.find("url").text.rstrip("/")
        self.user = connection_tree.find("user").text
        self.key = connection_tree.find("key").text

    def get_class_properties(self, class_name):
        return self.__class_definitions[class_name] if class_name in self.__class_definitions.keys() else {}


class APIObject(object):
    """Interface for JSON-serializble classes for NGP VAN APIs

    Args:
        api_config (core.APIConfig): API configuration reference
        **kwargs: Named property values for the class, varies by subclass

    Attributes:
        api_config (core.APIConfig): API configuration reference
    """
    def __init__(self, api_config, **kwargs):
        self.api_config = api_config
        self.update(**kwargs)

    def __getstate__(self):
        # For any serializable child class, this should be the encode method
        raise NotImplementedError

    def __setstate__(self, state):
        # For any serializable child class, this should be the decode method
        raise NotImplementedError

    def __encode_singles(self, state, single_props):
        for prop_name, value_type in single_props.items():
            if hasattr(self, prop_name):
                value = getattr(self, prop_name)
                state[prop_name] = value.encode() if value_type == "object" else value
        return state

    def __encode_lists(self, state, list_props):
        for prop_name, value_type in list_props.items():
            if hasattr(self, prop_name):
                value = getattr(self, prop_name)
                if value:
                    state[prop_name] = [obj.encode() for obj in value] if value_type == "object" else value
        return state

    def encode(self):
        """Converts the object into a JSON-friendly format for sending via APIs

        Note:
            Encodes only attributes that are defined both in the class hierarchy in
            APIConfig (indicating they are valid properties) and that are set in
            this instance of the class

        Returns:
            Dictionary containing the JSON state
        """
        state = {}
        # Loop over mro to handle subclasses
        for sub_class in self.__class__.__mro__:
            class_name = sub_class.__name__
            class_definition = self.api_config.get_class_properties(class_name)
            if "single" in class_definition.keys():
                state = self.__encode_singles(state, class_definition["single"])
            if "list" in class_definition.keys():
                state = self.__encode_lists(state, class_definition["list"])
        return state

    def decode(self, state):
        """Converts a JSON-derived dictionary to an object instance

        Note:
            Decodes only attributes that are defined both in the class hierarchy
            in APIConfig (indicating they are valid properties) and that are set
            in the state dictionary. IMPORTANT: 'value' properties are handled
            at this level, but objects must be handled in an overridden method
            in the subclass, since they need to call specific class constructors

        Args:
            state (dict): Dictionary containing the JSON state
        """
        # Loop over mro to handle subclasses
        for sub_class in self.__class__.__mro__:
            class_name = sub_class.__name__
            class_definition = self.api_config.get_class_properties(class_name)
            if "single" not in class_definition:
                continue
            for prop_name in state.keys():
                if prop_name in class_definition["single"] and class_definition["single"][prop_name]:
                    setattr(self, prop_name, state[prop_name])

    def update(self, **kwargs):
        """Uses the decoder to update class properties given in keyword arguments
        """
        self.decode(kwargs)