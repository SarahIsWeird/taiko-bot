import math

# The list of possible mods.
mods = {
	'noMod': 0,
	'NoFail': 1,
	'Easy': 2,
	'Hidden': 8,
	'HardRock': 16,
	'DoubleTime': 64,
	'HalfTime': 256,
	'Flashlight': 1024,
	'Nightcore': 64, # Technically not API-compliant, but nightcore is only set alongside DoubleTime, anyways.
	'NF': 1,
	'EZ': 2,
	'HD': 8,
	'HR': 16,
	'DT': 64,
	'HT': 256,
	'FL': 1024,
	'NC': 64
}

def getModString(modVal: int):
	modStr = ''
	for mod in mods: # Loop through the mods and change the modsVal according to the enabled mods.
		if mods[mod] & modVal:
			modVal -= mods[mod]
			modStr = ' '.join([modStr, f'+{mod}'])
	
	return modStr

def getModVal(modString: int):
	modVal = 0
	
	modString = modString.lower()

	for mod in mods:
		if modString.find(mod.lower()) != -1:
			modVal += mods[mod]
	
	return modVal

# Scaling for the HP and OD values is the same.
def scaleHPOD(hpod: float, enabledMods):
	newOd = hpod

	if enabledMods & mods['Easy']:
		newOd /= 2
	
	if enabledMods & mods['HardRock']:
		newOd *= 1.4
	
	if enabledMods & mods['DoubleTime']:
		newOd = newOd / 1.5 + 5.5
	
	if enabledMods & mods['HalfTime']:
		newOd = newOd / 0.75 - 5.5
	
	if newOd > 10:
		newOd = 10
	
	return round(newOd, 1)

# Calculate the hit window for a perfect hit (300) in ms depending on the enabled mods using the OD (Overall Difficulty).
def getHW(od: float, enabledMods):	
	return round(49.5 - (round(od, 2) / 0.5) * 1.5, 1)

# Given the maximum combo, misses and the accuracy, this calculates the number of bad hits (100s).
def getHundreds(maxcombo: int, misses: int, acc: float):
	return round((1 - misses / maxcombo - acc / 100) * 2 * maxcombo)

# Does the actual pp calculation. For more info on this, please refer to the forum post linked in the README.md file.
# There isn't a whole lot to explain here, just doing the calculations, really!
def calcPP(stars: float, maxcombo: int, combo: int, hundreds: int, misses: int, acc: float, od: float, enabledMods):
	hitWindow = getHW(od, enabledMods)

	# Strain value calculation
	strainVal = max(1.0, stars / 0.0075) * 5.0 - 4.0
	strainVal = math.pow(strainVal, 2) / 100000.0

	lenBonus = min(1.0, maxcombo / 1500.0) * 0.1 + 1.0
	strainVal *= lenBonus
	
	strainVal *= math.pow(0.985, misses)

	strainVal *= min(math.sqrt(combo) / math.sqrt(maxcombo), 1.0)

	if enabledMods & mods['Hidden']:
		strainVal *= 1.025
	
	if enabledMods & mods['Flashlight']:
		strainVal *= 1.05 * lenBonus
	
	strainVal *= acc / 100

	# Accuracy value calculation (NOT the same as the accuracy ingame!)
	accVal = math.pow(150.0 / hitWindow, 1.1)
	accVal *= math.pow(acc / 100, 15) * 22.0
	accVal *= min(math.pow(maxcombo / 1500.0, 0.3), 1.15)

	# Final pp calculation
	multiplier = 1.1

	if enabledMods & mods['NoFail']:
		multiplier *= 0.9
	
	if enabledMods & mods['Hidden']:
		multiplier *= 1.1
	
	totalPP = math.pow(math.pow(strainVal, 1.1) + math.pow(accVal, 1.1), 1.0 / 1.1) * multiplier

	return totalPP