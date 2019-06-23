import math

mods = {'noMod': 0,
		'Easy': 1,
		'HardRock': 2,
		'HalfTime': 4,
		'DoubleTime': 8,
		'Hidden': 16,
		'FlashLight': 32,
		'NoFail': 64 }

def getHW(od: float, enabledMods):
	newOd = od

	if enabledMods & mods['Easy']:
		newOd /= 2
	
	if enabledMods & mods['HardRock']:
		newOd *= 1.4
	
	if enabledMods & mods['DoubleTime']:
		newOd = newOd / 1.5 + 5.5
	
	if enabledMods & mods['HalfTime']:
		newOd = newOd / 0.75 - 5.5
	
	return round(49.5 - (newOd / 0.5) * 1.5, 1)

def getHundreds(maxcombo: int, misses: int, acc: float):
	return round((1 - misses / maxcombo - acc / 100) * 2 * maxcombo)

def calcPP(stars: float, maxcombo: int, combo: int, hundreds: int, misses: int, acc: float, od: float, enabledMods):
	hitWindow = getHW(od, enabledMods)

	strainVal = max(1.0, stars / 0.0075) * 5.0 - 4.0
	strainVal = math.pow(strainVal, 2) / 100000.0

	lenBonus = min(1.0, maxcombo / 1500.0) * 0.1 + 1.0
	strainVal *= lenBonus * math.pow(0.985, misses)

	strainVal *= min(math.sqrt(combo) / math.sqrt(maxcombo), 1.0)

	if enabledMods & mods['Hidden']:
		strainVal *= 1.025
	
	if enabledMods & mods['FlashLight']:
		strainVal *= 1.05 * lenBonus
	
	strainVal *= acc / 100

	# print(f'Strain value: {strainVal}')

	accVal = math.pow(150.0 / hitWindow, 1.1)
	accVal *= math.pow(acc / 100, 15) * 22.0
	accVal *= min(math.pow(maxcombo / 1500.0, 0.3), 1.15)

	# print(f'Accuracy value: {accVal}')

	multiplier = 1.1

	if enabledMods & mods['NoFail']:
		multiplier *= 0.9
	
	if enabledMods & mods['Hidden']:
		multiplier *= 1.1
	
	totalPP = math.pow(math.pow(strainVal, 1.1) + math.pow(accVal, 1.1), 1.0 / 1.1) * multiplier

	return totalPP