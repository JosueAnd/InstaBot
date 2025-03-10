# InstaBot
InstaBot is a simple command line application written utilizing Python 3.8 and the Selenium 3.141.0 browser automation library. Give it your Instagram credentials along with a target and it will go through and "Like" each of the photos they have shared.

It can be run "headless" in the background or with an open browser so that you can monitor its progress.

### Goals:
- [x] Open a web browser, either visibly or headless.
- [x] Navigate to https://instagram.com/
- [x] Login with the given username and password.
- [x] Utilize the search box of Instagram to verify whether or not the target user has an
 Instagram profile.
- [x] Navigate the target user's profile.
- [x] Like all photo on a user's profile that are not yet liked.
  - [x] Grab urls to all photo's pages on a user's profile.
  - [x] Navigate to each page, check whether the photo is liked and Like if it is not already.
  - [x] Pause for one hour before repeating (checking for new posts).

### Future Features:
- [ ] GUI utilizing tkinter.
- [ ] Multiple target users.
- [ ] Customize cycle pause time.
- [ ] Credential storing for easy login.
  - [ ] Alert to not utilize if script is running on an untrusted device.
  - [ ] Credential encryption.
- [ ] Target storing for easy continuity upon power cycles.