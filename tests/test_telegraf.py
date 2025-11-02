import pytest
from pathlib import Path
from lib.database import Database
from lib.telegraf import Telegraf, eprint


TEST_DIR = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def remove_created_telegraf_conf():
    """Fixture to remove created telegraf_conf_example.conf after tests."""

    eprint("No setup needed before tests.")
    yield
    eprint("Removing created telegraf_conf_example.conf...")
    telegraf_conf_path = TEST_DIR / "data" / "telegraf_conf_example.conf"
    if telegraf_conf_path.exists():
        telegraf_conf_path.unlink()


class TestTelegraf:
    """Tests for the Telegraf class."""

    def test_create_new_snmp_conf_header(self):
        """Test creating a new telegraf_conf_example.conf with SNMP header."""

        telegraf_conf_file = TEST_DIR / "data" / "telegraf_conf_example.conf"

        Telegraf.create_new_snmp_conf_header(telegraf_conf_file)
        assert telegraf_conf_file.exists()
        content = telegraf_conf_file.read_text()
        assert "[[outputs.influxdb]]" in content
        assert 'urls = ["http://127.0.0.1:8086"]' in content
        assert 'database = "telegraf"' in content
        assert "[[inputs.snmp.table.field]]" in content
        assert 'name = "ifAlias"' in content
        assert 'oid = ".1.3.6.1.2.1.31.1.1.1.18"' in content
        assert "is_tag = true" in content

    def test_add_snmp_device_to_telegraf_conf(self):
        """Test adding an SNMP device configuration to telegraf_conf_example.conf."""

        telegraf_conf_file = TEST_DIR / "data" / "telegraf_conf_example.conf"
        database_path = TEST_DIR / "data"
        database = Database(
            db_path=database_path,
            ip_address="192.168.1.1",
            username="testuser",
            security_level="authPriv",
            authentication_protocol="MD5",
            passphrase="authpass",
            privacy_protocol="DES",
            privacy_keys="privpass",
        )

        database.create_snmp_database()
        db_file = database_path / "snmp_devices.db"
        assert db_file.exists()
        database.add_snmp_device_to_db()
        devices: dict = Database.fetch_all_devices(db_file=db_file)
        telegraf = Telegraf(devices=devices)
        Telegraf.create_new_snmp_conf_header(telegraf_conf_file)
        assert telegraf_conf_file.exists()
        telegraf.add_snmp_device_conf(telegraf_conf_file)
        content = telegraf_conf_file.read_text()
        assert "[[inputs.snmp]]" in content
        assert 'agents = ["udp://192.168.1.1:161"]' in content
        assert 'sec_name = "testuser"' in content
        assert 'sec_level = "authPriv"' in content
        assert 'auth_protocol = "MD5"' in content
        assert 'auth_password = "authpass"' in content
        assert 'priv_protocol = "DES"' in content
        assert 'priv_password = "privpass"' in content
        assert "[[inputs.ping]]" in content
        assert 'urls = ["192.168.1.1"]' in content
        assert "count = 1" in content
        assert "ping_interval = 1.0" in content
        assert "timeout = 1.0" in content
        db_file.unlink()

    def test_remove_snmp_device_from_telegraf_conf(self):
        """Test removing an SNMP device configuration from telegraf_conf_example.conf."""

        telegraf_conf_file = TEST_DIR / "data" / "telegraf_conf_example.conf"
        snmp_db = TEST_DIR / "data" / "test_snmpdata.db"
        Database.remove_snmp_device_from_db(ip_address="192.168.1.2", db_file=snmp_db)
        devices = Database.fetch_all_devices(db_file=snmp_db)
        telegraf = Telegraf(devices=devices)
        Telegraf.create_new_snmp_conf_header(telegraf_conf_file)
        telegraf.add_snmp_device_conf(telegraf_conf_file)
        assert telegraf_conf_file.exists()
        content = telegraf_conf_file.read_text()
        assert 'agents = ["udp://192.168.1.2:161"]' not in content
        assert 'urls = ["192.168.1.2"]' not in content
        assert 'sec_name = "testuser2"' not in content
        assert 'auth_password = "authpass2"' not in content
        assert 'priv_password = "privpass2"' not in content
        assert 'agents = ["udp://192.168.1.1:161"]' in content
        assert 'urls = ["192.168.1.1"]' in content
        assert 'sec_name = "testuser"' in content
        assert 'auth_password = "authpass"' in content
        assert 'priv_password = "privpass"' in content
