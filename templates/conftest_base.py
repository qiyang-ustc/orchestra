"""
{{PROJECT_NAME}} Test Configuration

Provides fixtures and utilities for proving equivalence between
source and target implementations.

EQUIVALENCE TESTING PHILOSOPHY:
- Every test is a proof, not just a check
- Compare against source ground truth
- Handle numerical edge cases systematically
"""
from __future__ import annotations

import pytest
import numpy as np
import torch
from pathlib import Path
from typing import Dict, Any, Optional

# =============================================================================
# Configuration
# =============================================================================

GROUND_TRUTH_DIR = Path(__file__).parent / "ground_truth"
DEFAULT_RTOL = 1e-10
DEFAULT_ATOL = 1e-12


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def device() -> torch.device:
    """Default device for tests."""
    return torch.device("cpu")


@pytest.fixture(scope="session")
def dtype() -> torch.dtype:
    """Default dtype for tests."""
    return torch.complex128


@pytest.fixture(scope="session")
def ground_truth() -> Dict[str, Dict[str, np.ndarray]]:
    """Load all ground truth data from source language exports."""
    data = {}
    if GROUND_TRUTH_DIR.exists():
        for npz_file in GROUND_TRUTH_DIR.glob("*.npz"):
            module_name = npz_file.stem
            loaded = np.load(npz_file, allow_pickle=True)
            data[module_name] = {key: loaded[key] for key in loaded.files}
    return data


# =============================================================================
# Equivalence Assertions
# =============================================================================

def assert_close(
    actual: torch.Tensor,
    expected: np.ndarray | torch.Tensor,
    rtol: float = DEFAULT_RTOL,
    atol: float = DEFAULT_ATOL,
    msg: str = "",
) -> None:
    """Assert two tensors are numerically close."""
    if isinstance(expected, np.ndarray):
        expected = torch.from_numpy(expected)
    
    actual = actual.detach().cpu()
    expected = expected.detach().cpu()
    
    if not torch.allclose(actual, expected, rtol=rtol, atol=atol):
        diff = torch.abs(actual - expected)
        max_diff = diff.max().item()
        raise AssertionError(
            f"Tensors not close. {msg}\n"
            f"Max diff: {max_diff:.2e}, rtol={rtol}, atol={atol}"
        )


def assert_eigenvector_equivalent(
    v_actual: torch.Tensor,
    v_expected: np.ndarray | torch.Tensor,
    rtol: float = DEFAULT_RTOL,
    atol: float = DEFAULT_ATOL,
) -> None:
    """Assert eigenvectors equivalent up to phase."""
    if isinstance(v_expected, np.ndarray):
        v_expected = torch.from_numpy(v_expected)
    
    v_actual = v_actual.detach().cpu().flatten()
    v_expected = v_expected.detach().cpu().flatten()
    
    # Normalize
    v_actual = v_actual / torch.linalg.norm(v_actual)
    v_expected = v_expected / torch.linalg.norm(v_expected)
    
    # Compare projectors (phase-invariant)
    proj_actual = torch.outer(v_actual, v_actual.conj())
    proj_expected = torch.outer(v_expected, v_expected.conj())
    
    assert_close(proj_actual, proj_expected, rtol=rtol, atol=atol)


def assert_gradient_equivalent(
    grad_pytorch: torch.Tensor,
    grad_source: np.ndarray | torch.Tensor,
    rtol: float = 1e-8,
    atol: float = 1e-10,
    wirtinger: bool = True,
) -> None:
    """
    Assert gradients are equivalent.
    
    Note: PyTorch uses Wirtinger derivatives for complex tensors.
    Set wirtinger=True to account for conjugate relationship.
    """
    if isinstance(grad_source, np.ndarray):
        grad_source = torch.from_numpy(grad_source)
    
    grad_pytorch = grad_pytorch.detach().cpu()
    grad_source = grad_source.detach().cpu()
    
    if wirtinger:
        grad_source = grad_source.conj()
    
    assert_close(grad_pytorch, grad_source, rtol=rtol, atol=atol)


# =============================================================================
# Property Assertions
# =============================================================================

def assert_hermitian(A: torch.Tensor, atol: float = 1e-10) -> None:
    """Assert A = A†"""
    diff = torch.linalg.norm(A - A.mH).item()
    assert diff < atol, f"Not Hermitian: ||A - A†|| = {diff:.2e}"


def assert_unitary(U: torch.Tensor, atol: float = 1e-10) -> None:
    """Assert U†U = I"""
    n = U.shape[0]
    eye = torch.eye(n, dtype=U.dtype, device=U.device)
    diff = torch.linalg.norm(U.mH @ U - eye).item()
    assert diff < atol, f"Not unitary: ||U†U - I|| = {diff:.2e}"


def assert_positive_diagonal(R: torch.Tensor, atol: float = 1e-10) -> None:
    """Assert R has positive real diagonal (for QR with positive convention)."""
    diag = torch.diag(R)
    imag_norm = torch.linalg.norm(diag.imag).item()
    assert imag_norm < atol, f"Diagonal not real: ||Im(diag)|| = {imag_norm:.2e}"
    min_diag = diag.real.min().item()
    assert min_diag > -atol, f"Diagonal not positive: min = {min_diag:.2e}"


# =============================================================================
# Test Data Factories
# =============================================================================

@pytest.fixture
def random_hermitian(device, dtype):
    """Factory for random Hermitian matrices."""
    def _make(n: int, seed: Optional[int] = None) -> torch.Tensor:
        if seed is not None:
            torch.manual_seed(seed)
        A = torch.randn(n, n, dtype=dtype, device=device)
        return (A + A.mH) / 2
    return _make


@pytest.fixture
def random_unitary(device, dtype):
    """Factory for random unitary matrices."""
    def _make(n: int, seed: Optional[int] = None) -> torch.Tensor:
        if seed is not None:
            torch.manual_seed(seed)
        A = torch.randn(n, n, dtype=dtype, device=device)
        Q, _ = torch.linalg.qr(A)
        return Q
    return _make


# =============================================================================
# Pytest Configuration
# =============================================================================

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "equivalence: marks equivalence tests")
    config.addinivalue_line("markers", "source_required: requires source runtime")


def pytest_collection_modifyitems(config, items):
    if not torch.cuda.is_available():
        skip_gpu = pytest.mark.skip(reason="CUDA not available")
        for item in items:
            if "gpu" in item.keywords:
                item.add_marker(skip_gpu)
