import json
		
with open("comments.json") as ah:
	dict = json.load(ah)

with open("comments.json", "w") as ah:
	json.dump(dict, ah, indent=4)

print("Done")