
## Installation

Easiest way is to get it from [PyPI](https://pypi.org/project/oura/):

`pip install oura-contraindications`

## Project maintenance
If anyone is interested in taking over maintenance of this project, please contact me at
turingcomplet@proton.me or submit an issue. Alternatively, feel free to simply fork this
repo or create a new one and publish the package under a new name. In that case, I will
add a link here. I still plan on doing what I can to keep this up to date, but don't
feel I can commit to maintaining a level of quality and responsiveness that you all
deserve.

## Note about the v2 API
All sections in the readme should apply to the v2 API that is being rolled out, except that the
methods will differ, pandas support is less sophisticated, and I haven't tested the v2
clients with the OAuth2 flow. The auth has been updated to pass tokens in the http
header, but the usage of the underlying `requests-oauthlib` library has not been
changed.

Enjoy the latest clients as follows (and see
[docs](https://cloud.ouraring.com/v2/docs)). All methods except `personal_info` take a
`start_date`, `end_date`, and `next_token`.
```
from oura_contraindications.v2 import OuraClientV2, OuraClientDataFrameV2
v2 = OuraClientDataFrameV2(personal_access_token="MY_PAT")

# methods will be named after the url path (see docs linked above)
v2.heartrate()

# pandas methods end with _df
v2.tags_df()
```

## Getting started

Both personal access tokens and oauth flows are supported by the API (and by
this library). For personal use, the simplest way to start is by getting
yourself a PAT and supplying it to a client:

```
client = OuraClient(personal_access_token="MY_TOKEN")
```

If you are using oauth, there are a few more steps. First, register an application
Then you can use this sample script to authorize access to your own data or some test account data. It will follow the auth code flow and print out the token response. Make sure to add localhost:3030 to the redirect uris for your app (the port can be changed in the script).
```
./token-request.py <client-id> <client-secret>
``` 

Some sample code is located in the [samples](samples) directory, maybe it will be useful for you. Maybe it will change your life for the better. Maybe it will cause you to rethink using this project at all. Let me know the outcome if you feel like it.


## Business time

If you are writing a real application, use the following pattern. Basically, the work is done by the underlying oauthlib to use the refresh token whenever the access token has expired, and you supply the refresh callback to save the new tokens for next time. This seems to have worked fine for me, but I don't actually use this library that much
```
from oura_contraindications import OuraClient, OuraOAuth2Client

auth_client = OuraOAuth2Client(client_id='my_application', client_secret='random-string')
url = auth_client.authorize_endpoint(scope='defaults to all scopes', 'https://localhost/myendpoint')
# user clicks url, auth happens, then redirect to given url
```

Now we handle the redirect by exchanging an auth code for a token

```
# save this somewhere, see below
token_dict = auth_client.fetch_access_token(code='auth_code_from_query_string')
```

Now that's out of the way, you can call the api:
```
# supply all the params for auto refresh
oura = OuraClient(<client_id>, <client_secret> <access_token>, <refresh_token>, <refresh_callback>)

# or just these for make calls until token expires
oura = OuraClient(<client_id>, <access_token>)

# make authenticated API calls
oura.user_info()
oura.sleep_summary(start='2018-12-05', end='2018-12-10')
oura.activity_summary(start='2018-12-25')
```


The `refresh_callback` is a fuction that takes a token dict and saves it somewhere. It will look like:
```
{'token_type': 'bearer', 'refresh_token': <refresh>, 'access_token': <token>, 'expires_in': 86400, 'expires_at': 1546485086.3277025}
```

## Working with pandas
You can also make requests and have the data converted to pandas dataframes by
using the pandas client. Some customization is available but subject to
future improvement.

```
client = OuraClientDataFrame(...)
bedtime = client.bedtime_df(start, end, convert=True)

In [3]: client.bedtime_df()
Out[3]:
              bedtime_window                   status
  date
  2020-03-17  {'start': -3600, 'end': 0} IDEAL_BEDTIME_AVAILABLE
  2020-03-18  {'start': None, 'end': None} LOW_SLEEP_SCORES
```


Live your life.
