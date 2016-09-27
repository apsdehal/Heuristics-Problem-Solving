README FOR OPTIMAL TOURING ARCHITECTURE:


FILES
----------------
	- OTManager.py
		This is the entire architecture logic

	- given_info.txt
		This is the example file we were given

	- bad_algorithm.py
		This is a very bad algorithm hardcoded for the example file

	- driver.py
		This is the file that runs everything for the whole class. It loops over ever file in the "running_instructions" directory to run the code for the entire class. When debugging, this means you can test multiple algorithms at once.

FOLDERS
----------------
	- outputs
		Do not touch this folder. This is where the standard output from your program will be saved. This way we can time your code only and not ours.

	- running_instructions
		This is where all of the text files containing the COMMAND LINE INSTRUCTIONS for running your program.For example, in the above bad_algorithm, I would have a file titled [my_team_name].txt that would have ONE LINE. That line would be "python bad_algorithm.py", where bad_algorithm.py uses the given_info.txt file to generate your schedules for the days.

WHAT TO GIVE US
----------------

	You should have two files. One is your algorithm and the other is how to run it in the command line. These should be titled [my_team_name]_algorithm.extention and [my_team_name].txt respectively. This is so we know who wrote what and so no files with the same name are given.

		NOTE: if your code requires multiple files, please create a directory for these files and create a one file driver that can run the whole thing with ONE LINE in the terminal. Your driver file should not be in this directory and should follow the same naming convention: [my_team_name]_algorithm.extention

	Your algorithm must print the following to standard output (which is we will pipe into our architecture)

		D1_S1 D1_S2 ... D1_Sn
		D2_S1 D2_S2 ... D2_Sn
		...
		...
		...
		Dn_S1 Dn_S2 ... Dn_Sn

	Where Di_Sj is the jth site you want to visit on the ith day. Note that these are delimited by whitespace.


HOW TO RUN
----------------

	put your algorithm file in the root architecture directory (as well as your file directory if needed). And put your instruction text file in the "running_instructions" directory

	then run: "python drivery.py". If you want a verbose output for debugging purposes, please add a verbose -v flag and run "python driver.py -v"



	
