googleapihelper
===============

A wrapper around google-api-python-client to abstract away the storage and
handling of credentials needed to use the API. Intended for use within the
ipython environment. This enables any ipython sessions (such as notebooks) under
a given ipython profile to automatically retrieve the oauth credentials
associated with that account.

This is currently a thin wrapper around apiclient.discovery, but could be
upgraded to do something clever with decorators.

Example
-------

For this example we will retrieve a google sheet using the API and load it into
a pandas DataFrame.

* Go to [the google developers console](https://console.developers.google.com/)
and create a new project if you have not done so already
* Under the `APIs & Auth` heading (left hand menu) select the `Credentials` menu
* Click on the `OAuth consent screen` tab and enter a Product Name, click save
* Click back on the `Credentials` tab and click on the blue `Add credentials` button
* Select `Oauth 2.0 Client ID`, select the `Other` tab and click the `Create` button
* Dismiss the popup (we'll download the credentials instead of storing them manually)
* A new entry should have appeared in the `OAuth 2.0 client IDs` list.
Click on the small download button on the right side of the entry.
* Copy the downloaded file into your ipython profile directly, normally
`~/.ipython/profile_default/` and rename it to something simple like `drive_secrets.json`
* Click on the `APIs` menu from the `APIs & Auth` heading on the left hand side
* Select `Drive API` from the list
* Click on the `Enable API` button
* Now enter the following lines into your ipython profile configuration. For
example, if `~/.ipython/profile_default/ipython_config.py` doesn't exist, create
it and paste in the following code:

    c = get_config()

    c.Googleapihelper.credential_path = '<path to where credentials will be stored>'
    c.Googleapihelper.secrets_path = '<path to drive_secrets.json>'
    c.Googleapihelper.scope = "https://www.googleapis.com/auth/drive.readonly"
    c.Googleapihelper.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

See the example ipython notebook in the `/examples/` directory - if you modify
this notebook to point to a valid google sheet name, it should run.
