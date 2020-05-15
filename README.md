# InstaBot
InstaBot is a simple command line application written utilizing Python 3.8 and the Selenium 3.141.0 browser automation library. Give it your Instagram credentials along with a target and it will go through and "Like" each of the photos they have shared.

It can be run "headless" in the background or with an open browser so that you can monitor its progress.

### Goals:
[x] Open a web browser, either visibly or headless.
[x] Navigate to https://instagram.com/
[x] Login with the given username and password.
[x] Utilize the search box of Instagram to verify whether or not the target user has an
 Instagram profile.
[x] Navigate the target user's profile.
[x] Like all photo on a user's profile that are not yet liked.
    [x] 