# Drinker fate analysis

Dash application with modelling the chances of safe-home return of a heavy drinker.

The motion of heaby drinker is modelled as 2D Brownian motion $\mathbf{B}_t$ with drift $\mathbf{v}$, so:

$$
\left(x_t, y_t\right) = \left(\mathbf{B}^{(1)}_t + \mathbf{v}^{(1)}, \mathbf{B}^{(2)}_t + \mathbf{v}^{(2)}\right).
$$

Cars appear at random, according to mixed Poisson process jump times (distriubtion used for modelling is simply uniform distribution). Cars move with constant speed.

---
## Files description
* `analysis.ipynb` contains conclusions from many simulations run for different sets of parameters.
* `app.py` implements Dash application in which user can run the simluations for chosen parameters and check the fate of the drinker with their own eyes thanks to animation.
* `animation.py` contains a function creating Plotly animation.
* `utils.py` contains classes required for perfroming simulations and mixed Poisson generating functions.
* `simulation.py` contains function that returns the trajectories of a drinker and cars for chosen simulation parameters. 
