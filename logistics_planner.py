import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random
    import math
    import matplotlib.pyplot as plt
    import time

    return math, mo, plt, random, time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📦 Smart Logistics Planner
    **Advanced Algorithms & Programming | Final Mini-Project**

    This tool solves a two-part logistics problem:
    1. **Queue Prioritization:** Using an optimized **Quicksort** algorithm to organize a queue of packages based on their urgency.
    2. **Route Optimization:** Using a **Genetic Algorithm** to solve the Traveling Salesman Problem (TSP), finding the most fuel-efficient route between the highest-priority delivery locations.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. Algorithm Definitions
    First, we define our core algorithms. Notice the optimization in `quicksort_packages`: we use a **middle-element pivot**. This prevents the $O(n^2)$ worst-case time complexity that occurs in standard Quicksort when the input data is already partially sorted.
    """)
    return


@app.cell
def _(random):
    # ==========================================
    # ALGORITHM A: OPTIMIZED QUICKSORT O(n log n)
    # ==========================================
    def quicksort_packages(arr):
        """
        Sorts a list of package dictionaries by their 'priority' integer.
        Lower number = Higher Priority (e.g., 1 is delivered before 3).
        """
        if len(arr) <= 1:
            return arr

        # OPTIMIZATION: Middle pivot avoids O(n^2) on partially sorted daily queues
        pivot_idx = len(arr) // 2
        pivot_val = arr[pivot_idx]["priority"]

        left = []
        middle = []
        right = []

        for p in arr:
            if p["priority"] < pivot_val:
                left.append(p)
            elif p["priority"] == pivot_val:
                middle.append(p)
            else:
                right.append(p)

        return quicksort_packages(left) + middle + quicksort_packages(right)

    # ==========================================
    # ALGORITHM B: GENETIC ALGORITHM (TSP SOLVER)
    # ==========================================
    def calculate_distance(route, dist_matrix):
        """Calculates total distance including departure and return to Warehouse (Node 0)"""
        if not route:
            return 0
        full_path = [0] + route + [0]
        total = 0
        for i in range(len(full_path) - 1):
            total += dist_matrix[full_path[i]][full_path[i+1]]
        return total

    def genetic_algorithm(locations, dist_matrix, generations=50, pop_size=30):
        """
        Evolves a population of routes to find the shortest path.
        """
        if len(locations) <= 1:
            return locations

        # 1. Initialize random population
        population = [random.sample(locations, len(locations))
                      for _ in range(pop_size)]

        for gen in range(generations):
            # 2. Fitness Evaluation (Sort by shortest distance)
            population = sorted(
                population, key=lambda r: calculate_distance(r, dist_matrix))

            # 3. Elitism (Keep the best 20% of routes automatically)
            elite_count = max(2, int(pop_size * 0.2))
            next_gen = population[:elite_count]

            # 4. Mutation / Breeding to fill the rest of the generation
            while len(next_gen) < pop_size:
                # Pick a parent from the better half of the population
                parent = random.choice(population[:int(pop_size * 0.5)])
                child = list(parent)
                # Swap Mutation: swap two locations in the route
                idx1, idx2 = random.sample(range(len(child)), 2)
                child[idx1], child[idx2] = child[idx2], child[idx1]
                next_gen.append(child)

            population = next_gen

        # Return the best route found after all generations
        return population[0]

    return calculate_distance, genetic_algorithm, quicksort_packages


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. City Environment & Delivery Dashboard
    Use the controls below to generate a new day of deliveries and run the simulation. The system will sort the packages and route the driver to the top priority locations.
    """)
    return


@app.cell
def _(mo):
    # Interactive UI Elements
    pkg_count_slider = mo.ui.slider(
        start=20, stop=200, step=10, value=50, label="Total Packages in Queue:")
    route_size_slider = mo.ui.slider(
        start=5, stop=15, step=1, value=8, label="Truck Capacity (Locations per route):")
    gen_data_btn = mo.ui.button(
        label="1. Generate City & Queue", value=0, on_click=lambda v: v + 1)
    run_algo_btn = mo.ui.button(
        label="2. Optimize Routing", value=0, on_click=lambda v: v + 1)

    controls = mo.vstack([
        mo.hstack([pkg_count_slider, route_size_slider]),
        mo.hstack([gen_data_btn, run_algo_btn])
    ])
    return (
        controls,
        gen_data_btn,
        pkg_count_slider,
        route_size_slider,
        run_algo_btn,
    )


@app.cell
def _(gen_data_btn, math, mo, pkg_count_slider, random):
    # Reactive state updates when "Generate" is clicked
    _ = gen_data_btn.value

    TOTAL_NODES = 20

    # Generate City Coordinates (for plotting)
    city_coords = {0: (50, 50)}  # Node 0 is the Warehouse in the center
    for _i in range(1, TOTAL_NODES):
        city_coords[_i] = (random.randint(0, 100), random.randint(0, 100))

    # Generate Distance Matrix (Euclidean distance between all nodes)
    dist_matrix = [[0] * TOTAL_NODES for _ in range(TOTAL_NODES)]
    for _i in range(TOTAL_NODES):
        for _j in range(TOTAL_NODES):
            _x1, _y1 = city_coords[_i]
            _x2, _y2 = city_coords[_j]
            dist_matrix[_i][_j] = math.sqrt((_x2 - _x1)**2 + (_y2 - _y1)**2)

    # Generate random package queue
    raw_packages = []
    for _ in range(pkg_count_slider.value):
        raw_packages.append({
            "id": f"PKG-{random.randint(1000, 9999)}",
            "loc": random.randint(1, TOTAL_NODES - 1),
            "priority": random.randint(1, 5)  # 1 is High, 5 is Low
        })

    mo.md("✅ *City map and package queue generated successfully!*")
    return city_coords, dist_matrix, raw_packages


@app.cell
def _(
    calculate_distance,
    city_coords,
    controls,
    dist_matrix,
    genetic_algorithm,
    mo,
    plt,
    quicksort_packages,
    raw_packages,
    route_size_slider,
    run_algo_btn,
    time,
):
    layout = controls

    if run_algo_btn.value > 0:
        # --- 1. RUN QUICKSORT ---
        t0 = time.time()
        sorted_packages = quicksort_packages(raw_packages)
        sort_time = time.time() - t0

        # --- 2. BATCHING ---
        # Get the unique locations of the highest priority packages to fill the truck
        target_locations = []
        for _pkg in sorted_packages:
            if _pkg["loc"] not in target_locations:
                target_locations.append(_pkg["loc"])
            if len(target_locations) >= route_size_slider.value:
                break

        # --- 3. RUN GENETIC ALGORITHM ---
        t1 = time.time()
        best_route = genetic_algorithm(
            target_locations, dist_matrix, generations=80, pop_size=40)
        route_time = time.time() - t1

        final_distance = calculate_distance(best_route, dist_matrix)
        full_path = [0] + best_route + [0]  # Include warehouse

        # --- 4. VISUALIZATION ---
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot all city nodes (Grey)
        for _idx, (_x, _y) in city_coords.items():
            if _idx == 0:
                ax.plot(_x, _y, marker='s', color='black',
                        markersize=12, label="Warehouse")
            elif _idx in best_route:
                ax.plot(_x, _y, marker='o', color='orange', markersize=10,
                        label="Delivery Drop-off" if _idx == best_route[0] else "")
            else:
                ax.plot(_x, _y, marker='o', color='lightgrey', markersize=6)

            # Add node labels
            ax.text(_x+1, _y+1, str(_idx), fontsize=8)

        # Draw the route path (Blue arrows)
        for _i in range(len(full_path)-1):
            _start_node = full_path[_i]
            _end_node = full_path[_i+1]
            _x1, _y1 = city_coords[_start_node]
            _x2, _y2 = city_coords[_end_node]
            ax.annotate("", xy=(_x2, _y2), xytext=(_x1, _y1),
                        arrowprops=dict(arrowstyle="->", color="blue", lw=1.5, alpha=0.7))

        ax.set_title(
            f"Optimized Delivery Route (Total Distance: {final_distance:.2f} km)")
        ax.grid(True, linestyle="--", alpha=0.4)

        # Build the final output display
        route_str = " ➔ ".join(map(str, full_path))

        results_panel = mo.md(f"""
        ### 📊 Execution Results
        **Phase 1: Prioritization (Quicksort)**
        * Sorted {len(raw_packages)} packages in `{sort_time:.6f} seconds`.
        * Selected Top {len(target_locations)} unique priority locations.

        **Phase 2: Pathfinding (Genetic Algorithm)**
        * Processed {80} generations in `{route_time:.6f} seconds`.
        * **Final Route Sequence:** {route_str}
        * **Total Distance Driven:** {final_distance:.2f} km
        """)

        layout = mo.vstack([
            controls,
            results_panel,
            fig
        ])

    layout
    return


if __name__ == "__main__":
    app.run()
