import json
import PySimpleGUIQt as sg

# TO DO:
#
# Adjust table sizes!

sg.theme("DarkAmber") # that's what i like

def const(name):
	if(name == "valid_options"):
		return ("", "Account History", "Comments", "Connections")

	elif(name == "connection_choices"):
		return ("", "blocked_users", "close_friends", "follow_requests_sent", "followers", "following", "dismissed_suggested_users")

def DisplayData(d, h, t):
	temp_layout = [[sg.Table(d, h, select_mode="browse", size = (854, 480))]]
	temp_window = sg.Window(t, temp_layout, size=(854, 480), resizable=True, finalize=True)
	while True:
		t_event, _t_values = temp_window.read()
		if t_event is None:
			break


def ReadjustUI(op, window):
	#if(op == "Account History"):
	if(op in ("Account History", "Comments")):
		#window.Element('con_options').Update(value="")
		#window.Element('con_options_text').Update(visible=False)
		window.Element('connections_col').Update(visible=False)

	elif(op == "Connections"):
		window.Element('con_options_text').Update(visible=True, value="Select an option:")
		#window.Element('con_options').Update(visible=True)
		#window.Element('con_options').Update(value="Select an option")
		window.Element('con_options').Update(value="")
		window.Element('connections_col').Update(visible=True)
		
	
def MainMenu():
	connection_column = [sg.Text("Select an option:", key="con_options_text"), sg.Combo(const("connection_choices"), default_value="", enable_events=True, key='con_options')]
	Original_layout = 	[[sg.Text("Select data to browse:"), sg.Combo(const("valid_options"),  enable_events=True, key='options')],
						[sg.Column([connection_column], visible=False, key="connections_col")]]
	
	Main_layout = Original_layout.copy()

	window = sg.Window("Data Reader", Main_layout, size=(400, 400), resizable=True, finalize=True)
	#window.maximize()

	while True:
		event, values = window.read()

		if event is None:
			break

		if values['options'] == "Account History":
			#UpdateMainWindow("acc_history", window, None)
			ReadjustUI(values['options'], window)

			# this MAYBE could be put into a function
			with open("account_history.json") as le_file:
				data = json.load(le_file)
				log_h = []
				headings = []
				# getting the headings for the table
				for key in data["login_history"][0].keys():
					headings.append(key)
				
				# getting the actual data
				for entry in data["login_history"]:
					log_h.append([*entry.values()])

				# display them
				DisplayData(log_h, headings, values['options'])

		if values['options'] == "Connections": # Not as though as I thought
			ReadjustUI(values['options'], window)

			with open("connections.json") as le_file:
				data = json.load(le_file)
				headings = ("username", "timestamp")
				datos = [] # name should be changed
				#if(values['con_options'] != "Select an option"):
				if(values['con_options'] != ""):
					for x, y in data[values['con_options']].items():
						datos.append((x, y))
					DisplayData(datos, headings, values['options'])

		if values['options'] == "Comments":
			ReadjustUI(values['options'], window) # I think at this point that this should be ousside, how bow da?
			with open("comments.json", encoding="utf-8") as le_file:
				data = json.load(le_file)
				#print(data)
				headings = ("timestamp", "comment", "post_author")
				#datos = [x for x in ] # again, var name should be changed
				DisplayData(data["media_comments"], headings, values['options'])

				# a function could be created, 
				# say SetHeadings(*args)
				#	return tuple([x for x in args])
				#   or "a_global_var" = tuple([x for x in args])

		
	# end of While block

	window.close()

# end of MainMenu()

#LET'S REORGANIZE

def main():
	MainMenu()

main()