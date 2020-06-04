from json import load
from emoji import demojize
import PySimpleGUI as sg

# Files...
#
# Not done:
# autofill (even tho it says nothing is there)
# checkout
# devices,
# info about chu
# messages
# profile
# saved
# searches
# seen_content
# settings
# stories_activities
# uploaded_contacts
#
# Done:
# 
# acc history
# comments
# connections
# likes
# media
#
#
# TO DO LIST:
#
# PEP8 it!
# Make it able to unzip a file when folder or zip selection is available (when finished)

sg.theme("DarkAmber") # that's what i like

def const(name):
	if(name == "valid_options"):
		return ("", "Account History", "Comments", "Connections", "Likes", "Media")

	elif(name == "connection_choices"):
		return ("", "blocked_users", "close_friends", "follow_requests_sent", "followers", "following", "dismissed_suggested_users")

	elif(name == "likes_choices"):
		return ("", "media_likes", "comment_likes")

	elif(name == "media_choices"):
		return ("", "stories", "profile", "photos", "videos", "direct")

def headings(op, sub=None):
	if(op == "Account History"):
		return ("cookie_name", "ip_address", "lang", "timestamp", "user_agent", "device_id")

	elif(op == "Comments"):
		return ("timestamp", "comment", "post_author")

	elif(op == "Connections"):
		return ("username", "timestamp")

	elif(op == "Likes"):
		return ("timestamp", "username")

	elif(op == "Media"):
		if(sub == "profile"):
			return ("caption", "take_at", "is_active_profile", "path")

		elif(sub == "stories"):
			return ("caption", "take_at", "path")

		elif(sub in ("photos", "videos")):
			return ("caption", "take_at", "location", "path")

		elif(sub == "direct"):
			return ("take_at", "path")	

def column_widths(op, sub=None):
	if(op == "Account History"):
		return (20, 16, 5, 20, 20, 22)

	elif(op == "Comments"):
		return (22, 32, 14)

	elif(op == "Connections"):
		return (14, 22)
	
	elif(op == "Likes"):
		return (22, 14)

	elif(op == "Media"):
		if(sub == "stories"):
			return (30, 22, 38)
		
		elif(sub == "profile"):
			return (10, 22, 7, 38)

		elif(sub in ("photos", "videos")):
			return (30, 22, 19, 38)

		elif(sub == "direct"):
			return (22, 38)

def display_data(d, h, t, cw=None): # it's None for now until I get every file done
	layout = [[sg.Table(d, h, select_mode="browse", col_widths=cw, num_rows=30, auto_size_columns=False)]]
	window = sg.Window(t, layout, resizable=True, finalize=True)
	while True:
		event, _values = window.read()
		if event is None:
			break


def readjust_ui(op, window, sub_values=None):
	if(op in ("Account History", "Comments")):
		window.Element('sub_column').Update(visible=False)

	elif op is "Connections":
		window.Element('sub_options').Update(value="", values=sub_values)
		window.Element('sub_column').Update(visible=True)

	elif op is "Likes":
		window.Element('sub_options').Update(value="", values=sub_values)
		window.Element('sub_column').Update(visible=True)

	elif op is "Media":
		window.Element('sub_options').Update(value="", values=sub_values)
		window.Element('sub_column').Update(visible=True)


def main_menu():
	secondary_column = [sg.Text("Select an option:", key="sub_options_text"), sg.Combo([""], default_value="", size=(20, 1), enable_events=True, key='sub_options')]
	
	layout = 	[[sg.Text("Select data to browse:"), sg.Combo(const("valid_options"),  enable_events=True, key='options')],
				[sg.Column([secondary_column], visible=False, key="sub_column")]]

	window = sg.Window("Data Reader", layout, size=(400, 400), resizable=True, finalize=True)

	while True:
		event, values = window.read()

		if event is None:
			break
		
		op = values['options'] # not really needed but makes EVERYTHING SHORTER
		sub_op = values['sub_options']
		
		if op == "Account History":
			readjust_ui(op, window)

			# this MAYBE could be put into a function
			with open("account_history.json") as le_file:
				data = load(le_file)
				p_data = [] # processed data
				# getting the actual data
				for x in data["login_history"]:
					p_data.append([*x.values()])

				# display them
				display_data(p_data, headings(op), op, column_widths(op))

		if op == "Comments":
			readjust_ui(op, window) # I think at this point that this should be ousside, how bow da?
			with open("comments.json", encoding="UTF-8") as le_file:
				data = load(le_file)
				for x in data["media_comments"]:
					x[1] = demojize(x[1], use_aliases=True) # because tkinter can't process emojis
				display_data(data["media_comments"], headings(op), op, column_widths(op))

		if op == "Connections": # Not as though as I thought
			readjust_ui(op, window, const("connection_choices"))
			with open("connections.json") as le_file:
				data = load(le_file)
				p_data = [] # name should be changed
				if(sub_op != ""):
					for x, y in data[sub_op].items():
						p_data.append((x, y))
					display_data(p_data, headings(op), sub_op, column_widths(op))

		if op == "Likes":
			readjust_ui(op, window, const("likes_choices"))
			with open("likes.json") as le_file:
				data = load(le_file)
				if(sub_op != ""):
					display_data(data[sub_op], headings(op), sub_op, column_widths(op))

		if op == "Media":
			readjust_ui(op, window, const("media_choices"))
			with open("media.json", encoding="UTF-8") as le_file:
				data = load(le_file)
				if(sub_op != ""):
					p_data = []
					for x in data[sub_op]:
						if(sub_op in ("stories", "photos", "videos")):
							for y in data[sub_op]: # same as for x in data[(sub_op]
								y["caption"] = demojize(y["caption"], use_aliases=True)

						if(sub_op in ("videos", "photos")):
							# kind of a patch
							aux = list(x.values())
							p_data.append([aux[0], aux[1], ("" if len(aux) != 4 else aux[2]), aux[2] if len(aux) == 3 else aux[3]])
						else:
							p_data.append([*x.values()])


					display_data(p_data, headings(op, sub_op), sub_op, column_widths(op, sub_op))		
	# end of While block

	window.close()

# end of main_menu()


def main():
	main_menu()

main()