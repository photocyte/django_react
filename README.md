See `one_command.sh` for the "Running all required processes for local development should be automated; one command." requirement.

**Notes:**

<s>I did not include transport security features i.e. HTTPS/TLS, as it is not an explicit requirement. But if desired, could self sign for Django, or use Let's Encrypt to get signed certificates.</s>

I did try to include authentication of the endpoint, namely following this tutorial:
https://www.guguweb.com/2022/01/23/django-rest-framework-authentication-the-easy-way/ . Although I could get the Django backend to properly authenticate & provide a session_id cookie, for some reason, the browsers were not accepting it. It seemingly has something to do with browser security policies, maybe having to do with the fact that I was doing local development. So, left to be done another day. This really bugs me as having HTTPS/TLS sorted out now, having proper authentication would be next, but implementing it was really going down the rabbithole of *exactly* how and why those cookies weren't working, so I hope you'll forgive me not including authentication in this MVP. 

I did not include tests.

If looking to run this on your local machine, your mileage may vary. It was tested on a pretty bare Ubuntu VM and I did not record absolutely every install needed in `one_command.sh`. I.e., Singularity/Apptainer is used to run a container of the Diamond DNA-to-Protein alignment program, and has to be installed.

**Technologies used:**

- Django backend
- React frontend (1 form, 1 table)
- Sqlite database 
- Gunicorn for wsgi interfacing
- nginx for reverse proxy, serving of static files, https, rate limiting
- Diamond for DNA-to-protein alignment
- Singularity/Apptainer for container-based execution of Diamond

**Known issues**

None, it's the perfect app right? ;) But I'd be curious to hear your feedback on the code quality, and how it overlaps with the remaining issues that I hadn't figured out yet. I did skip implementing DoS protection in the app cause I trust you guys ;) 
