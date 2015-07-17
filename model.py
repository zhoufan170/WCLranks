import requests
from bs4 import BeautifulSoup
import json
import re

def get_fights_from_log_id(log_id):
	r = requests.get("https://www.warcraftlogs.com/reports/fights_and_participants/"+log_id+"/0")
	r = json.loads(r.text)
	return r

def find_boss_fights(r, log_id):
	kills = []
	fights = r["fights"]
	for i in fights:
		if i["boss"] != 0:
			if i["bossPercentage"] == 0:
				boss_dict = {}
				boss_dict["boss_id"] = i["boss"]
				boss_dict["fight_id"] = i["id"]
				boss_dict["boss_name"] = i["name"]
				boss_dict["url"] = "https://www.warcraftlogs.com/rankings/report_rankings_for_fight/"+str(log_id)+"/"+str(boss_dict["fight_id"])+"/"+str(boss_dict["boss_id"])
				kills.append(boss_dict)
	return kills

def scrape_rankings(kills):
	rankings = {}
	rankings["tank"] = {}
	rankings["dps"] = {}
	rankings["hps"] = {}
	rankings["guild"] = {}
	for kill in kills:
		r=requests.get(kill["url"])
		soup = BeautifulSoup(r.text, "html5lib")
		data = dps_rankings(soup, rankings, kill["boss_id"])
		data = hps_rankings(soup, rankings, kill["boss_id"])
		data = tank_rankings(soup, rankings, kill["boss_id"])
		data = guild_rankings(soup, rankings, kill["boss_id"])
	return data

def dps_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[3]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["dps"]:
			rankings["dps"][name] = {}
			rankings["dps"][name]["class"] = link['class'][0]
			if rankings["dps"][name]["class"] == "DeathKnight":
				rankings["dps"][name]["class"] = "Death Knight"
			rankings["dps"][name]["spec_path"] = spec_path
			rankings["dps"][name]["spec"] = spec
			rankings["dps"][name]["rank"] = {}
			rankings["dps"][name]["damage"] = {}
			rankings["dps"][name]["bracket"] = {}
			rankings["dps"][name]["br_rank"] = {}
			rankings["dps"][name]["ilvl"] = {}
		rankings["dps"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		rankings["dps"][name]["damage"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["dps"][name]["ilvl"][boss_id] = row.findAll("td")[6].contents[0]
		rankings["dps"][name]["bracket"][boss_id] = row.findAll("td")[7].contents[0]
		rankings["dps"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		if rankings["dps"][name]["spec"] != spec:
			rankings["dps"][name]["spec"] = "Multiple"
	return rankings


def hps_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[4]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["hps"]:
			rankings["hps"][name] = {}
			rankings["hps"][name]["class"] = link['class'][0]
			rankings["hps"][name]["spec_path"] = spec_path
			rankings["hps"][name]["spec"] = spec
			rankings["hps"][name]["rank"] = {}
			rankings["hps"][name]["healing"] = {}
			rankings["hps"][name]["bracket"] = {}
			rankings["hps"][name]["br_rank"] = {}
			rankings["hps"][name]["ilvl"] = {}
		rankings["hps"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		rankings["hps"][name]["healing"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["hps"][name]["ilvl"][boss_id] = row.findAll("td")[6].contents[0]
		rankings["hps"][name]["bracket"][boss_id] = row.findAll("td")[7].contents[0]
		rankings["hps"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		if rankings["hps"][name]["spec"] != spec:
			rankings["hps"][name]["spec"] = "Multiple"
	return rankings

def tank_rankings(soup, rankings, boss_id):
	table = soup.findAll("table")[2]
	for row in table.findAll("tr")[1:]:
		link = row.findAll("a")[0]
		name = link.contents[0]
		spec_path = row.findAll("img")[0]["src"]
		spec = re.findall( '-(.*?).jpg', spec_path)[0]
		if name not in rankings["tank"]:
			rankings["tank"][name] = {}
			rankings["tank"][name]["class"] = link['class'][0]
			if rankings["dps"][name]["class"] == "DeathKnight":
				rankings["dps"][name]["class"] = "Death Knight"
			rankings["tank"][name]["spec_path"] = spec_path
			rankings["tank"][name]["spec"] = spec
			rankings["tank"][name]["rank"] = {}
			rankings["tank"][name]["healing"] = {}
			rankings["tank"][name]["bracket"] = {}
			rankings["tank"][name]["br_rank"] = {}
			rankings["tank"][name]["ilvl"] = {}
		rankings["tank"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
		rankings["tank"][name]["healing"][boss_id] = row.findAll("td")[5].contents[0]
		rankings["tank"][name]["ilvl"][boss_id] = row.findAll("td")[6].contents[0]
		rankings["tank"][name]["bracket"][boss_id] = row.findAll("td")[7].contents[0]
		rankings["tank"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
		if rankings["tank"][name]["spec"] != spec:
			rankings["tank"][name]["spec"] = "Multiple"
	return rankings

def guild_rankings(soup, rankings, boss_id):
	# table = soup.findAll("table")[2]
	# for row in table.findAll("tr")[1:]:
	# 	link = row.findAll("a")[0]
	# 	name = link.contents[0]
	# 	spec_path = row.findAll("img")[0]["src"]
	# 	spec = re.findall( '-(.*?).jpg', spec_path)[0]
	# 	if name not in rankings["tank"]:
	# 		rankings["tank"][name] = {}
	# 		rankings["tank"][name]["class"] = link['class'][0]
	# 		rankings["tank"][name]["spec_path"] = spec_path
	# 		rankings["tank"][name]["spec"] = spec
	# 		rankings["tank"][name]["rank"] = {}
	# 		rankings["tank"][name]["healing"] = {}
	# 		rankings["tank"][name]["bracket"] = {}
	# 		rankings["tank"][name]["br_rank"] = {}
	# 		rankings["tank"][name]["ilvl"] = {}
	# 	rankings["tank"][name]["rank"][boss_id] = row.findAll("td")[0].contents[0]
	# 	rankings["tank"][name]["healing"][boss_id] = row.findAll("td")[5].contents[0]
	# 	rankings["tank"][name]["ilvl"][boss_id] = row.findAll("td")[6].contents[0]
	# 	rankings["tank"][name]["bracket"][boss_id] = row.findAll("td")[7].contents[0]
	# 	rankings["tank"][name]["br_rank"][boss_id] = row.findAll("td")[8].contents[0]
	# 	if rankings["tank"][name]["spec"] != spec:
	# 		rankings["tank"][name]["spec"] = "Multiple"
	return rankings

def analyze(log_id):
	response = get_fights_from_log_id(log_id)
	kills = find_boss_fights(response, log_id)
	details = scrape_rankings(kills)
	return kills, details

