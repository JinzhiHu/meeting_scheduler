# Meeting Scheduler

This project translates the provided dictionary of meetings into a Min-cost Network Flow problem.

We utilize the Minimum-cost Network Flow (MCNF) problem formulation to solve the meeting scheduling optimization.

## Methodology
- **Optimization Algorithm**: We apply the Bus Problem methodology to solve the MCNF problem and minimize the negative cost (or the maximum positive value of the attended meetings).
- **Data Preparation**: We convert the dictionary of meetings into a network graph suitable for the problem. Two detailed .csv files will be generated. One of them contains detials about the Arcs, the other contians information about the Vertices.
 **Fields in the dictionary network are not consistent with data outputted in the csv files** (the consistency issue will be fixed in the future.)
- **Output**: After optimization, the list of meetings to be attended will be outputted.

## Reference

Optimization part is provided by [MO-book](https://mobook.github.io/MO-book/notebooks/04/02-mincost-flow.html).
