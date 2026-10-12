#road network planner ---version `1`
locations=[
    "divili",
    "virava",
    "mallam",
    "pullimeru",
    "gorinta"
]
#each road is :(start,end,distance in km)
roads=[
    ("gorinta","pullimeru",4),
    ("pullimeru","divili",2),
    ("divili","virava",3),
    ("virava","mallam",2.5),
    ("mallam","gorinta",3),
    ("pullimeru","virava",2)
]
print("locations:",locations)
print("possible roads:")
for start,end,distance in roads:
    print(start,"-",end,":",distance,"km")
#krushkal's minimum spaning tree algorithm
#cost assumtions
RATE_PER_KM = 10
# calculate candidate road cost
edges = []
for start,end,distance in roads:
    cost=distance*RATE_PER_KM
    edges.append((cost,start,end))
print("\nroad cost estimation:")
for cost,start,end in edges:
    print(f"{start}-{end}:RS{cost}lakh")
# sort roads by increasing cost
edges.sort()
#6 initially ,every location in its own groups
parent={
     location:location for location in locations
}
def find(location):
    if parent[location] != location:
        parent[location]=find(parent[location])
    return parent[location]
#7 built the minimum spanning tree 
mst=[]
total_cost=0
for cost,start,end in edges:
    root_start=find(start)
    root_end=find(end)
    # accept only if the roads joins different groups
    if root_start != root_end:
        parent[root_start]=root_end
        mst.append((start,end,cost))
        total_cost += cost
    # a spanning treesn needs v-1 edges8
    if len(mst)== len(locations)-1:
        break
# 8 display results
print("\n-----Road Network Plan------")
print("Assumec rate :RS",RATE_PER_KM,"LAKSH/KM")
if len(mst)==len(locations)-1:
    print("\nSelected Rods:")
    for start,end,cost in mst:
        print(f"{start}-{end}:RS{cost} laksh")
    print("\nTotal Estimated cost:RS ",total_cost,"laksh")
else:
    print('connot Connect all locations')
    print("check available roads")
    
print("Selected Roads:",mst)
print("Total Cost:",total_cost)
