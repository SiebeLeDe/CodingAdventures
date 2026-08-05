from enum import StrEnum
import numpy as np


class StateType(StrEnum):
    PURE = "pure"
    MIXED = "mixed"


def calculate_density_matrix(coefficients: np.ndarray) -> np.ndarray:
    """
    Calculate the density matrix for a given set of coefficients.

    Parameters:
    coefficients (np.ndarray): Coefficients representing the state vector.

    Returns:
    np.ndarray: The density matrix corresponding to the state.
    """
    basis_length = len(coefficients) // 2

    density_matrix = np.zeros((basis_length, basis_length), dtype=complex)
    for a in range(basis_length):
        for a_prime in range(basis_length):
            # Integrate out the b part
            for b in range(basis_length):
                density_matrix[a, a_prime] += coefficients[a * basis_length + b] * np.conj(coefficients[a_prime * basis_length + b])
    return density_matrix


def determine_state_properties(density_matrix: np.ndarray) -> StateType:
    """
    Determine whether the state represented by the density matrix is pure or mixed.

    Parameters:
    density_matrix (np.ndarray): The density matrix to analyze.

    Returns:
    StateType: The type of the state (PURE or MIXED).
    """
    trace_squared = np.trace(density_matrix @ density_matrix)
    if np.isclose(trace_squared, 1.0):
        return StateType.PURE
    else:
        return StateType.MIXED


def main():

    # Mixed state using basis {up, down} for both observers Alice and Bob
    # # |                               uu>, |ud>, |du>, |dd>
    mixed_state_coefficients = np.array([0.0, np.sqrt(0.5), np.sqrt(0.5), 0.0])

    print("Mixed State Coefficients:", mixed_state_coefficients)

    density_matrix = calculate_density_matrix(mixed_state_coefficients)
    print("Density Matrix:")
    print(density_matrix)
    state_type = determine_state_properties(density_matrix)
    print("State Type:", state_type)


if __name__ == "__main__":
    main()
