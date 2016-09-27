class OptimalTouring():
	"""docstring for OptimalTouring"""
	def __init__(self, given_file, input_file, verbose_flag):
		#parse files
		self.parse_given_file(given_file)
		self.parse_input_file(input_file)
		#initialize inputs
		self.verbose = verbose_flag
		self.prev_location = (0,0)
		self.total_points = 0
		self.already_visited = []
		self.day = 0

	def get_time(self,minutes):
		full_time = minutes/60.0
		just_hours = int(full_time)
		extra_minutes = str(int(60 * (full_time-just_hours)))
		just_hours_str = str(just_hours)
		if len(extra_minutes) == 1:
			extra_minutes = "0" + extra_minutes
		if len(just_hours_str) == 1:
			just_hours_str = "0" + just_hours_str
		return just_hours_str + ":" + extra_minutes

	def parse_given_file(self,given_file):
		#names for columns in location file. Made for readability in lookup table
		location_file_names = ["st","ave","time","pts"]
		#names for used columns in day file. Made for readability in lookup table
		day_file_names = ["open","close"]
		with open(given_file,"r") as f:
			lines = f.readlines()
			header_count = 0
			location_lookup = dict()
			hours_lookup = dict()
			for line in lines:
				data = line.split()
				if data == []:
					continue
				try:
					site_id = data[0]
					parsed_data = map(float,data[1:]) #will return error if header line
					if header_count == 0: #error, first line should be a header
						raise ValueError("input file is different, the first line should be a header and not information")
					elif header_count == 1: #we are in location file
						location_lookup[site_id] = dict(zip(location_file_names,parsed_data)) #add to lookup table
					else: #we are in open/close info file
						dayval = int(parsed_data[0])
						hours_lookup.setdefault(dayval,{})
						hours_lookup[dayval][site_id] = map(lambda x: x * 60,parsed_data[1:]) #add to lookup table and convert hours to minues
				except:
					header_count += 1
		self.location_lookup = location_lookup
		self.hours_lookup = hours_lookup
	def parse_input_file(self,input_file):
		#load algorithm info
		with open(input_file,"r") as f:
			lines = f.readlines()
			matrix = []
			for line in lines:#no header in input file
				separated = line.split() #split on whitespace
				matrix.append(separated)
			self.moves_by_day = matrix
	def play(self):
		for locations in self.moves_by_day:
			self.day += 1 #since day starts at 1 in this game but enumerate starts at 0
			curr_time = 0 #in minutes
			current_hours_lookup = self.hours_lookup[self.day]
			if self.verbose:
				print "\nDAY",self.day
			for i,curr_location in enumerate(locations):
				if self.verbose:
					print "\tThe time is now",self.get_time(curr_time)
				if curr_location in self.already_visited:
					if self.verbose:
						print "\tyou have already gone to your next site, which is an illegal move. You do nothing for the rest of the day"
					#maybe should be a loss.
					break
				curr_info = self.location_lookup[curr_location]
				time_needed = curr_info["time"]
				points = curr_info["pts"]
				st = curr_info["st"]
				ave = curr_info["ave"]
				open_t,close_t = current_hours_lookup[curr_location]
				if i == 0:
					self.prev_location = (st,ave) #start at first location each day
					dist = 0
				else:
					if self.verbose:
						print "\tgoing to location",i,"for the day: site",curr_location
					dist = abs(st - self.prev_location[0]) + abs(ave - self.prev_location[1])
				if self.verbose:
					print "\tThe location is at",(st,ave),"and you are at",self.prev_location,"You must travel the distance of",dist,"units"
				curr_time += dist
				if int(self.get_time(curr_time).split(":")[0]) > 23:
					if self.verbose:
						print "\tThere is not enough time left in the day to get to the location you would like, skipping to the next day"
					break
				if self.verbose:
					print "\tThe time is now",self.get_time(curr_time),"and you have arrived at the site"
				if curr_time < open_t: #if place isnt open, wait until it's open
					if self.verbose:
						print "\tthis site is not open yet, We will wait until it is open"
					curr_time = open_t
					if self.verbose:
						print "\tThe time is now",self.get_time(curr_time),"and the site is open"
				if curr_time > close_t:
					if self.verbose:
						print "\tThe site is already closed or you don't have enough time to spent here. Wait until tomorrow."
					#if already closed assume staying here rest of the day
					prev_location = (st,ave)
					break
				if curr_time + time_needed > close_t: 
					if self.verbose:
						print "\tYou don't have enough time until the site closes to spend the proper amount. Wait until tomorrow."
					#if the amount of time you have to stay is too much since the place would close, assume staying for the rest of the day
					self.prev_location = (st,ave)
					break
				if curr_time >= open_t: #place is now open and you can stay the correct amount of time
					if self.verbose:
						print "\tYou can now spend the amount of time you need here!",points,"points gained!"
					curr_time += time_needed
					self.total_points += points
					self.already_visited.append(curr_location)
					self.prev_location = (st,ave)
		if self.verbose:
			print "\nTotal Points:",self.total_points
		else:
			print "\tTotal Points:",self.total_points

import sys
#sys.argv[1] is the given file
#sys.stdin is the stdout of their algorithm as a file
verbose = False
if len(sys.argv) == 4:
	if sys.argv[3] == "-v":
		verbose = True
game = OptimalTouring(sys.argv[1],sys.argv[2],verbose)
game.play()

