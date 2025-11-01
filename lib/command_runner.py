import subprocess
from lib.shell import Shell


class CommandRunner(Shell):
    """
    A concrete implementation using the subprocess.run() function.
    """

    def run_command(self, command: str, timeout: int = 60) -> tuple[str, str, int]:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.CalledProcessError as e:
            # Handle non-zero exit codes when check=True
            return e.stdout, e.stderr, e.returncode
        except subprocess.TimeoutExpired as e:
            # Handle commands that take too long
            return e.stdout.decode(), e.stderr.decode(), -1
        except FileNotFoundError as e:
            # Handle cases where the command itself is not found
            return "", f"Command not found: {e}", -2
