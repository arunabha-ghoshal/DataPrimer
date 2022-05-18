import csv

# implementation of an undirected graph using Adjacency Matrix, with  unweighted edges
class Vertex:
	def __init__(self, n):
		self.name = n

class IPL:
	PlayerTeam = {}
	edges = []
	edge_indices = {}
	
	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.name not in self.PlayerTeam:
			self.PlayerTeam[vertex.name] = vertex
			for row in self.edges:
				row.append(0)
			self.edges.append([0] * (len(self.edges)+1))
			self.edge_indices[vertex.name] = len(self.edge_indices)
			return True
		else:
			return False
	
	def add_edge(self, u, v, weight=1):
		if u in self.PlayerTeam and v in self.PlayerTeam:
			self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
			self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
			return True
		else:
			return False
			
	def print_graph(self):
		for v, i in sorted(self.edge_indices.items()):
			print(v + ' ', end='')
			for j in range(len(self.edges)):
				print(self.edges[i][j], end='')
			print(' ')

	def readInputfile(self,inputfile):
		with open(inputfile,newline='') as f:
			lines =csv.reader(f,delimiter='/')
			for line in lines:
				_iter = len(line) - 1
				rel = []
				for field in line:
					print(field)
					v = Vertex(field.strip())
					self.add_vertex(v)
				for i in range(_iter):
					val = line[0],line[i+1]
					print(val)
					rel.append(val)
				print(rel)
				for r in rel:
					self.add_edge(r[0].strip(),r[1].strip())

	def displayAll(self):
		with open('outputPS10.txt','w') as f:
			f.write('--------Function displayAll--------\n')
			p=0
			t=0
			for i in self.PlayerTeam.keys():
				if len(i)<=4:
					t += 1
				else:
					p += 1
			f.write(f'Total no. of franchises: {t}\n')
			f.write(f'Total no. of players: {p}\n')
			f.write('List of franchises:\n')
			for i in self.PlayerTeam.keys():
				if len(i) <= 4:
					f.write(f'{str(i)}\n')
			f.write('\n\nList of Players:\n')
			for i in self.PlayerTeam.keys():
				if len(i)>4:
					f.write(f'{str(i)}\n')

	def displayFranchises(self, player):
		with open('outputPS10.txt','a') as f:
			f.write('\n\n--------Function displayFranchises --------\n\n')
			f.write(f'Player Name: {player}\n')
			f.write('List of Franchises:\n')
			if player not in self.edge_indices:
				print('the plyer details do not exist in the graph DS')
				f.write('Franchises Not Found\n')
			else:
				edge_index = self.edge_indices[player]
				print('the index: ',edge_index)
				indices = [index for index, element in enumerate(self.edges[edge_index]) if element == 1]
				for key,val in self.edge_indices.items():
					for i in indices:
						if val == i:
							f.write(f'{key.strip()}\n')
	
	def displayPlayers(self, franchise):
		with open('outputPS10.txt','a') as f:
			f.write('\n\n--------Function displayPlayers--------\n\n')
			f.write(f'Franchise Name: {franchise}\n')
			f.write('List of Players:\n')
			if franchise not in self.edge_indices:
				print('the plyer details do not exist in the graph DS')
				f.write('Players Not Found\n')
			else:
				edge_index = self.edge_indices[franchise]
				print('the index: ',edge_index)
				indices = [index for index, element in enumerate(self.edges[edge_index]) if element == 1]
				for key,val in self.edge_indices.items():
					for i in indices:
						if val == i:
							f.write(f'{key.strip()}\n')

	def franchiseBuddies(self, playerA, playerB):
		if playerA not in self.edge_indices or playerB not in self.edge_indices:
			print('One or more players not found in the graph')
			return None
		with open('outputPS10.txt','a') as f:
			f.write('\n\n--------Function franchiseBuddies--------\n\n')
			f.write(f'Player A: {playerA}\n')
			f.write(f'Player B: {playerB}\n')
			edge_indexA = self.edge_indices[playerA]
			edge_indexB = self.edge_indices[playerB]
			indicesA = [index for index, element in enumerate(self.edges[edge_indexA]) if element == 1]
			indicesB = [index for index, element in enumerate(self.edges[edge_indexB]) if element == 1]
			#bud = [i for i, j in zip(indicesA, indicesB) if i == j]
			bud = list(set(indicesA) & set(indicesB))
			if len(bud) == 0:
				print(f'{playerA} and {playerB} have not played for same team')
				f.write(f'Franchise Buddies: No, {playerA} and {playerB} have not played for same team\n')
			else:
				msg = 'Franchise Buddies: Yes '
				for key,val in self.edge_indices.items():
					for i in bud:
						if val == i:
							msg += f', {key.strip()} '
				f.write(f'{msg}\n')

	def findPlayerConnect(self, playerA, playerB):
		if playerA not in self.edge_indices or playerB not in self.edge_indices:
			print('One or more players not found in the graph')
			return None
		with open('outputPS10.txt','a') as f:
			f.write('\n\n--------Function findPlayerConnect --------\n\n')
			f.write(f'Player A: {playerA}\n')
			f.write(f'Player B: {playerB}\n')
			edge_indexA = self.edge_indices[playerA]
			edge_indexB = self.edge_indices[playerB]
			indicesA = [index for index, element in enumerate(self.edges[edge_indexA]) if element == 1]
			indicesB = [index for index, element in enumerate(self.edges[edge_indexB]) if element == 1] 
			for i in indicesA:
				for j in indicesB:
					playersA = [index for index, element in enumerate(self.edges[i]) if element == 1]
					playersB = [index for index, element in enumerate(self.edges[j]) if element == 1]
					connect = list(set(playersA) & set(playersB))
					if len(connect) >= 1 :
						for key,val in self.edge_indices.items():
							if val == connect[0]:
								playerC = key.strip()
							if val == i:
								teamA = key.strip()
							if val == j:
								teamB = key.strip()
						f.write(f'Related: Yes, {playerA} > {teamA} > {playerC} > {teamB} > {playerB}\n')
						return True
			print(f'There is no connection between {playerA} and {playerB}')
			f.write(f'Related: No, here is no connection between {playerA} and {playerB}')

		
	def destroyGraph(self):
		self.PlayerTeam = {}
		self.edges = []
		self.edge_indices = {}




# to create a IPL object:
ipl = IPL()

#to insert data from inputPS10.txt to the graph DS
ipl.readInputfile('inputPS10.txt')

#to print the graph
ipl.print_graph()

#to create the outputPS10.txt for the 1st time:
ipl.displayAll()

#to perform all the operation by reading data from promptsPS10.txt
with open('promptsPS10.txt',newline='') as f:
    lines =csv.reader(f,delimiter=':')
    for line in lines:
        if line[0].strip() == 'findFranchise':
            ipl.displayFranchises(line[1].strip())
        if line[0].strip() == 'listPlayers':
            ipl.displayPlayers(line[1].strip())
        if line[0].strip() == 'franchiseBuddies':
            ipl.franchiseBuddies(line[1].strip(),line[2].strip())
        if line[0].strip() == 'playerConnect':
            ipl.findPlayerConnect(line[1].strip(),line[2].strip())


# to destroy the graph DS
ipl.destroyGraph()