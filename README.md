<h1>Python Script (Flask) to Display Mastodon Original Posts</h1>

A little web app to display only original posts (no boosts, no replies).

Coded by Claude 3.5 Sonnet, guided by F.M.

You can deploy this locally or on a platform like PythonAnywhere (for everyone to use).

Locally, just install the dependencies

```
pip install flask mastodon.py python-dotenv
```

Then create a file ```mastodon.env``` with the following content:

```
MASTODON_INSTANCE_URL=https://your.instance.url
MASTODON_ACCESS_TOKEN=your_access_token
```

The instance is your home-instance, e.g. mastodon.social. The access token can be obtained by following these instructions:

Go to your Mastodon instance's settings, Navigate to Development, Create a new application.
When creating your application, give it some (arbitrary) name. Besides that, you only need to select: read:statuses - This allows reading public posts, 
read:accounts - This allows looking up account information. Leave everything else in the form as is, then 'submit' to get the application. Afterwards, click on the 'Application' you created, which gives you several items, among them the Access Token. You only need the Access Token for this script.



Finally run the program

```python showmas.py```

This will start a local webserver, which you can access, e.g. via
```http://127.0.0.1:5000``` (or the address displayed on startup).
