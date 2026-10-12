

import folium

# Approximate village-center coordinates
VILLAGE_COORDS = {
    "gorinta": (17.11126, 82.16693),
    "pullimeru": (17.12669, 82.15932),
    "divili": (17.14439, 82.16255),
    "virava": (17.13536, 82.18612),
    "mallam": (17.11030, 82.18546),
}
locations=[
    "gorinta",
    "pullimeru",
    "divili",
    "virava",
    "mallam"
]
roads=[
    ("gorinta","pullimeru",4),
    ("pullimeru","divili",2),
    ("divili","virava",3),
    ("virava","mallam",2.5),
    ("mallam","gorinta",3),
    ("pullimeru","virava",2)
]
RATE_PER_KM = 10

edges = []

for start, end, distance in roads:
    cost = distance * RATE_PER_KM
    edges.append((cost, start, end))

edges.sort()
parent = {location: location for location in locations}

def find(location):
    if parent[location] != location:
        parent[location] = find(parent[location])
    return parent[location]

mst = []
total_cost = 0

for cost, start, end in edges:
    root1 = find(start)
    root2 = find(end)

    if root1 != root2:
        parent[root1] = root2
        mst.append((start, end, cost))
        total_cost += cost

    if len(mst) == len(locations) - 1:
        break


def draw_map(locations, roads, mst):
    center = [17.13, 82.17]

    road_map = folium.Map(
        location=center,
        zoom_start=13,
        tiles="CartoDB positron"
    )

    # Add village markers
    for name in locations:
        folium.Marker(
            location=VILLAGE_COORDS[name.lower()],
            popup=name.title(),
            tooltip=name.title()
        ).add_to(road_map)

    # Draw candidate roads in grey
    for start, end, distance in roads:
        folium.PolyLine(
            locations=[
                VILLAGE_COORDS[start.lower()],
                VILLAGE_COORDS[end.lower()]
            ],
            color="gray",
            weight=2,
            tooltip=f"Candidate: {start} - {end}"
        ).add_to(road_map)

    # Draw selected MST roads in blue
    total_cost = 0

    for start, end, cost in mst:
        folium.PolyLine(
            locations=[
                VILLAGE_COORDS[start.lower()],
                VILLAGE_COORDS[end.lower()]
            ],
            color="blue",
            weight=5,
            tooltip=f"Selected: {start} - {end}: ₹{cost} lakh"
        ).add_to(road_map)

        total_cost += cost

    # Display the total cost
    folium.Marker(
        location=center,
        tooltip="Minimum Spanning Tree",
        popup=(
            f"Selected roads: {len(mst)}<br>"
            f"Total estimated cost: ₹{total_cost} lakh"
        ),
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(road_map)

    road_map.save("road_network_map.html")
    print("Map created: road_network_map.html")
    print(f"Selected roads: {len(mst)}")
    print(f"Total estimated cost: ₹{total_cost} lakh")
from map_view import draw_map

draw_map(locations, roads, mst)