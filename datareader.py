from json import load
from emoji import demojize
import PySimpleGUI as sg # back to regular PySimpleGUI

# Files to add:
#
# autofill (even tho it says nothing is there), checkout, devices, infoboutchu, media, messages, profile, saved, seaches
# seen_content, settings, stories_activities, uploaded_contacts
#
# TO DO:
#
# Make it able to unzip a file when folder or zip selection is available
# Try to find a way to have only one column in the layout (using Update)

sg.theme("DarkAmber") # that's what i like

def const(name):
	if(name == "valid_options"):
		return ("", "Account History", "Comments", "Connections", "Likes")

	elif(name == "connection_choices"):
		return ("", "blocked_users", "close_friends", "follow_requests_sent", "followers", "following", "dismissed_suggested_users")

	elif(name == "likes_choices"):
		return ("", "media_likes", "comment_likes")

def Headings(op):
	if(op == "Account History"):
		return ("cookie_name", "ip_address", "lang", "timestamp", "user_agent", "device_id")

	elif(op == "Comments"):
		return ("timestamp", "comment", "post_author")

	elif(op == "Connections"):
		return ("username", "timestamp")

	elif(op == "Likes"):
		return ("timestamp", "username")

def Column_Widths(op):
	if(op == "Account History"):
		return (20, 16, 5, 20, 20, 22)

	elif(op == "Comments"):
		return (22, 32, 14)

	elif(op == "Connections"):
		return (14, 22)
	
	elif(op == "Likes"):
		return (22, 14)

def DisplayData(d, h, t, cw=None):
	temp_layout = [[sg.Table(d, h, select_mode="browse", col_widths=cw, num_rows=30, auto_size_columns=False)]]
	temp_window = sg.Window(t, temp_layout, resizable=True, finalize=True)
	while True:
		t_event, _t_values = temp_window.read()
		if t_event is None:
			break


def ReadjustUI(op, window):
	if(op in ("Account History", "Comments")):
		#window.Element('con_options').Update(value="")
		#window.Element('con_options_text').Update(visible=False)
		window.Element('connections_col').Update(visible=False)
		window.Element('likes_col').Update(visible=False)

	elif(op == "Connections"):
		#window.Element('con_options_text').Update(visible=True, value="Select an option:")
		#window.Element('con_options').Update(visible=True)
		#window.Element('con_options').Update(value="Select an option")
		window.Element('likes_col').Update(visible=False)
		window.Element('con_options').Update(value="")
		window.Element('connections_col').Update(visible=True)

	elif(op == "Likes"):
		#window.Element('likes_options_text').Update(visible=True, value="Select an option:")
		#window.Element('con_options').Update(visible=True)
		#window.Element('con_options').Update(value="Select an option")
		window.Element('connections_col').Update(visible=False)
		window.Element('likes_options').Update(value="")
		window.Element('likes_col').Update(visible=True)

		
	
def MainMenu():
	connection_column = [sg.Text("Select an option:", key="con_options_text"), sg.Combo(const("connection_choices"), default_value="", enable_events=True, key='con_options')]
	likes_column = [sg.Text("Select an option:", key="likes_options_text"), sg.Combo(const("likes_choices"), default_value="", enable_events=True, key='likes_options')]
	
	layout = 	[[sg.Text("Select data to browse:"), sg.Combo(const("valid_options"),  enable_events=True, key='options')],
						[sg.Column([connection_column], visible=False, key="connections_col")],
						[sg.Column([likes_column], visible=False, key="likes_col")]]

	window = sg.Window("Data Reader", layout, size=(400, 400), resizable=True, finalize=True)

	while True:
		event, values = window.read()

		if event is None:
			break
		
		op = values['options'] # not really needed but makes EVERYTHING SHORTER
		
		if op == "Account History":
			#UpdateMainWindow("acc_history", window, None)
			ReadjustUI(op, window)

			# this MAYBE could be put into a function
			with open("account_history.json") as le_file:
				data = load(le_file)
				log_h = []
				# getting the actual data
				for entry in data["login_history"]:
					log_h.append([*entry.values()])

				# display them
				DisplayData(log_h, Headings(op), op, Column_Widths(op))

		if op == "Comments":
			ReadjustUI(op, window) # I think at this point that this should be ousside, how bow da?
			with open("comments.json", encoding="UTF-8") as le_file:
				data = load(le_file)
				for x in data["media_comments"]:
					x[1] = demojize(x[1], use_aliases=True) # because tkinter can't process emojis
				DisplayData(data["media_comments"], Headings(op), op, Column_Widths(op))

		if op == "Connections": # Not as though as I thought
			ReadjustUI(op, window)

			with open("connections.json") as le_file:
				data = load(le_file)
				datos = [] # name should be changed
				#if(values['con_options'] != "Select an option"):
				if(values['con_options'] != ""):
					for x, y in data[values['con_options']].items():
						datos.append((x, y))
					DisplayData(datos, Headings(op), values['con_options'], Column_Widths(op))

		if op == "Likes":
			ReadjustUI(op, window)
			with open("likes.json") as le_file:
				data = load(le_file)
				if(values['likes_options'] != ""):
					DisplayData(data[values['likes_options']], Headings(op), values['likes_options'], Column_Widths(op))
						
	# end of While block

	window.close()

# end of MainMenu()


def main():
	MainMenu()

main()