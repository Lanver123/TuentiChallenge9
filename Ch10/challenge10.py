import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


class Moon:
	def __init__(self, moonID, planetDistance, radialPos, orbitalPer,  material):
		self.moonID = moonID
		self.orbitalPer = orbitalPer
		self.planetDistance = planetDistance
		self.radialPos = radialPos
		self.material = material

	def __repr__(self):
		return ("%i %f %i" % (self.moonID, self.radialPos, self.material))

	def __str__(self):
		return ("%i %i" % (self.moonID, self.material))


def hierarchy_pos(G, root, levels=None, width=1., height=1.):
	'''If there is a cycle that is reachable from root, then this will see infinite recursion.
	   G: the graph
	   root: the root node
	   levels: a dictionary
			   key: level number (starting from 0)
			   value: number of nodes in this level
	   width: horizontal space allocated for drawing
	   height: vertical space allocated for drawing'''
	TOTAL = "total"
	CURRENT = "current"

	def make_levels(levels, node=root, currentLevel=0, parent=None):
		"""Compute the number of nodes for each level
		"""
		if not currentLevel in levels:
			levels[currentLevel] = {TOTAL: 0, CURRENT: 0}
		levels[currentLevel][TOTAL] += 1
		neighbors = G.neighbors(node)
		for neighbor in neighbors:
			if not neighbor == parent:
				levels = make_levels(levels, neighbor, currentLevel + 1, node)
		return levels

	def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
		dx = 1/levels[currentLevel][TOTAL]
		left = dx/2
		pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
		levels[currentLevel][CURRENT] += 1
		neighbors = G.neighbors(node)
		for neighbor in neighbors:
			if not neighbor == parent:
				pos = make_pos(pos, neighbor, currentLevel +
							   1, node, vert_loc-vert_gap)
		return pos
	if levels is None:
		levels = make_levels({})
	else:
		levels = {l: {TOTAL: levels[l], CURRENT: 0} for l in levels}
	vert_gap = height / (max([l for l in levels])+1)
	return make_pos({})


def readProcessInputs():
	moonDistances = [
		float(distance) for distance in inputFile.readline().replace("\n", "").split()]
	posicionesRadiales = [
		float(radialPos) for radialPos in inputFile.readline().replace("\n", "").split()]
	periodosOrbitales = [float(
		orbitalPer) for orbitalPer in inputFile.readline().replace("\n", "").split()]
	cantidadRecolectar = [
		int(material) for material in inputFile.readline().replace("\n", "").split()]
	moonsInfo = list(zip(moonDistances, posicionesRadiales,
						 periodosOrbitales, cantidadRecolectar))
	moons = {}
	i = 1
	for moonInfo in moonsInfo:
		moons[i] = (Moon(i, moonInfo[0], moonInfo[1],
						 moonInfo[2], moonInfo[3]))
		i += 1
	moons[0] = Moon(0, 0, 0, 0, 0)
	return moons


def distanciaLunas(moon1, moon2):
	x = np.array([np.cos(moon1.radialPos)*moon1.planetDistance,
				  np.sin(moon1.radialPos)*moon1.planetDistance])
	y = np.array([np.cos(moon2.radialPos)*moon2.planetDistance,
				  np.sin(moon2.radialPos)*moon2.planetDistance])
	return np.linalg.norm(x-y)


def desfaseTemporal(moon1):
	if moon1.moonID == 0:
		return moon1
	velocidadAngular = 2*3.14 / moon1.orbitalPer	
	posicionFinal = (moon1.radialPos + velocidadAngular * 6) % 2*3.14
	moon1.radialPos = posicionFinal
	return moon1


def primerSalto(diGraph, moons, distanciaSaltoMax, currentNode, capacidadNave):
	for moon in moons.values():
		if moons[currentNode[0]] == moon.moonID:
			continue
		dist = distanciaLunas(Moon(0, 0, 0, 0, 0), moon)
		if distanciaSaltoMax >= dist and currentNode[1]+moon.material <= capacidadNave:
			nextNode = (moon.moonID, currentNode[1]+moon.material)
			diGraph.add_edge(currentNode, nextNode, weight=0)
			siguienteSalto(diGraph, moons, distanciaSaltoMax, nextNode, [], capacidadNave)


def siguienteSalto(diGraph, moons, distanciaSaltoMax, currentNode, visitados, capacidadNave):

	lunaCurrentNode = moons[currentNode[0]]
	for visitado in visitados:
		if visitado[0] == currentNode[0]:
			return
	# Si has vuelto al planeta, fin
	if currentNode[0] != 0:
		visitados += [currentNode]
		# Ya has saltado, se aplica desfase temporal
		for moonId in moons.keys():
			moons[moonId] = desfaseTemporal(moons[moonId])
		for moon in moons.values():
			if lunaCurrentNode.moonID == moon.moonID:
				continue
			dist = distanciaLunas(lunaCurrentNode, moon)
			if distanciaSaltoMax >= dist and currentNode[1]+moon.material <= capacidadNave:
				nextNode = (moon.moonID, currentNode[1]+moon.material)
				diGraph.add_edge(currentNode, nextNode, weight=lunaCurrentNode.material)
				siguienteSalto(diGraph, moons, distanciaSaltoMax,
							   nextNode, visitados, capacidadNave)


if __name__ == "__main__":
	inputFile = open(sys.argv[1], "r")
	writeFile = open("out.txt", "w")
	cases = int(inputFile.readline())
	for case in range(1, cases+1):
		numberMoons = int(inputFile.readline())
		moons = readProcessInputs()
		capacidadNave = int(inputFile.readline().replace("\n", ""))
		distanciaSaltoMax = float(inputFile.readline().replace("\n", ""))

		diGraph = nx.DiGraph()
		# 1: Planeta ini como nodo inicial
		firstNode = (0, 0)
		primerSalto(diGraph, moons, distanciaSaltoMax, firstNode, capacidadNave)

		# Remove leaves not root and not planet
		ciclos = nx.find_cycle(diGraph, firstNode)
		diGraph.remove_edges_from(ciclos)
		leaves = [leave for leave in diGraph.nodes() if diGraph.out_degree(
			leave) == 0 and diGraph.in_degree(leave) == 1 and leave[0] != 0]
		diGraph.remove_nodes_from(leaves)

		pos = hierarchy_pos(diGraph, firstNode)
		nx.draw(diGraph, pos, with_labels=False, node_size=10, font_size=10)
		labels = nx.get_edge_attributes(diGraph, 'weight')
		nx.draw_networkx_edge_labels(diGraph, pos, edge_labels=labels)
		# plt.savefig('hierarchy.png')
		plt.show()
		
		longestPath = nx.dag_longest_path(diGraph)
		toPrint = "Case #%i:" % case

		listaMateriales = [moons[node[0]].material for node in longestPath if moons[node[0]].material != 0]
		listaMateriales = sorted(listaMateriales)
		if len(listaMateriales) == 0:
			toPrint += " None"
		else:
			for mat in listaMateriales:
				toPrint += " %i" % mat
		toPrint += "\n"
		print(toPrint)
		writeFile.write(toPrint)
