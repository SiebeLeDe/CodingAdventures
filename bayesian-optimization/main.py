import matplotlib as mpl
import matplotlib.pyplot as plot
import numpy as np
import numpy.typing as npt
from sklearn.gaussian_process import GaussianProcessRegressor
from warnings import catch_warnings, simplefilter

mpl.use("TkAgg")
# mpl.rcParams["figure.dpi"] = 600
# mpl.rcParams["figure.figsize"] = (8, 6)
mpl.rcParams["figure.facecolor"] = "Black"
mpl.rcParams["axes.facecolor"] = "Black"
mpl.rcParams["axes.edgecolor"] = "White"
mpl.rcParams["axes.labelcolor"] = "White"
mpl.rcParams["xtick.color"] = "White"
mpl.rcParams["ytick.color"] = "White"
# mpl.rcParams["lines.linewidth"] = 1.5
# mpl.rcParams["lines.markersize"] = 5
mpl.rcParams["legend.facecolor"] = "Black"
mpl.rcParams["legend.edgecolor"] = "White"
mpl.rcParams["legend.fontsize"] = "Small"
mpl.rcParams["legend.labelcolor"] = "White"
mpl.rcParams["font.family"] = "Arial"


def objective_function(x: npt.NDArray[np.float64], noise_factor: float = 0.9) -> npt.NDArray[np.float64]:
    noise = np.random.normal(loc=0, scale=noise_factor, size=x.shape)
    return (x**2 * np.sin(5 * np.pi * x) ** 6.0) + noise


def plot_objective_function(x: npt.NDArray[np.float64], y: npt.NDArray[np.float64], y_with_noise: npt.NDArray[np.float64]) -> None:
    fig, axs = plot.subplots()
    plot.plot(x, y, label="Objective Function (without noise)", linestyle="solid")
    plot.scatter(x, y_with_noise, label="Objective Function (with noise)", linestyle="dotted", color="orange")
    plot.legend()
    plot.show()
    plot.close()


def surrogate(regressor: GaussianProcessRegressor, X: npt.NDArray[np.float64]) -> tuple[npt.NDArray, npt.NDArray]:
    with catch_warnings():
        simplefilter("ignore")
        return regressor.predict(X, return_std=True)  # type: ignore[datatype]


def plot_surrogate(regressor: GaussianProcessRegressor, X: npt.NDArray[np.float64], y: npt.NDArray[np.float64], y_with_noise: npt.NDArray[np.float64]) -> None:
    y_pred, y_std = surrogate(regressor, X)
    fig, axs = plot.subplots()
    plot.plot(X, y, label="Objective Function", color="Green")
    plot.scatter(X, y_with_noise, label="Objective Function (with noise)", color="orange")
    plot.plot(X, y_pred, label="Surrogate Model", linestyle="dotted", color="cyan")
    plot.fill_between(X.flatten(), (y_pred - 1.96 * y_std).flatten(), (y_pred + 1.96 * y_std).flatten(), color="cyan", alpha=0.2, label="95% Confidence Interval")
    plot.legend()
    plot.show()
    plot.close()


def main():
    # Source: https://machinelearningmastery.com/what-is-bayesian-optimization/
    x = np.arange(0, 1, 0.01, dtype=np.float64)
    y = objective_function(x, noise_factor=0.0)
    y_with_noise = objective_function(x, noise_factor=0.1)

    # plot_objective_function(x, y, y_with_noise)

    # Create a Gaussian Process Regressor
    regressor = GaussianProcessRegressor()
    X = x.reshape(-1, 1)  # Reshape x to be a 2D array for the regressor
    Y = y_with_noise.reshape(-1, 1)  # Reshape y_with_noise to be a 2D array for the regressor
    regressor.fit(X, Y)

    plot_surrogate(regressor, X, y, y_with_noise)


if __name__ == "__main__":
    main()
