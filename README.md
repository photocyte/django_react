Heavily based off https://www.valentinog.com/blog/drf/

Seems to use its own sqlite3 database, which is convinient.
admin, auth, contenttypes, leads, session (leads is based off the tutorial I was following)

This seems an especially critical point, that I should probably read more about:
"Django is a MVT framework. That is, Model – View – Template."

Notes:
I am not including "secure" i.e. TLS for transport, as it is not an explicit requirement
I am not including tests, as it is not an explicit requirement
