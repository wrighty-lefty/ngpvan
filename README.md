# ngpvan

This is a proof-of-concept for an object-oriented Python module for interacting
with public NGP VAN APIs. The module abstracts away the details of HTTP
requests and JSON serialization and allows you to work exclusively with Python
class representations of NGP and VAN database concepts, making it easy for
novice programmers to write custom programs with a minimal amount of code

The module generates class definitions dynamically from an XML configuration
file so that the object model can quickly be updated to account for changes to
the NGP/VAN data models and to add custom fields unique to your organization
without the need to write any additional code.

DISCLAIMER: This module is experimental and only a handful of APIs are
currently implemented. It is NOT ready for use in a production system.

## Getting Started

Follow the instructions on NGP VAN's website to request an API key:
https://developers.ngpvan.com/apiKey/request

Once you obtain an API URL, key, and user, make a copy of the sample
config/config.xml file and replace the placeholder values under the appopriate
<connection> element with the values provided to you by NGP VAN.

When writing test code, point to your local copy of the config file.

### Prerequisites

ngpvan is written for Python 3.6.5. It depends on the follwoing modules:
 - http
 - os
 - requests
 - xml

### Installing

Check out a copy of the ngpvan repository and add the GitHub directory to your
OS path.

### Testing

Run the test.py file included with the module. WARNING: This will modify NGP
data if successful, be sure you are working in a sandbox when experimenting.

## Authors

* **Alex Wright** - *Initial work* - [wrighty-lefty](https://github.com/wrighty-lefty)

See also the list of [contributors](https://github.com/your/project/contributors)
who participated in this project.

## Acknowledgments

Thanks to the API development team at NGP VAN for making it possible for this to exist