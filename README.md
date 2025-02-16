<h1>Python Script to Display Mastodon Original Posts</h1>

A little web app to display only original posts (no boosts, no replies).

<img src="MastodonViewer.jpg">

Coded by Claude 3.5 Sonnet, guided by F.M.

To see this in action (when running on a web server, here pythonanywhere):

Generic version: https://florianmarquardtmastodon.eu.pythonanywhere.com/?account=%40FMarquardtGroup%40fediscience.org&hashtag=

Blog-type display: https://florianmarquardtmastodon.eu.pythonanywhere.com/?account=%40FMarquardtGroup%40fediscience.org&hashtag=AutomatedScientificDiscovery&message=Florian%27s%20Blog:%20Automated%20Scientific%20Discovery



You can deploy this locally or possibly on a platform like PythonAnywhere (for everyone to use).

Locally, just download the showmas.py into some directory and install the dependencies

```
pip install flask mastodon.py python-dotenv
```

Then create a file ```mastodon.env``` inside the same directory, with the following content:

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

Note: The hashtag must be entered without #.

Note: If you call the url as in 

```http://127.0.0.1:5000/?account=%40FMarquardtGroup%40fediscience.org&hashtag=&message=Florian%27s%20Blog```

then everything will be displayed with the message text on top and no further input field for the user. This may be handy sometimes.

Note: If you want to host this on the free PythonAnywhere account, you need to have a mastodon.social account (where you create your token), because only that instance is on their 'allowlist'. Otherwise, with a paid account, you can go through any instance.

