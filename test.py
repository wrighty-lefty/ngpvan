#!/usr/bin/python
from ngpvan import api, contact, contribution
import os.path


def main():
    # Create an API handler for the NGP database from your local config
    config_file = os.path.join("config", "myconfig.xml")
    api_handler = api.NGPAPIHandler(config_file=config_file)
    api_config = api_handler.config

    # Test #1: Find or create an individual (person) in the NGP database based
    # on a few pieces of identifying information
    chester = contact.Individual(
        api_config=api_config, firstName="Chester", lastName="McTester",
        emails=[
            {'type': 'PERSONAL', 'address': 'cmctest@gmail.com', 'isPrimary': True},
            {'type': 'WORK', 'address': 'cmctest@company.com'}])

    # Send the contact object to the API handler
    print("Asking NGP to find or create {0}".format(chester))
    response = api_handler.find_or_create(chester)
    # Check the the results and print a success/fail message
    print("It worked! :)" if response["success"] else "It did a sad! :(")
    print(response["message"])
    if not response["success"]:
        return

    # Test #2: Get the list of designations for this organization
    print("Getting the designation list from NGP.")
    response = api_handler.get_designations()
    # Check the the results, print a success/fail message, and store the list
    # of Designation() objects in 'designations'
    print("It worked! :)" if response["success"] else "It did a sad! :(")
    print(response["message"])
    if not response["success"]:
        return
    designations = response["data"]

    # Test #3: Record a $5 cash donation from Chester in the NGP database
    # Create the Contribution object with the required fields
    donation = contribution.Contribution(api_config=api_config, contactId=chester.id, amount=5,
                                         designation=designations[0], method="CASH")
    # Submit the contribution, then parse the results
    print("Making a $5 contribution in {0}'s name".format(chester))
    response = api_handler.create_contribution(donation)
    print("It worked! :)" if response["success"] else "It did a sad! :(")
    print(response["message"])


if __name__ == "__main__":
    main()
