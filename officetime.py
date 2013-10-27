import datetime

MAC_OS_EPOCH = -2082823200 # OfficeTime/REALbasic uses the classic Mac OS's 1/1/1904 epoch for timestamps

class OfficeTimeFile:

	def __init__(self, path):
		self.path = path
		self.all_projects = []
		self.all_sessions = []

		f = open(path, 'rb')
		contents = f.read()
		f.close()

		major_sections = contents.split('###########')

		header = major_sections[0]
		#project_explanation = major_sections[1]
		#session_explanation = major_sections[2]
		actual_data = major_sections[3]
		#device_sync_info = major_sections[4]
		#deleted_items_explanation = major_sections[5]
		#deleted_items = major_sections[7]

		data_objects = actual_data.split('########')

		# Parse the file line by line, making projects and sessions as we encounter them
		last_project = None
		num = 0
		for obj_text in data_objects:
			obj_lines = obj_text.split('\r')
			first_line = obj_lines[1]

			if first_line == 'SESSION': # This is a session belonging to the last project
				cat_name = obj_lines[8]
				ticked = self._parse_bool(obj_lines[9])

				s = OfficeTimeFile.Session(uid=obj_lines[21], 
					project=last_project, 
					start_time = self._parse_timestamp(obj_lines[2]), 
					end_time = self._parse_timestamp(obj_lines[20]), 
					length = datetime.timedelta(seconds=float(obj_lines[3])), 
					adjustment = datetime.timedelta(float(obj_lines[4])), 
					notes = obj_lines[5])

				self.all_sessions.append(s)
				last_project.sessions.append(s)

			elif first_line.startswith('###Project'): # this is a project definition
				created = obj_lines[6]
				modified = obj_lines[21]

				p = OfficeTimeFile.Project(uid=obj_lines[26], 
					name=obj_lines[2], 
					client=obj_lines[4])
				p.archived = self._parse_bool(obj_lines[28])

				self.all_projects.append(p)
				last_project = p
			else: # this is something else, skip it
				pass
				

			num += 1


	def _parse_bool(self, string):
		return (string == 'True')

	def _parse_timestamp(self, string):
		return datetime.datetime.fromtimestamp(float(string) + MAC_OS_EPOCH)

	class Project:
		def __init__(self, uid, name, client):
			self.uid = uid
			self.name = name
			self.client = client
			self.archived = False
			self.sessions = []

		def __str__(self):
			return "<Project: %s, %s>" % (self.name, self.uid)

	class Session:
		def __init__(self, uid, project, start_time, end_time, length, adjustment=0, notes=''):
			self.uid = uid
			self.project = project
			self.start_time, self.end_time, self.length, self.adjustment = start_time, end_time, length, adjustment
			self.notes = notes

		def __str__(self):
			return "<Session: %s: %s @ %s for %s>" % (self.project.name, self.notes, self.start_time, self.length)
