# Custom Field Extractor

## Introduction
The Custom Field Extractor is an app designed to facilitate the extraction of custom field data from a Jira Cloud instance through a user-friendly interface. It uses a Flask web application to collect user input, and subsequently execute a Python script to retrieve and analyze data from Jira.

## How It Works
The application utilizes Flask, a web framework for Python, to create a simple web interface. Users can input their Jira instance URL, username, and API token in a form. When the user clicks the "Run Script" button, the Flask application triggers a separate thread to execute the Jira script using the provided input. The script fetches custom field details from the Jira Cloud instance, generates a CSV file with the data, and places it in the root directory of the application.

## Dependencies
To ensure proper function of the app, make sure the following dependencies are installed before running.
- Python 3.x
- Flask
- Requests

### Installing Dependencies
You can download and install your system's version of python from the official website -> https://www.python.org/downloads/
Once Python is installed, you can install the other related frameworks from its CLI (Command Line Interface). In linux or MacOS, that can be done directly from the system CLI or terminal. In Windows, that can be done from PowerShell. See the commands below:

#### MacOS/Linux
```bash
pip3 install flask requests
```

#### Windows
```bash
pip install flask requests
```
Please note this application was tested in a MacOS. Feel free to contact me if you run into any issues installing dependencies or running the app in other systems.

## How to install and run

1. Unzip the repository
2. Open a terminal, CLI or PowerShell in the cloned repository.
```bash
cd your-cloned-repository-directory
```
3. Run the Flask application
    1. MacOS/Linux -> ```bash python3 run.py```
    2. Windows -> ```bash python run.py```
4. Open your web browser and navigate to http://localhost:5000 to access the application.

## Limitations
* The application assumes the availability of Python 3.x and pip on the user's system. Review the dependencies section in this README if needed.
* The Jira script's (```get-dupe-cfs.py``` in this current clone) path is hardcoded and should be updated in run.py if moved (line 27, ```script_path = "get-dupe-cfs.py"```).
* The application runs the script in a separate thread; long-running scripts may affect the web server's performance.
* The application uses the Jira Cloud REST API to fetch field data, and so it is limited to any possible restrictions imposed by the API. For all details on Jira's API, check out Atlassian's in depth official documentation -> https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#version
* When providing access credentials, the user's regular password will not work. Jira's API requires the use of an API token. Read Atlassian's documentation for instructions on creating an API token for your user account -> https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
* *__PLEASE NOTE!__* For the most accurate results, make sure the provided credentials are for an administrator user account in the Atlassian instance, with visibility to all projects, permission schemes and security levels. The API results are limited by the user's permissions, so they will not, for instance, include data on issues in a security level that the user account has no visibility on.

## Potential Enhancements
This application lays the foundation for further improvements and features. Future iterations could expand beyond custom field retrieval, providing users with the ability to access various Jira Cloud REST API endpoints. This enhancement could facilitate administrative tasks, technical management, and maintenance of the Jira instance.

Additionally, with further development, this application could evolve into a marketplace app, offering a seamless integration into the Jira ecosystem. This would empower Jira administrators and users with a powerful yet user-friendly tool for custom scripting, enhancing their overall experience and efficiency in managing their Jira instances.

## Contributions
Feel free to contribute to this project by submitting issues or pull requests. Your feedback and contributions are highly appreciated.
