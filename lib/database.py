from dataclasses import dataclass
from pathlib import Path
from lib.telegraf import eprint
import sqlite3


PROJECT_DIR = Path(__file__).parent.parent.resolve()
DATABASE_DIR = PROJECT_DIR / ".database"


@dataclass
class Database:
    db_path: Path = DATABASE_DIR
    """Path to the database directory."""
    ip_address: str = ""
    """IP address of the SNMP device."""
    username: str = ""
    """Username for SNMP authentication."""
    security_level: str = ""
    """Security level for SNMP."""
    authentication_protocol: str = ""
    """Authentication protocol for SNMP."""
    passphrase: str = ""
    """Passphrase for SNMP authentication."""
    privacy_protocol: str = ""
    """Privacy protocol for SNMP."""
    privacy_keys: str = ""
    """Privacy keys for SNMP."""

    def create_snmp_database(self):
        """Creates a SQLite database and the SNMPINFOS table if they do not exist."""

        if not self.db_path.exists():
            self.db_path.mkdir(parents=True, exist_ok=True)

        db_file = self.db_path / "snmp_devices.db"
        conn = sqlite3.connect(db_file)
        eprint(f"Database '{db_file.name}' has been created.")
        list_of_tables = conn.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name='SNMPINFOS';"""
        ).fetchall()
        if not list_of_tables:
            eprint("Table 'SNMPINFOS' not found! Creating table...")
            sql = """CREATE TABLE SNMPINFOS(
                ip_address TEXT PRIMARY KEY,
                username TEXT,
                security_level TEXT,
                authentication_protocol TEXT,
                passphrase TEXT,
                privacy_protocol TEXT,
                privacy_keys TEXT
            )"""
            conn.execute(sql)
            eprint("Table 'SNMPINFOS' has been created.")
        else:
            eprint("Table 'SNMPINFOS' found!")
        conn.close()

    @staticmethod
    def check_device_exists_in_db(
        ip_address: str, db_file: str | Path | None = None
    ) -> bool:
        """Checks if an SNMP device with the given IP address exists in the SNMPINFOS table."""

        if db_file is None:
            eprint(
                f"Database file path not provided. Use db file {DATABASE_DIR / 'snmp_devices.db'}"
            )
            db_file = DATABASE_DIR / "snmp_devices.db"
        if isinstance(db_file, str):
            db_file = Path(db_file)
        if not db_file.exists():
            eprint(f"Database '{db_file}' does not exist.")
            return False
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM SNMPINFOS WHERE ip_address = ?"
        cursor.execute(sql, (ip_address,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def add_snmp_device_to_db(self):
        """Adds an SNMP device record to the SNMPINFOS table in the database."""

        db_file = self.db_path / "snmp_devices.db"
        if Database.check_device_exists_in_db(self.ip_address, db_file=db_file):
            eprint(f"SNMP device with IP '{self.ip_address}' already exists.")
            return
        if not db_file.exists():
            eprint(f"Database '{db_file}' does not exist.")
            return

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        sql = """INSERT INTO SNMPINFOS(
            ip_address,
            username,
            security_level,
            authentication_protocol,
            passphrase,
            privacy_protocol,
            privacy_keys
        ) VALUES(?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(
            sql,
            (
                self.ip_address,
                self.username,
                self.security_level,
                self.authentication_protocol,
                self.passphrase,
                self.privacy_protocol,
                self.privacy_keys,
            ),
        )
        conn.commit()
        eprint(
            f"SNMP device with IP '{self.ip_address}' has been added to the database."
        )
        conn.close()

    @staticmethod
    def remove_snmp_device_from_db(
        ip_address: str, db_file: str | Path | None = None
    ) -> None:
        """Deletes an SNMP device record from the SNMPINFOS table in the database."""

        if not Database.check_device_exists_in_db(ip_address, db_file=db_file):
            eprint(f"SNMP device with IP '{ip_address}' does not exist.")
            return
        if not db_file.exists():
            eprint(f"Database '{db_file}' does not exist.")
            return
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        sql = "DELETE FROM SNMPINFOS WHERE ip_address = ?"
        cursor.execute(sql, (ip_address,))
        conn.commit()
        eprint(
            f"SNMP device with IP '{ip_address}' has been deleted from the database."
        )
        conn.close()

    @staticmethod
    def fetch_all_devices(db_file: str | Path | None = None) -> dict:
        """Fetches all SNMP device records from the SNMPINFOS table in the database."""

        if isinstance(db_file, str):
            db_file = Path(db_file)

        if db_file is None:
            db_file = DATABASE_DIR / "snmp_devices.db"

        if not db_file.exists():
            eprint(f"Database '{db_file.name}' does not exist.")
            return
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        sql = "SELECT * FROM SNMPINFOS"
        cursor.execute(sql)
        rows = cursor.fetchall()
        devices = {}
        for row in rows:
            devices[row[0]] = {
                "username": row[1],
                "security_level": row[2],
                "authentication_protocol": row[3],
                "passphrase": row[4],
                "privacy_protocol": row[5],
                "privacy_keys": row[6],
            }
        conn.close()
        return devices
