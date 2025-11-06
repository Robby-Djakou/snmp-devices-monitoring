from abc import ABC, abstractmethod


class Shell(ABC):
    """
    Abstract Base Class defining an interface for running system commands.
    """

    @abstractmethod
    def run_command(self, command: str, timeout: int = 60) -> tuple[str, str, int]:
        """
        Abstract method to execute a system command

        Args:
            command: A string representing the command and its arguments.
            timeout: Maximum time in seconds to wait for the command to complete.

        Returns:
            'stdout', 'stderr' and 'returncode'.
        """
        pass
