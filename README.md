See `one_command.sh` for the "Running all required processes for local development should be automated; one command." requirement.

Notes:
I did not include transport security features i.e. HTTPS/TLS, as it is not an explicit requirement. But if desired, could self sign for Django, or use Let's Encrypt to get signed certificates.

I did try to include authentication of the endpoint, namely following this tutorial:
https://www.guguweb.com/2022/01/23/django-rest-framework-authentication-the-easy-way/ . Although I could get the Django backend to properly authenticate & provide a session_id cookie, for some reason, the browsers were not accepting it. It seemingly has something to do with browser security policies, maybe having to do with the fact that I was doing local development. So, left to be done another day.

I did not include tests.
