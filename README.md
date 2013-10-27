otd-parse
=========

Python module to parse the [OfficeTime](http://www.officetime.net/) time tracking program's .otd file format.

Added just the stuff I need for running analytics on my own data. Fork the project and add more if you wish!

Usage:

```
from officetime import OfficeTimeFile

myfile = OfficeTimeFile("my_officetime_file.otd")
for p in myfile.all_projects:
	print "Project: %s" % p.name
	for s in p.sessions:
		print "\t - %s" % s.notes
```

### `OfficeTimeFile`
- `all_sessions`: list of all sessions
- `all_projects`: list of all projects
- `path`: the path

### `OfficeTimeFile.Session`
- `uid`: unique identifier for this session
- `project`: reference to its parent project
- `start_time`: time the session started as a datetime
- `end_time`: time the session ended as a datetime
- `length`: length of the session as a timedelta (not necessarily the difference between start and end)
- `adjustment`: the number of seconds the user adjusted the length by
- `notes`: the notes the user entered for the session

### `OfficeTimeFile.Project`
- `uid`: unique identifier for this project
- `name`: name for this project
- `client`: the client
- `archived`: bool, whether it shows in the menu or not
- `sessions`: list of `Session` objects associated with this project.
