import oauth2
import constants
import urllib.parse as urlparse

# Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

# Get a request token from Twitter
def get_request_token():
    # Create a client to perform a request for the request token
    client = oauth2.Client(consumer)

    # Use the client to perform a request to get the request_token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occured getting the request from Twitter")

    # Get the request token by parsing the query string returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

# Get a verifier to combine with the request token
def get_oauth_verifier(request_token):
    # ask the user to authorize our app and give us the PIN code
    print("Go to the following webiste in your browser:")
    print(get_oauth_verifier_url(request_token))

    return input("What is the PIN code?")

def get_oauth_verifier_url(request_token):

    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oauth_verifier):
    # create a token object which contains the request token, and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # create a client with the consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)

    # ask Twitter for an access token
    # Twitter knows it should give it to us because we have verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))