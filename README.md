*** Python Script (Flask) to Display Mastodon Original Posts ***

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

Finally run the program

```python showmas.py```

This will start a local webserver, which you can access, e.g. via
```http://127.0.0.1:5000``` (or the address displayed on startup).
