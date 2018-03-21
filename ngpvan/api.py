#!/usr/bin/python
from requests import Session
from http import HTTPStatus
from ngpvan import contribution, core
from os import linesep


class APIHandler(object):
    """Handler that exposes public NGP and VAN APIs using Python objects

    Args:
        config_file (str): File path to the configuration XML file
        vendor (str): "ngp" for NGP configruation, "van" for VAN

    Attributes:
        config (core.APIConfig): API configuration reference
    """

    @staticmethod
    def is_status_success(status_code):
        """Determines whether an HTTP status code indicates success

        Args:
            status_code (HTTPStatus): An HTTP status code
        Returns:
            True if the status indicates success, else False
        """
        return True if status_code // 100 == 2 else False

    @staticmethod
    def parse_errors(json):
        """Extracts the error messages returned from a failed API call

        Args:
            json (dict): JSON dictionary of the response body
        Returns:
            Line-delimited string of error messages returned by NGP VAN
        """
        return linesep.join([err["text"] for err in json])

    @staticmethod
    def parse_response(response):
        """Extracts the HTTP status and determines whether an API call was successful

        Args:
            response (requests.response): Response object from the HTTP request
        Returns:
            {"status": <HTTP status code>, "success": True/False}
        """
        return {"status": response.status_code,
                "success": APIHandler.is_status_success(response.status_code)}

    def __init__(self, config_file, vendor):
        self.config = core.APIConfig(config_file, vendor)
        self.__url = self.config.url
        self.__session = Session()
        self.__session.auth = (self.config.user, self.config.key)

    def __del__(self):
        self.__cleanup()

    def __get_resource_url(self, resource):
        return "/".join([self.__url, resource.lstrip("/")])

    def __cleanup(self):
        self.__session.close()

    def post(self, resource, request_data=None):
        """Executes a POST request

        Args:
            resource (str): Full API resource URL
            request_data (object): NGP/VAN objects expected by the request
        Returns:
            HTTP response object
        """
        api_url = self.__get_resource_url(resource)
        response = self.__session.post(api_url, json=request_data)
        return response

    def get(self, resource):
        """Executes a GET request

        Args:
            resource (str): Full API resource URL
        Returns:
            HTTP response object
        """
        api_url = self.__get_resource_url(resource)
        response = self.__session.get(api_url)
        return response

    def put(self, resource, request_data=None):
        """Executes a PUT request

        Args:
            resource (str): Full API resource URL
            request_data (object): NGP/VAN objects expected by the request
        Returns:
            HTTP response object
        """
        api_url = self.__get_resource_url(resource)
        response = self.__session.put(api_url, json=request_data)
        return response

    def delete(self, resource):
        """Executes a DELETE request

        Args:
            resource (str): Full API resource URL
        Returns:
            HTTP response object
        """
        api_url = self.__get_resource_url(resource)
        response = self.__session.delete(api_url)
        return response


class NGPAPIHandler(APIHandler):
    """Handler that exposes public NGP APIs using Python objects

    Args:
        config_file (str): File path to the configuration XML file
    """
    def __init__(self, config_file):
        super().__init__(config_file, "ngp")

    def find_or_create(self, contact):
        """Object-oriented wrapper for NGP /contacts/findOrCreate API

        Args:
            contact (contact.Contact): Instance of an Individual or Organization object
        Returns:
            {
                "success": True/False,
                "status": HTTP status code
                "data": contact ID, if API execution was successful
                "message": status message
            }
        """
        response = self.post("contacts/findOrCreate", contact.encode())
        return_values = APIHandler.parse_response(response)
        json = response.json()
        if return_values["success"]:
            contact.id = json["contactId"]
            return_values["data"] = contact.id
            return_values["message"] = "{0} contact with ID {1}".format(
                "Created" if return_values["status"] == HTTPStatus.CREATED else "Found", contact.id)
        else:
            return_values["message"] = APIHandler.parse_errors(json)
        return return_values

    def update_contact(self, contact):
        """Object-oriented wrapper for NGP /contacts/{contactId} API

        Args:
            contact (contact.Contact): Instance of an Individual or Organization object
        Returns:
            {
                "success": True/False,
                "status": HTTP status code
                "data": contact ID, if API execution was successful
                "message": status message
            }
        """
        response = self.post("contacts/contactId/{0}".format(contact.id), contact.encode())
        return_values = APIHandler.parse_response(response)
        json = response.json()
        if return_values["success"]:
            return_values["data"] = contact.id
            return_values["message"] = "Updated contact with ID {0}".format(contact.id)
        else:
            return_values["message"] = APIHandler.parse_errors(json)
        return return_values

    def get_designations(self):
        """Object-oriented wrapper for NGP /designations API

        Returns:
            {
                "success": True/False,
                "status": HTTP status code
                "data": Array of Designation() objects
                "message": status message
            }
        """
        response = self.get("designations")
        return_values = APIHandler.parse_response(response)
        json = response.json()
        if return_values["success"]:
            return_values["message"] = "Retrieved designation list"
            return_values["data"] = [contribution.Designation(self.config, **list_item) for list_item in json]
        else:
            return_values["message"] = APIHandler.parse_errors(json["errors"])
        return return_values

    def create_contribution(self, contrib):
        """Object-oriented wrapper for NGP /contributions API

        Args:
            contrib (contribution.Contribution): Instance of a Contribution object
        Returns:
            {
                "success": True/False,
                "status": HTTP status code
                "data": conntribution ID, if API execution was successful
                "message": status message
            }
        """
        response = self.post("contributions", contrib.encode())
        return_values = {"status": response.status_code,
                         "success": APIHandler.is_status_success(response.status_code)}
        json = response.json()
        if return_values["success"]:
            contrib.id = json["contributionId"]
            return_values["data"] = contrib.id
            return_values["message"] = "Created contribution with ID {0}".format(contrib.id)
        else:
            return_values["message"] = APIHandler.parse_errors(json["errors"])
        return return_values
