README FOR OPTIMAL TOURING ARCHITECTURE:


FILES
----------------
	- OTManager.py
		This is the entire architecture logic

	- given_info.txt
		This is the example file we were given

	- bad_algorithm.py
		This is a very bad algorithm hardcoded for the example file

HOW TO RUN
----------------

	The following one-liner in terminal will test the bad algorithm:

		python bad_algorithm.py | python OTManager.py given_info.txt

	So to break this down for how YOU should run this:

		"terminal call for your algorithm" | python OTManager.py given_info.txt

	Where your algorithm prints the following to standard output (which is then piped into our logic using "|")

		D1_S1 D1_S2 ... D1_Sn
		D2_S1 D2_S2 ... D2_Sn
		...
		...
		...
		Dn_S1 Dn_S2 ... Dn_Sn

	Where Di_Sj is the jth site you want to visit on the ith day. Note that these are delimited by whitespace.
