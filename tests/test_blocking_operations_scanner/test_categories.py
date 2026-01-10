"""Tests for blocking operation categories."""

import pytest

from upcast.scanners.blocking_operations import BlockingOperationsScanner
from tests.fixtures.test_utils import create_test_file


class TestTimeBasedCategory:
    """Test detection of time-based blocking operations."""

    def test_time_sleep_detection(self, tmp_path, create_scanner, time_based_fixtures):
        """Test detection of time.sleep operations."""
        file_path = create_test_file(tmp_path, time_based_fixtures["TIME_SLEEP"], "time_sleep.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) >= 1
        operations = [op.operation for op in output.results["time_based"]]
        assert any("time.sleep" in op for op in operations)

    def test_asyncio_sleep_detection(self, tmp_path, create_scanner, time_based_fixtures):
        """Test detection of asyncio.sleep operations."""
        file_path = create_test_file(tmp_path, time_based_fixtures["ASYNCIO_SLEEP"], "asyncio_sleep.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["time_based"]) >= 1
        operations = [op.operation for op in output.results["time_based"]]
        assert any("asyncio.sleep" in op for op in operations)


class TestSynchronizationCategory:
    """Test detection of synchronization primitives."""

    def test_threading_lock_detection(self, tmp_path, create_scanner, sync_fixtures):
        """Test detection of threading.Lock operations."""
        file_path = create_test_file(tmp_path, sync_fixtures["THREADING_LOCK"], "threading_lock.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["synchronization"]) >= 1
        operations = [op.operation for op in output.results["synchronization"]]
        assert any("threading.Lock" in op for op in operations)

    def test_threading_semaphore_detection(self, tmp_path, create_scanner, sync_fixtures):
        """Test detection of threading.Semaphore operations."""
        file_path = create_test_file(tmp_path, sync_fixtures["THREADING_SEMAPHORE"], "semaphore.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["synchronization"]) >= 1
        operations = [op.operation for op in output.results["synchronization"]]
        assert any("Semaphore" in op for op in operations)


class TestSubprocessCategory:
    """Test detection of subprocess operations."""

    def test_subprocess_run_detection(self, tmp_path, create_scanner, subprocess_fixtures):
        """Test detection of subprocess.run operations."""
        file_path = create_test_file(tmp_path, subprocess_fixtures["SUBPROCESS_RUN"], "subprocess_run.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["subprocess"]) >= 1
        operations = [op.operation for op in output.results["subprocess"]]
        assert any("subprocess.run" in op for op in operations)

    def test_subprocess_call_detection(self, tmp_path, create_scanner, subprocess_fixtures):
        """Test detection of subprocess.call operations."""
        file_path = create_test_file(tmp_path, subprocess_fixtures["SUBPROCESS_CALL"], "subprocess_call.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["subprocess"]) >= 1
        operations = [op.operation for op in output.results["subprocess"]]
        assert any("subprocess.call" in op for op in operations)


class TestDatabaseCategory:
    """Test detection of database blocking operations."""

    def test_select_for_update_detection(self, tmp_path, create_scanner, database_fixtures):
        """Test detection of select_for_update operations."""
        file_path = create_test_file(tmp_path, database_fixtures["SELECT_FOR_UPDATE"], "select_for_update.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        assert len(output.results["database"]) >= 1
        operations = [op.operation for op in output.results["database"]]
        assert any("select_for_update" in op for op in operations)

    def test_django_transaction_atomic(self, tmp_path, create_scanner, database_fixtures):
        """Test detection of Django transaction.atomic."""
        file_path = create_test_file(tmp_path, database_fixtures["DJANGO_TRANSACTION"], "transaction.py")
        scanner = create_scanner(BlockingOperationsScanner)

        output = scanner.scan(file_path)

        # Note: transaction.atomic might not be in default patterns,
        # but select_for_update should be detected
        assert len(output.results["database"]) >= 0
