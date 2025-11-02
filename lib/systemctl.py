from dataclasses import dataclass
from command_runner import CommandRunner
import sys


@dataclass
class Systemctl:
    """Class to manage systemctl units."""

    @staticmethod
    def start_unit(unit_name: str):
        """Start unit using systemctl command."""

        cmd = f"systemctl start {unit_name}"
        out, err, ret = CommandRunner().run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    @staticmethod
    def stop_unit(unit_name: str):
        """Stop unit using systemctl command."""

        cmd = f"systemctl stop {unit_name}"
        out, err, ret = CommandRunner().run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    @staticmethod
    def restart_unit(unit_name: str):
        """Restart unit using systemctl command."""

        cmd = f"systemctl restart {unit_name}"
        out, err, ret = CommandRunner().run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out, err, ret

    @staticmethod
    def exist_unit(unit_name: str) -> bool:
        """Check if an systemctl unit exists"""

        cmd = "systemctl list-units --all"
        out, err, ret = CommandRunner().run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        if unit_name in out:
            return True
        return False

    @staticmethod
    def is_unit_active(unit_name: str) -> bool:
        """Check if an systemctl unit is active"""

        cmd = f"systemctl is-active {unit_name}"
        out, err, ret = CommandRunner().run_command(cmd)
        assert ret == 0 and not err, f"Error occurs: {err} by running: '{cmd}'"
        return out.strip() == "active"
