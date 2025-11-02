import sys
import textwrap
import toml
from command_runner import CommandRunner
from dataclasses import dataclass
from pathlib import Path
from lib.systemctl import Systemctl


def eprint(*args, **kwargs):
    """
    Prints the given arguments to the standard error stream (stderr).
    """
    print(*args, file=sys.stderr, **kwargs)


@dataclass
class Telegraf:
    ip_address: str
    """IP address to add new SNMP device or remove existing one."""
    username: str
    """Username for SNMP authentication."""
    security_level: str
    """Security level for SNMP (e.g., authPriv, authNoPriv, noAuthNoPriv)."""
    authentication_protocol: str
    """Authentication protocol for SNMP (e.g., MD5, SHA)."""
    passphrase: str
    """Passphrase for SNMP authentication."""
    privacy_protocol: str
    """Privacy protocol for SNMP (e.g., DES, AES)."""
    privacy_keys: str
    """Privacy keys for SNMP."""

    @classmethod
    def add_snmp_device_conf(cls, telegraf_conf_path: str | Path | None = None):
        """Add a new SNMP device configuration to the Telegraf configuration file."""

        if telegraf_conf_path is None:
            telegraf_conf_path = Path("/etc/telegraf/telegraf.conf")

        if isinstance(telegraf_conf_path, str):
            telegraf_conf_path = Path(telegraf_conf_path)

        telegraf_conf = textwrap.dedent(
            f"""
            [[inputs.snmp]]
            agents = ["udp://{cls.ip_address}:161"]
            timeout = "5s"
            sec_name = "{cls.username}"
            auth_protocol = "{cls.authentication_protocol}"
            auth_password = "{cls.passphrase}"
            sec_level = "{cls.security_level}"
            priv_protocol = "{cls.privacy_protocol}"
            priv_password = "{cls.privacy_keys}"
            community = "public"
            name = "snmp"
            version = 3
            [[inputs.ping]]
            urls = ["{cls.ip_address}"]
            count = 1
            ping_interval = 1.0
            timeout = 1.0"""
        )
        with open(telegraf_conf_path, "a") as conf_file:
            conf_file.write("\n" + telegraf_conf)

    @classmethod
    def remove_snmp_device_conf(cls, telegraf_conf_path: str | Path | None = None):
        """Remove a SNMP device configuration from the Telegraf configuration file."""

        if telegraf_conf_path is None:
            telegraf_conf_path = Path("/etc/telegraf/telegraf.conf")

        if isinstance(telegraf_conf_path, str):
            telegraf_conf_path = Path(telegraf_conf_path)

        parsed_telegraf_with_tolm = toml.load(telegraf_conf_path)
        parsed_telegraf_with_tolm["inputs"]["snmp"] = [
            dev
            for dev in parsed_telegraf_with_tolm["inputs"]["snmp"]
            if f"udp://{cls.ip_address}:161" not in dev.get("agents", [])
        ]
        toml.dump(parsed_telegraf_with_tolm, telegraf_conf_path.open("w"))

    @staticmethod
    def create_new_snmp_conf_header(telegraf_conf_path: str | Path | None = None):
        """Create a new Telegraf SNMP configuration file header."""

        if telegraf_conf_path is None:
            telegraf_conf_path = Path("/etc/telegraf/telegraf.conf")
            # remove existing file
            if telegraf_conf_path.exists():
                telegraf_conf_path.unlink()

        if isinstance(telegraf_conf_path, str):
            telegraf_conf_path = Path(telegraf_conf_path)

        telegraf_conf = textwrap.dedent(
            f"""
            # Telegraf Configuration
            # Configuration for telegraf agent
            [agent]
            ## Default data collection interval for all inputs
            interval = "10s"
            ## Rounds collection interval to 'interval'
            ## ie, if interval="10s" then always collect on :00, :10, :20, etc.
            round_interval = true

            ## Telegraf will send metrics to outputs in batches of at most
            ## metric_batch_size metrics.
            ## This controls the size of writes that Telegraf sends to output plugins.
            metric_batch_size = 1000

            ## Maximum number of unwritten metrics per output.  Increasing this value
            ## allows for longer periods of output downtime without dropping metrics at the
            ## cost of higher maximum memory usage.
            metric_buffer_limit = 10000

            ## Collection jitter is used to jitter the collection by a random amount.
            ## Each plugin will sleep for a random time within jitter before collecting.
            ## This can be used to avoid many plugins querying things like sysfs at the
            ## same time, which can have a measurable effect on the system.
            collection_jitter = "0s"

            ## Collection offset is used to shift the collection by the given amount.
            ## This can be be used to avoid many plugins querying constraint devices
            ## at the same time by manually scheduling them in time.
            # collection_offset = "0s"

            ## Default flushing interval for all outputs. Maximum flush_interval will be
            ## flush_interval + flush_jitter
            flush_interval = "10s"
            ## Jitter the flush interval by a random amount. This is primarily to avoid
            ## large write spikes for users running a large number of telegraf instances.
            ## ie, a jitter of 5s and interval 10s means flushes will happen every 10-15s
            flush_jitter = "0s"

            ## Collected metrics are rounded to the precision specified. Precision is
            ## specified as an interval with an integer + unit (e.g. 0s, 10ms, 2us, 4s).
            ## Valid time units are "ns", "us" (or "µs"), "ms", "s".
            ##
            ## By default or when set to "0s", precision will be set to the same
            ## timestamp order as the collection interval, with the maximum being 1s:
            ##   ie, when interval = "10s", precision will be "1s"
            ##       when interval = "250ms", precision will be "1ms"
            ##
            ## Precision will NOT be used for service inputs. It is up to each individual
            ## service input to set the timestamp at the appropriate precision.
            precision = "0s"

            ## Override default hostname, if empty use os.Hostname()
            hostname = ""

            omit_hostname = false

            # Configuration for sending metrics to InfluxDB
            [[outputs.influxdb]]
            urls = ["http://127.0.0.1:8086"]
            database = "telegraf"

            ## HTTP Basic Auth
            username = "telegraf"
            password = "telegraf"

            # SNMP Input Plugin Configurations
            [[inputs.snmp.field]]
                name = "uptime"
                oid = ".1.3.6.1.2.1.1.3.0"
            [[inputs.snmp.field]]
                name = "gebaeude"
                oid = ".1.3.6.1.2.1.1.5.0"
            [[inputs.snmp.table]]
            name = "DATA"
            inherit_tags = [ "source" ]
            [[inputs.snmp.table.field]]
                name = "ifName"
                oid = ".1.3.6.1.2.1.31.1.1.1.1"
                is_tag = true
            [[inputs.snmp.table.field]]
                name = "ifHCInOctets"
                oid = ".1.3.6.1.2.1.31.1.1.1.6"
            [[inputs.snmp.table.field]]
                name = "ifHCOutOctets"
                oid = ".1.3.6.1.2.1.31.1.1.1.10"
            [[inputs.snmp.table.field]]
                name = "ifInDiscards"
                oid = ".1.3.6.1.2.1.2.2.1.13"
            [[inputs.snmp.table.field]]
                name = "ifOutDiscards"
                oid = ".1.3.6.1.2.1.2.2.1.19"
            [[inputs.snmp.table.field]]
                name = "ifInErrors"
                oid = ".1.3.6.1.2.1.2.2.1.14"
            [[inputs.snmp.table.field]]
                name = "ifOutErrors"
                oid = ".1.3.6.1.2.1.2.2.1.20"
            [[inputs.snmp.table.field]]
                name = "ifInUnknownProtos"
                oid = ".1.3.6.1.2.1.2.2.1.15"
            [[inputs.snmp.table.field]]
                name = "ifAlias"
                oid = ".1.3.6.1.2.1.31.1.1.1.18"
                is_tag = true
            [[inputs.snmp.table.field]]
                name = "ifHighSpeed"
                oid = ".1.3.6.1.2.1.31.1.1.1.15"
            [[inputs.snmp.table.field]]
                name = "ifAdminStatus"
                oid = ".1.3.6.1.2.1.2.2.1.7"
                is_tag = true
            [[inputs.snmp.table.field]]
                name = "ifOperStatus"
                oid = ".1.3.6.1.2.1.2.2.1.8"
            """
        )

        with open(telegraf_conf_path, "w") as conf_file:
            conf_file.write(telegraf_conf)

    def test_telegraf_conf(self, telegraf_conf_path: str | Path) -> bool:
        """Test Telegraf configuration file for correctness."""

        if isinstance(telegraf_conf_path, str):
            telegraf_conf_path = Path(telegraf_conf_path)
        cmd = f"telegraf --config {telegraf_conf_path} --test"
        command_runner = CommandRunner()
        _, err, ret = command_runner.run_command(cmd)
        if ret != 0:
            print(f"Telegraf configuration test failed: {err}")
            return False
        return True

    def run_telegraf_with_custom_conf(self, telegraf_conf_path: str | Path) -> None:
        """Run Telegraf with a custom configuration file."""

        if isinstance(telegraf_conf_path, str):
            telegraf_conf_path = Path(telegraf_conf_path)
        cmd = f"telegraf --config {telegraf_conf_path}"
        command_runner = CommandRunner()
        _, err, ret = command_runner.run_command(cmd)
        if ret != 0:
            print(f"Telegraf command failed: {err}")
            return
        eprint("Telegraf is running with custom configuration.")

    def run_telegraf_with_default_conf(self) -> None:
        """Run Telegraf with the default configuration file."""

        cmd = "telegraf"
        command_runner = CommandRunner()
        _, err, ret = command_runner.run_command(cmd)
        if ret != 0:
            print(f"Telegraf command failed: {err}")
            return
        eprint(
            "Telegraf is running with default configuration in /etc/telegraf/telegraf.conf."
        )

    def start_telegraf_service(self) -> None:
        """Start the Telegraf service using systemctl."""

        systemctl = Systemctl()
        _, err, ret = systemctl.start_unit("telegraf.service")
        if ret != 0:
            print(f"Failed to start Telegraf service: {err}")
            return
        eprint("Telegraf service started successfully.")

    def stop_telegraf_service(self) -> None:
        """Stop the Telegraf service using systemctl."""

        systemctl = Systemctl()
        _, err, ret = systemctl.stop_unit("telegraf.service")
        if ret != 0:
            print(f"Failed to stop Telegraf service: {err}")
            return
        eprint("Telegraf service stopped successfully.")

    def restart_telegraf_service(self) -> None:
        """Restart the Telegraf service using systemctl."""

        systemctl = Systemctl()
        _, err, ret = systemctl.restart_unit("telegraf.service")
        if ret != 0:
            print(f"Failed to restart Telegraf service: {err}")
            return
        eprint("Telegraf service restarted successfully.")

    def is_telegraf_service_active(self) -> bool:
        """Check if the Telegraf service is active using systemctl."""

        systemctl = Systemctl()
        return systemctl.is_unit_active("telegraf.service")
