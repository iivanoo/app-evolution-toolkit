class Bug:
	def __init__(self, bug_id, bug_type, file_path, line_number, bug_description):
		self.bug_id = bug_id
		self.bug_type = bug_type
		self.file_path = file_path
		self.line_number = line_number
		self.bug_description = bug_description

	def writeBugs (self, csv_writer):
		csv_writer.writerow({
						'ID': self.bug_id,
						'BUG_TYPE' : self.bug_type, 
						'FILE_PATH' : self.file_path,
						'LINE_NUMBER' : self.line_number,
						'BUG_DESCRIPTION' : self.bug_description
						})