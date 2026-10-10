# Smart Logistics Planner

**Advanced Algorithms & Programming — Final Mini-Project**
Ahmed AlHennawi · MSc Computer Science, University of the Arts London

A dispatch planner that sorts a package queue by urgency, then evolves a delivery route around that order with a genetic algorithm. Built as an interactive [marimo](https://marimo.io) notebook.

**[Live site](https://git.arts.ac.uk/pages/a-alhennawi0520251/Mini-Final-Project-Enhanced/)** · **[Repository](https://git.arts.ac.uk/a-alhennawi0520251/Mini-Final-Project-Enhanced)**

---

## The problem

A van can leave with the medical box first, or it can leave on the shortest loop. It cannot do both perfectly.

Sort purely by urgency and the driver zig-zags across the city, burning fuel and time to honour an order the customer never sees. Sort purely by geography and the insulin sits in the back until stop eleven.

This planner treats the two as separate stages rather than one impossible score:

1. **Urgency decides who is in today's batch**, and in what tier.
2. **The route optimiser decides how to physically cover that batch.**

Neither stage has to pretend the other doesn't exist.

---

## How a run works

| Stage | What happens |
|-------|--------------|
| **1. Intake** | Packages are generated with `(x, y)` coordinates and a priority flag. Nothing is assumed to be pre-sorted. |
| **2. Sort** | Quicksort orders the queue by urgency using a middle-element pivot. |
| **3. Select** | The top *N* packages are taken, where *N* is the truck capacity set by the slider. |
| **4. Evolve** | A genetic algorithm searches for a short tour through those stops over 80 generations. |
| **5. Dispatch** | The winning permutation is drawn on the city map with its total distance. |

---

## The algorithms

### Quicksort (middle pivot)

Urgency has few distinct values, so the interesting failure case isn't speed on random data — it's what happens when yesterday's list comes back nearly sorted. Choosing the first or last element as the pivot on that input produces maximally unbalanced partitions and quadratic behaviour.

Picking the middle element costs nothing and removes the common case of that failure.

```python
def quicksort(packages):
    if len(packages) <= 1:
        return packages
    pivot = packages[len(packages) // 2]
    left  = [p for p in packages if p.priority <  pivot.priority]
    mid   = [p for p in packages if p.priority == pivot.priority]
    right = [p for p in packages if p.priority >  pivot.priority]
    return quicksort(left) + mid + quicksort(right)
```

Merge sort would guarantee the O(n log n) bound, but it needs O(n) extra space for a queue that is already in memory, and stability isn't required here.

### Genetic algorithm (Travelling Salesman Problem)

Visiting every stop once at minimum total distance is the TSP. Exhaustive search is O(n!) — twelve stops is already 479 million orderings.

So the planner stops asking for the *best* route and asks for a *good* one, quickly:

- **Chromosome** — a permutation of the selected stops.
- **Fitness** — the inverse of total route distance.
- **Selection** — the strongest routes survive into the next generation.
- **Crossover** — surviving routes exchange ordered segments.
- **Mutation** — two stops are occasionally swapped, so the search doesn't settle on the first hill it finds.

> A genetic algorithm will not return the optimal tour, and it won't return the same tour twice. For dispatch planning, a route within a few percent of optimal in under a second beats an exact answer nobody waits for.

---

## Complexity

| Operation | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Quicksort by urgency | Ω(n log n) | Θ(n log n) | O(n²) | O(log n) |
| Route distance evaluation | Ω(n) | Θ(n) | O(n) | O(1) |
| Genetic algorithm (*g* generations, *p* population) | Θ(g · p · n) per run | | | O(p · n) |
| Exact TSP by brute force *(not used)* | Θ(n!) | | | O(n) |

Runtime is bounded by the generation count rather than by the number of stops. That is what makes the planner predictable to run, and also what caps how good its answer can get.

---

## Running it

**Requirements:** Python 3.9 or newer.

```bash
pip install marimo matplotlib
```

Then, from the project folder:

```bash
marimo edit logistics_planner.py
```

The dashboard opens in your browser. To run it read-only, without the editor:

```bash
marimo run logistics_planner.py
```

If `marimo` isn't found after installing, use `python -m marimo edit logistics_planner.py`.

---

## Using the dashboard

1. Set **number of packages** and **truck capacity** with the sliders.
2. Click **Generate City & Queue** — this creates a random city map and a package list with mixed priorities.
3. Click **Optimize Routing** — the queue is sorted, the top-priority packages are selected, and the optimised route is drawn on the map.

Regenerate a few times with the same settings: because the genetic algorithm is stochastic, the same city can produce slightly different routes, which is the point of the exercise.

---

## Files

```
logistics_planner.py                 the marimo notebook — sorting, GA, and UI
index.html                           project landing page
app.html                             exported static build of the notebook
style.css / script.js                styling and interactions for the landing page
Smart_Logistics_Planner_Report_.pdf  main report
```

---

## What it doesn't do yet

- **Distance is Euclidean.** Straight lines between coordinates, not road distance. Real streets, one-way systems and traffic would change the ranking of routes.
- **One vehicle, unlimited capacity beyond the slider.** Splitting a batch across several vans is the vehicle routing problem and needs a different fitness function.
- **No time windows.** A delivery that must land between 09:00 and 11:00 is currently just another priority tier.
- **Fixed generation count.** Stopping at 80 rather than when improvement stalls wastes work on easy batches and cuts hard ones short.

The obvious next step is an adaptive stopping condition — halt when the best distance hasn't improved for *k* generations — followed by real road distances from a routing API.

---

## References

- Cormen, T. H. et al. (2022) *Introduction to Algorithms*, 4th edn. MIT Press. — Quicksort analysis, Ch. 7.
- Applegate, D. L. et al. (2006) *The Traveling Salesman Problem: A Computational Study*. Princeton University Press.
