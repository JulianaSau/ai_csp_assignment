
domains = []
neighbours = []
cities = []

j = int(input("Enter number of cities: "))
for i in range(j):
    adjacent = []
    colors = []
    city = input("Enter city: ")
    k = int(input("Enter number of neighbours: "))
    for a in range(k):
        neighbour = input("Enter neighbour: ")
        adjacent.append(neighbour)
    l = int(input("Enter number of colors: "))
    for a in range(l):
        color = input("Enter color: ")
        colors.append(color)
    cities.append(city)
    neighbours.append(adjacent)
    domains.append(colors)

solution = { }
agenda = []

def agenda_filling():
    for kota in cities:
        varIndex = cities.index(kota)
        for constraints in neighbours[varIndex]:
            agenda.append([kota, constraints])
    print("Initial Agenda List:")
    print(agenda)

def check_adjacent(xi,xj):
    temp = False
    xi_index = cities.index(xi)
    for x in domains[xi_index]:
        if xj not in neighbours[xi_index]:
            break
        elif xj not in solution:
            continue
        elif x in solution[xj]:
            domains[xi_index].remove(x) 
            temp = True
    if not temp and len(domains[xi_index]) > 0:
        solution[xi] = domains[xi_index][0]
    return temp

def arc_consistency():
    agenda_filling()
    while agenda:
        agenda_arc = agenda.pop(0)
        if check_adjacent(agenda_arc[0], agenda_arc[1]):
            city_index = cities.index(agenda_arc[0])
            if len(domains[city_index]) == 0:
                print ("ERROR! Can Not Be Solve!")
                return False
            tetangga = list(neighbours[city_index])
            tetangga.remove(agenda_arc[1])
            for xk in tetangga:
                agenda.append([xk, agenda_arc[0]])
    print("Solution:")
    print (solution)

print("City List:")
print(cities)
print("Neighbour List:")
print(neighbours)
print("Domain List:")
print(domains)
arc_consistency()
print("Finished Agenda List:")
print(agenda)
input("Enter To EXIT")