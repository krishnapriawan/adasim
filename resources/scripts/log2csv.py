# Script: run-sim.py
# Purpose: Runs a number of randomly generated simulations. 
# Author: Jochen Wuttke, wuttkej@gmail.com
# Date:
#
# The number and kind of simulations to run are defined in a simple text file.
# The script takes a filename as argument

import argparse
import sys
import subprocess
import xml.dom.minidom
import os
import re

class CarData:
	id = ""
	path = []
	path_length = 0
	hops = 0
	time = 0
	strategy = ""
	invalid_move = False

def parse_arguments():
	'''
	Parse and return the command line arguments.
	'''
	parser = argparse.ArgumentParser(description='Data directory and output file')
	parser.add_argument('-d', dest='DATA_DIR', required=True, help='Directory containing simulation config and output.')
	return parser.parse_args()

def process_path(line):
	#print line
	split_re = re.compile(r'.+Vehicle: (\d+).+\[(.*)]')
	result = split_re.match(line)
	car_id = result.group(1)
	#print "ID: " + car_id
	path = result.group(2)
	#print "Path: " + path
	car = CarData()
	car.id = car_id
	car.path = path
	car.path_length = len(path.split(', '))
	return car

def process_move(line):
	split_re = re.compile(r'.+Vehicle: (\d+).+')
	return split_re.match(line).group(1)

def process_log(file, prefix, cars):
	time = 0
	path_re = re.compile(".+- PATH: .+")
	move_re = re.compile(".+MOVE: .+")
	stop_re = re.compile(".+STOP: .+")
	time_re = re.compile(".+SIMULATION: .+" )
	invalid_re = re.compile(".+INVALID: .+" )

	for line in file:
		# print('line', line, prefix)
		if path_re.match( line ):
			car = process_path(line)
			car.id = car.id + prefix
			cars[ car.id ] = car
		elif move_re.match(line):
			moved_car_id = process_move(line) + prefix
			cars[moved_car_id].hops = cars[moved_car_id].hops + 1
			
		elif stop_re.match(line):
			moved_car_id = process_move(line) + prefix
			# print('moved car id ', moved_car_id)
			cars[moved_car_id].time = time
			
		elif time_re.match(line):
			time += 1
		
		elif invalid_re.match(line):
			invalid_id = process_move(line) + prefix
			cars[invalid_id].invalid_move = True
	return cars

def process_xml(file, prefix, cars):
	doc = xml.dom.minidom.parse(file)
	car_nodes = doc.documentElement.getElementsByTagName("car")
	cars_node = doc.documentElement.getElementsByTagName("cars")[0]
	def_strat = cars_node.getAttribute("default_strategy")
	for car in car_nodes:
		# print ("Car " + car.getAttribute("id") + " Strategy: " + car.getAttribute("strategy") )
		car_id = car.getAttribute("id") + prefix
		if car_id in cars:
			cars[car_id].strategy = car.getAttribute("strategy") 
	return cars

def filename_filter(files, regex):
	r = re.compile(regex)
	filtered = []
	for file in files:
		result = r.match(file)
		if result:
			filtered.append(result.group(1))
	return filtered

def process_files(dir, files, prefix):
	cars = {}
	print ("Checking " + dir + "/" + prefix)
	for file in filename_filter( files, "(" + prefix + "-.+)\.xml"):
		print ("\t Processing " + file)
		log_file = open( dir + "/" + file + ".log" )
		xml_file = open( dir + "/" + file + ".xml" )
		cars = process_log(log_file, file, cars)
		cars = process_xml(xml_file, file, cars)
	return cars

def write_line( file, nums, car):
	write_line2( file, nums[0] , nums[1] , car.id , str(car.hops) , 
		str(car.invalid_move), str(car.time), car.strategy ) 

def write_line2( file, nodes, cars, id, pl, invalid, time, strategy):
	file.write( nodes + "," + cars + "," + id + "," + 
		pl + "," + invalid + "," + time + "," + strategy + "\n") 
	

def write_cars(file, prefix, cars):
	nums = prefix.split('-')
	for car in cars.values():
		write_line(file, nums, car)

def get_prefixes(files):
	r = re.compile(r'(\d+-\d+)-\d+.xml')
	prefixes = set()
	for file in files:
		result = r.match(file)
		if result:
			prefixes.add(result.group(1))
	return list(prefixes)

def main(args):
	'''Main cycle'''
	files = os.listdir( args.DATA_DIR )
	all_output_file = open("all.csv", "w")
	write_line2(all_output_file, "Nodes", "Cars", "Car", "Hops", "Invalid", "Time", "Strategy" )
	for prefix in get_prefixes(files):
		output_file = open( prefix + ".csv", "w")
		write_line2(output_file, "Nodes", "Cars", "Car", "Hops", "Invalid", "Time", "Strategy" )
		cars = process_files(args.DATA_DIR, files, prefix )
		write_cars(output_file, prefix, cars)
		write_cars(all_output_file, prefix, cars)
		output_file.close()
	all_output_file.close()


if __name__ == "__main__":
	args = parse_arguments()
	ret = main(args)

