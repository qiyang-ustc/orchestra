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
# Verification Level Tracking
# =============================================================================

VERIFICATION_LEVELS = {
    "L0": "draft",
    "L1": "cross-checked",
    "L2": "tested",
    "L3": "adversarial",
    "L4": "proven",
}


class VerificationTracker:
    """Track verification levels across test runs."""

    def __init__(self):
        self.results: Dict[str, Dict[str, Any]] = {}

    def record(
        self,
        target: str,
        level: str,
        challenger: str,
        passed: bool,
        details: Optional[Dict] = None,
    ) -> None:
        """Record a verification result."""
        if target not in self.results:
            self.results[target] = {"history": []}

        self.results[target]["history"].append({
            "level": level,
            "challenger": challenger,
            "passed": passed,
            "details": details or {},
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        })

        if passed:
            self.results[target]["current_level"] = level

    def get_level(self, target: str) -> str:
        """Get current verification level for a target."""
        return self.results.get(target, {}).get("current_level", "L0")

    def export(self, path: Path) -> None:
        """Export results to YAML."""
        import yaml
        with open(path, "w") as f:
            yaml.dump(self.results, f, default_flow_style=False)


@pytest.fixture(scope="session")
def verification_tracker() -> VerificationTracker:
    """Session-wide verification tracker."""
    return VerificationTracker()


# =============================================================================
# Adversarial Testing Support
# =============================================================================

class AdversarialAttacker:
    """Generate adversarial inputs to break equivalence."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)
        self.attempts = 0
        self.failures = 0
        self.near_misses = 0

    def random_tensor(
        self,
        shape: tuple,
        dtype: torch.dtype = torch.complex128,
        strategy: str = "normal",
    ) -> torch.Tensor:
        """Generate adversarial tensor input."""
        self.attempts += 1

        if strategy == "normal":
            data = self.rng.standard_normal(shape) + 1j * self.rng.standard_normal(shape)
        elif strategy == "boundary":
            # Values near machine epsilon, large values, zeros
            choices = [1e-15, 1e15, 0.0, 1.0, -1.0]
            data = self.rng.choice(choices, size=shape)
            data = data + 1j * self.rng.choice(choices, size=shape)
        elif strategy == "sparse":
            data = np.zeros(shape, dtype=np.complex128)
            nnz = max(1, int(np.prod(shape) * 0.1))
            indices = self.rng.choice(np.prod(shape), size=nnz, replace=False)
            np.put(data, indices, self.rng.standard_normal(nnz))
        elif strategy == "ill_conditioned":
            # For matrices: create nearly singular
            if len(shape) == 2 and shape[0] == shape[1]:
                n = shape[0]
                u = self.rng.standard_normal((n, n))
                s = np.logspace(-15, 0, n)  # condition number ~ 1e15
                data = u @ np.diag(s) @ u.T
            else:
                data = self.rng.standard_normal(shape)
        else:
            data = self.rng.standard_normal(shape)

        return torch.from_numpy(np.asarray(data, dtype=np.complex128))

    def record_failure(self, details: str) -> None:
        """Record a failed attack (equivalence broken)."""
        self.failures += 1

    def record_near_miss(self, details: str) -> None:
        """Record near-miss (passed but close to tolerance)."""
        self.near_misses += 1

    def report(self) -> Dict[str, Any]:
        """Generate adversarial testing report."""
        return {
            "total_attempts": self.attempts,
            "failures": self.failures,
            "near_misses": self.near_misses,
            "success_rate": (self.attempts - self.failures) / max(1, self.attempts),
            "conclusion": "PASS" if self.failures == 0 else "FAIL",
        }


@pytest.fixture
def adversarial_attacker() -> AdversarialAttacker:
    """Adversarial input generator."""
    return AdversarialAttacker()


# =============================================================================
# Pytest Configuration
# =============================================================================

def pytest_configure(config):
    # Basic markers
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "equivalence: marks equivalence tests")
    config.addinivalue_line("markers", "source_required: requires source runtime")

    # Verification level markers
    config.addinivalue_line(
        "markers",
        "orchestra(level, source, challenger=None): verification level metadata"
    )
    config.addinivalue_line(
        "markers",
        "adversarial(attacker, attempts, failures): adversarial test metadata"
    )

    # Triangular confrontation markers
    config.addinivalue_line("markers", "doc_source: tests doc-source consistency")
    config.addinivalue_line("markers", "doc_target: tests doc-target consistency")
    config.addinivalue_line("markers", "source_target: tests source-target equivalence (oracle)")


def pytest_collection_modifyitems(config, items):
    if not torch.cuda.is_available():
        skip_gpu = pytest.mark.skip(reason="CUDA not available")
        for item in items:
            if "gpu" in item.keywords:
                item.add_marker(skip_gpu)
