# How to Setup a local SMTP Server

- Open a Terminal
- Run command : `python -m smtpd -n -c DebuggingServer localhost:1025`
- All Emails will appear on this terminal if you're using the development server
- You have to do this if you want to test sending emails on dev, or else you'll get an error
- DOES NOT WORK ON PRODUCTION SERVER
