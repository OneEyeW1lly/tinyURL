from flask import *
import time
import json

app = Flask(__name__)
__website__ = "http://127.0.0.1:5000/"
filename = "./db/urls.json"

class URL:
	def __init__(self, _id, _long):
		try:
			self.long = _long.replace(".www", "")
		except:
			self.long = _long

		self.id = _id
		self.short = ""
		self.json = {}
		self.website = __website__
		self.custom = False
		self.clicks = 0

	def addToDatabase(self):
		if self.id == "0":
			self.custom = False
			self.id = str(int(time.time()))
		else:
			self.custom = True
			self.id = self.id

		self.short = self.website + self.id

		self.json["id"] = self.id
		self.json["long"] = self.long
		self.json["short"] = self.short
		self.json["clicks"] = self.clicks

		with open(filename, "r") as f:
			temp = json.load(f)
			for entry in temp:
				if entry["id"] == self.id and self.custom == True:
					return render_template('index.html', website=__website__, errorMSG="Token already exists")
				elif entry["id"] == self.id and self.custom == False:
					self.id = str(int(time.time()))
				else:
					pass

			temp.append(self.json)
			f.close()

		with open(filename, "w") as f:
			json.dump(temp, f, indent=4)

		return self.short

@app.route("/")
def form():
	return render_template('index.html', website=__website__, errorMSG="")

@app.route("/", methods=["POST"])
def getlong():
	_id = request.form["_id"].replace(" ", "")
	if _id == "" or _id == "0":
		_id = "0"   #str(int(time.time()))
	else:
		_id = _id

	global short
	longUrl = request.form["url"]
	short = URL(_id, longUrl)
	try:
		return render_template('show-shortURL.html', shortURL=short.addToDatabase())
	except:
		return ""

def addClicks(key):
	with open(filename, "r") as f:
		data = json.load(f)

		for entry in data:
			if entry["id"] == key:
				entry["clicks"] += 1
				with open(filename, "w") as w:
					json.dump(data, w, indent=4)
					w.close()
					f.close()

			else:
				pass



@app.route("/<key>")
def opensite(key):
	with open(filename, "r") as f:
		data = json.load(f)

		for entry in data:
			if entry["id"] == key:
				addClicks(entry["id"])
				return redirect(entry["long"])
			else:
				pass

@app.route("/clicks")
def clicks():
	return render_template('clicks.html', clicks="")

@app.route("/clicks", methods=["POST"])
def getClicks():
	short = request.form["short"]

	with open(filename, "r") as f:
		temp = json.load(f)

		for item in temp:
			if item["short"] == short:
				return render_template('show-clicks.html', clicks=str(item["clicks"]))
				f.close()
			else:
				pass

@app.route("/lookup")
def lookup():
	return render_template('lookup.html', long="")

@app.route("/lookup", methods=["POST"])
def lookupLong():
	short = request.form["short"]

	with open(filename, "r") as f:
		temp = json.load(f)

		for item in temp:
			if item["short"] == short:
				return render_template('show-lookup.html', long=item["long"])
				f.close()
			else:
				pass
