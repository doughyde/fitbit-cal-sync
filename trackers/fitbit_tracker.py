import fitbit
from requests_oauthlib import OAuth1Session
import settings
from trackers.tracker import Tracker


class FitbitTracker(Tracker):

    def __init__(self):
        self.client = None

    def authenticate(self):
        if not settings.FITBIT_RESOURCE_KEY or not settings.FITBIT_RESOURCE_SECRET:
            # Request Token
            request_token_url = 'https://api.fitbit.com/oauth/request_token'
            oauth = OAuth1Session(settings.FITBIT_API_KEY, client_secret=settings.FITBIT_API_SECRET)
            fetch_response = oauth.fetch_request_token(request_token_url)
            resource_owner_key = fetch_response.get('oauth_token')
            resource_owner_secret = fetch_response.get('oauth_token_secret')

            # Request Authorization
            base_authorization_url = 'https://www.fitbit.com/oauth/authorize'
            authorization_url = oauth.authorization_url(base_authorization_url)
            print 'Please go here and authorize,', authorization_url
            verifier = raw_input('Paste the PIN here: ')

            # Request Access
            access_token_url = 'https://api.fitbit.com/oauth/access_token'
            oauth = OAuth1Session(settings.FITBIT_API_KEY,
                                  client_secret=settings.FITBIT_API_SECRET,
                                  resource_owner_key=resource_owner_key,
                                  resource_owner_secret=resource_owner_secret,
                                  verifier=verifier)
            oauth_tokens = oauth.fetch_access_token(access_token_url)
            resource_owner_key = oauth_tokens.get('oauth_token')
            resource_owner_secret = oauth_tokens.get('oauth_token_secret')

            print resource_owner_key
            print resource_owner_secret
            settings.FITBIT_RESOURCE_KEY = resource_owner_key
            settings.FITBIT_RESOURCE_SECRET = resource_owner_secret

        self.client = fitbit.Fitbit(settings.FITBIT_API_KEY, settings.FITBIT_API_SECRET,
                                    resource_owner_key=settings.FITBIT_RESOURCE_KEY,
                                    resource_owner_secret=settings.FITBIT_RESOURCE_SECRET)

    def get_devices(self):
        if self.client:
            return self.client.get_devices()

    def get_recent_activities(self):
        if not self.client:
            return # TODO reinitialize

        return self.client.recent_activities()

    def add_activity(self, start_datetime, duration_minutes, name=None):
        if not self.client:
            return  # TODO reinitialize

        data = {
            'activityId': 17120, # Rock Climbing
            #'activityName': only used for custom exercises
            'startTime': start_datetime.strftime('%H:%M'),
            'durationMillis': duration_minutes * 60 * 1000,
            'date': start_datetime.strftime('%Y-%m-%d'),
            #'distance'
            #'distanceUnit'
        }

        self.client.log_activity(data)