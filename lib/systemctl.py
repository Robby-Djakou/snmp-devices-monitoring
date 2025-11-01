import sys
from command_runner import CommandRunner


# def eprint(*args, **kwargs):
#     """
#     Prints the given arguments to the standard error stream (stderr).
#     """
#     print(*args, file=sys.stderr, **kwargs)


class Systemctl:

    def __init__(self):
        self.commandrunner = CommandRunner()

    def start_unit(self, unit_name: str):
        """Start unit using systemctl command."""

        cmd = f"systemctl start {unit_name}"
        out, err, ret = self.commandrunner.run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    def stop_unit(self, unit_name: str):
        """Stop unit using systemctl command."""

        cmd = f"systemctl stop {unit_name}"
        out, err, ret = self.commandrunner.run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    def restart_unit(self, unit_name: str):
        """Restart unit using systemctl command."""

        cmd = f"systemctl restart {unit_name}"
        out, err, ret = self.commandrunner.run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    def exist_unit(self, unit_name: str) -> bool:
        """
        Check if an systemctl unit exist
        """

        cmd = "systemctl list-units --all"
        out, err, ret = self.commandrunner.run_command(cmd)

        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        if unit_name in out:
            return True
        return False

    def is_unit_active(self, unit_name: str) -> bool:
        """"""

        raise NotImplementedError()
