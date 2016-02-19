
#Program to make a create a 1-player game of Hammurabi.
import random

def print_intro():
	'''
	Introduce the user to the game and rules
	'''
	print '''Congrats, you are the newest ruler of ancient Samaria, elected for a ten year term of office. Your duties are to distribute food, direct farming, and buy and sell land as needed to support your people. Watch out for rat infestations and the resultant plague! Grain is the general currency, measured in bushels. The following will help you in your decisions:
	(a) Each person needs at least 20 bushels of grain per year to survive.
	(b) Each person can farm at most 10 acres of land.
	(c) It takes 2 bushels of grain to farm an acre of land.
	(d) The market price for land fluctuates yearly.
	Rule wisely and you will be showered with appreciation at the end of your term. Rule poorly and you will be kicked out of office'''
def Hammurabi():
	'''
	Ask user for inputs and update the user every year based on his inputs. This is the main function which calls all the other functions.
	'''
	# Initializing variables for Year 1
	starved = 0
	immigrants = 5
	population = 100
	harvest = 3000 # total bushels harvested
	bushels_per_acre = 3 # amount harvested for each acre planted
	rats_ate = 200 # bushels destroyed by rats
	bushels_in_storage = 2800
	acres_owned = 1000
	cost_per_acre = 19 # each acre costs this many bushels
	plague_deaths = 0
	total_starved = 0
	#num_years = 11 # Used for testing only

# Introduce user to the rules
	print_intro()

# Status update for the user every year
	for i in range (1,11):
		print "O great Hammurabi! \n You are in year", i, "of your ten year rule.", "\n In the previous year", starved, "people starved to death.", "\n In the previous year", immigrants, "people entered the kingdom.", "\n The population is now", population, "\n We harvested", harvest, "bushels at", bushels_per_acre, "bushels per acre.", "\n Rats destroyed", rats_ate, "bushels, leaving", bushels_in_storage, "bushels in storage.", "\n The city owns", acres_owned, "acres of lands.", "\n Land is currently worth", cost_per_acre, "bushels per acre.", "\n There were", plague_deaths, "deaths from the plague."

		# Updating land owned by the city based on user input
		acres_bought = ask_to_buy_land(bushels_in_storage, cost_per_acre)
		if acres_bought == 0:
			acres_sold = ask_to_sell_land(acres_owned)
		else:
			acres_sold = 0
		acres_owned = acres_owned + acres_bought - acres_sold
		bushels_in_storage = bushels_in_storage - cost_per_acre*acres_bought + cost_per_acre*acres_sold

		#Updating the bushels fed to the population based on user input
		bushels_fed = ask_to_feed(bushels_in_storage)
		bushels_in_storage = bushels_in_storage - bushels_fed

		#Updating the acres cultivated  based on user input
		land_to_cultivate = ask_to_cultivate(acres_owned,population,bushels_in_storage)
		bushels_in_storage = bushels_in_storage - land_to_cultivate

		#Updating population for next year
		#Step 1: Updating population with plague condition
		if is_plague():
			plague_deaths = population / 2
			population = population / 2
		else:
			plague_deaths = 0
			

		#Step 2: Finding the number of people who starved
		starved = num_starving(population,bushels_fed)
		population = population - starved
		#Game over if starvation levels are too high
		if starved > 0.45 * population:
			print "Your rule sucketh much. So much starvation! Leave now before the citizens catch you."
			exit()

		#Step 3: Calculating number of immigrants to the city
		immigrants = num_immigrants(acres_owned, bushels_in_storage, population, starved)
		population = population + immigrants

		#Updating food supplies for next year
		#Step 1: Calculating amount of harvest in the year
		bushels_per_acre = get_harvest()
		harvest = bushels_per_acre * land_to_cultivate
		bushels_in_storage = bushels_in_storage + harvest

		#Step 2: Calculating damages from rat infestation
		percent_grain_destroyed = do_rats_infest() * percent_destroyed() / 100
		rats_ate = bushels_in_storage * percent_grain_destroyed
		bushels_in_storage = bushels_in_storage - rats_ate

		#Updating price of land every year
		cost_per_acre = price_of_land()

		#Updating variables for calculating average starvation as a metric of performance
		total_starved = total_starved + starved

	#Updating final performance parameters
	land_per_person = acres_owned / population
	average_starved = total_starved / 10

	#Prints the final summary of the user's performance
	print_summary(average_starved, land_per_person)


def ask_to_buy_land(bushels, cost):
	'''Ask user how many bushels to spend buying land.'''
	acres_to_buy = input("How many acres will you buy? ")
	while acres_to_buy * cost > bushels:
		print "O great Hammurabi, we have but", bushels, "bushels of grain!"
		acres_to_buy = input("How many acres will you buy? ")
	return acres_to_buy

def ask_to_sell_land(acres):
	'''Ask user how much land they want to sell'''
	acres_to_sell = input("How many acres will you sell? ")
	while acres_to_sell > acres:
		print "O great Hammurabi, we have but", acres, "acres of land"
		acres_to_sell = input("How many acres will you sell? ")
	return acres_to_sell

def ask_to_feed(bushels):
	'''Ask user how many bushels they want to use for feeding'''
	bushels_to_feed = input("How many bushels do you wish to feed your people? ")
	while bushels_to_feed > bushels:
		print "O great Hammurabi, we have but", bushels, "in storage"
		bushels_to_feed = input("How many bushels do you wish to feed your people? ")
	return bushels_to_feed

def ask_to_cultivate(acres, population, bushels):
	'''Ask user how much land they want to plant seeds in'''
	land_to_cultivate = input("How many acres do you wish to plant with seeds?")
	while land_to_cultivate > acres:
		print "O great Hammurabi, we have but", acres, "acres of land"
		land_to_cultivate = input("How many acres do you wish to plant with seeds?")
	while land_to_cultivate > population*10:
		print "O great Hammurabi, we have but", population, "people"
		land_to_cultivate = input("How many acres do you wish to plant with seeds?")
	while land_to_cultivate > bushels:
		print "O great Hammurabi, we have but", bushels, "bushels to plant"
		land_to_cultivate = input("How many acres do you wish to plant with seeds?")
	return land_to_cultivate

def is_plague():
	'''Determine whether a plague hits the city'''
	chance = random.randint(1,100)
	if chance <= 15:
		return True
	else:
		return False

def num_starving(population, bushels):
	''' Determine the number of people who starved in a year'''
	starved = max(0, population - bushels/20)
	return starved

def num_immigrants(land, grain_in_storage, population, num_starving):
	'''Determine the number of immigrants to the city'''
	if num_starving > 0:
		return 0
	else:
		immigrants = (20 * land + grain_in_storage) / (100 * population + 1)
		return immigrants

def get_harvest():
	'''Determine the level of harvest in the city from 1 to 8'''
	harvest_level = random.randint(1,8)
	return harvest_level

def do_rats_infest():
	'''Check whether rats infested in that year or not'''
	chance = random.randint(1,100)
	if chance <= 40:
		return True
	else:
		return False

def percent_destroyed():
	'''Determine the level of destruction by rats'''
	percent_grain = random.randint(10,30)
	return percent_grain

def price_of_land():
	'''Determine the per acre price of land to buy or sell'''
	price = random.randint(16,22)
	return price

def print_summary(starvation, prosperity):
	'''Prints the summary message at the end of the game'''
	print "Average starvation under your rule was", starvation, "deaths, and average land per person after your rule is", prosperity, "acres"
	if starvation < 3:
		if prosperity > 10:
			print "Great job, not only did you keep starvation under checks, you also increased prosperity."
		elif prosperity < 10:
			print "Average job. While you kept starvation under control, you could have done better on prosperity"
	else:
		print "Below average performance. Starvation levels were too high in your reign."

if __name__ == '__main__':
	Hammurabi()

