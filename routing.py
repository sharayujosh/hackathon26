import heapq
from itertools import permutations

import hospital_layout as layout


# --------------------------------------------------
# 1. DIJKSTRA'S SHORTEST PATH ALGORITHM
# --------------------------------------------------

def find_shortest_path(start, destination):

    # Check that both locations exist in the navigation graph
    if start not in layout.NAVIGATION_GRAPH:
        raise ValueError(f"Starting point '{start}' does not exist.")

    if destination not in layout.NAVIGATION_GRAPH:
        raise ValueError(f"Destination '{destination}' does not exist.")

    # Store the shortest known distance to each node
    distances = {
        node: float("inf")
        for node in layout.NAVIGATION_GRAPH
    }

    # Store the previous node in the shortest path
    previous_nodes = {
        node: None
        for node in layout.NAVIGATION_GRAPH
    }

    # Distance from the starting point to itself is zero
    distances[start] = 0

    # Priority queue stores (distance, node)
    priority_queue = [(0, start)]

    # Keep exploring until there are no nodes left
    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        # Ignore outdated entries in the priority queue
        if current_distance > distances[current_node]:
            continue

        # Stop when we reach the destination
        if current_node == destination:
            break

        # Check all neighboring nodes
        for neighbor, distance in layout.NAVIGATION_GRAPH[current_node]:

            # Calculate the distance through the current node
            new_distance = current_distance + distance

            # Update if this route is shorter
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Check whether a route was found
    if distances[destination] == float("inf"):
        raise ValueError(
            f"No route exists from '{start}' to '{destination}'."
        )

    # Reconstruct the shortest path
    path = []
    current_node = destination

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    # Reverse the path to get start -> destination
    path.reverse()

    return path, distances[destination]


# --------------------------------------------------
# 2. MULTI-ITEM ROUTE PLANNER
# --------------------------------------------------

def plan_multi_item_route(required_items):

    # Check that at least one item is required
    if not required_items:
        raise ValueError("No supplies were provided.")

    # Check that every requested storage location exists
    for item in required_items:
        if item not in layout.ACCESS_NODE_IDS:
            raise ValueError(
                f"Storage location '{item}' does not exist."
            )

    # Remove duplicate storage locations while preserving order
    required_items = list(dict.fromkeys(required_items))

    # Starting and ending points
    start = "ENTRY"
    end = "EXIT"

    # Store the best route found so far
    best_distance = float("inf")
    best_order = None
    best_path = None

    # Try every possible order of collecting the supplies
    for order in permutations(required_items):

        current_location = start
        total_distance = 0
        complete_path = [start]

        # Visit each required storage location
        for storage_id in order:

            # Get the navigation node for this storage location
            destination = layout.ACCESS_NODE_IDS[storage_id]

            # Find the shortest path to that location
            path, distance = find_shortest_path(
                current_location,
                destination
            )

            # Add the distance
            total_distance += distance

            # Add the path without repeating its starting node
            complete_path.extend(path[1:])

            # Update current location
            current_location = destination

        # Finally, travel to the EXIT
        path, distance = find_shortest_path(
            current_location,
            end
        )

        total_distance += distance
        complete_path.extend(path[1:])

        # Save this route if it is the shortest one so far
        if total_distance < best_distance:

            best_distance = total_distance
            best_order = list(order)
            best_path = complete_path

    return best_order, best_path, best_distance