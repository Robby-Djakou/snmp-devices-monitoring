from pathlib import Path
from flask import Flask, jsonify, render_template, request
from lib.database import Database
from lib.telegraf import Telegraf
from lib.validate_ipaddress import ValidateIPAddress
import pdb

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).parent.resolve()
TELEGRAF_CONF_PATH = PROJECT_ROOT / ".telegraf_conf"
TELEGRAF_CONF_FILE = TELEGRAF_CONF_PATH / "telegraf_with_snmp.conf"
DB_PATH = PROJECT_ROOT / ".database"
DB_FILE = DB_PATH / "snmp_devices.db"


@app.route("/api/remove_dev", methods=["POST"])
def api_remove_dev():
    """Remove SNMP device via API"""

    # Implementation for removing SNMP device via API
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400
    ipaddress = data.get("ipaddress")
    if not ipaddress:
        return jsonify({"message": "IP address is required"}), 400
    if not ValidateIPAddress.is_valid_ip(ipaddress):
        return jsonify({"message": "Invalid IP address"}), 400

    DB_PATH.mkdir(parents=True, exist_ok=True)
    TELEGRAF_CONF_PATH.mkdir(parents=True, exist_ok=True)

    # Remove device from database
    Database.remove_snmp_device_from_db(db_file=DB_FILE, ip_address=str(ipaddress))
    # Fetch all devices and update telegraf configuration
    devices: dict = Database.fetch_all_devices(db_file=DB_FILE)

    telegraf = Telegraf(devices=devices)
    Telegraf.create_new_snmp_conf_header(TELEGRAF_CONF_FILE)
    telegraf.add_snmp_device_conf(TELEGRAF_CONF_FILE)
    # Test the telegraf configuration
    if not Telegraf.test_telegraf_conf(TELEGRAF_CONF_FILE):
        return {"message": "Telegraf configuration test failed"}, 500
    # Run telegraf with the new configuration
    Telegraf.run_telegraf_with_custom_conf(TELEGRAF_CONF_FILE)
    return (
        jsonify(
            {"message": f"Device with ip address '{ipaddress}' removed successfully"}
        ),
        200,
    )


@app.route("/api/add_dev", methods=["POST"])
def api_add_dev():
    """Add SNMP device via API"""

    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400
    ipaddress = data.get("ipaddress")
    username = data.get("username")
    securitylevel = data.get("securitylevel")
    authenticationprotocol = data.get("authenticationprotocol")
    passphrase = data.get("passphrase")
    privacyprotocol = data.get("privacyprotocol")
    privacykeys = data.get("privacykeys")

    if not ipaddress or not username or not passphrase or not privacykeys:
        return jsonify({"message": "All fields are required"}), 400

    if not ValidateIPAddress.is_valid_ip(ipaddress):
        return jsonify({"message": "Invalid IP address"}), 400

    DB_PATH.mkdir(parents=True, exist_ok=True)
    TELEGRAF_CONF_PATH.mkdir(parents=True, exist_ok=True)

    # Create Database instance and use standard path of snmp_devices.db (in PROJECT_ROOT/.database/)
    database = Database(
        ip_address=str(ipaddress),
        username=str(username),
        security_level=str(securitylevel),
        authentication_protocol=str(authenticationprotocol),
        passphrase=str(passphrase),
        privacy_protocol=str(privacyprotocol),
        privacy_keys=str(privacykeys),
    )
    # Create the database and add the device
    database.create_snmp_database()
    database.add_snmp_device_to_db()
    # Fetch all devices and update telegraf configuration
    devices: dict = Database.fetch_all_devices(db_file=DB_FILE)
    telegraf = Telegraf(devices=devices)
    Telegraf.create_new_snmp_conf_header(TELEGRAF_CONF_FILE)
    telegraf.add_snmp_device_conf(TELEGRAF_CONF_FILE)
    # Test the telegraf configuration
    if not Telegraf.test_telegraf_conf(TELEGRAF_CONF_FILE):
        return {"message": "Telegraf configuration test failed"}, 500
    # Run telegraf with the new configuration
    Telegraf.run_telegraf_with_custom_conf(TELEGRAF_CONF_FILE)
    return (
        jsonify(
            {"message": f"Device with ip address '{ipaddress}' added successfully"}
        ),
        200,
    )


@app.route("/remove_dev")
def remove_dev():
    return render_template("./pages/remove_snmp_device.html")


@app.route("/add_dev")
def add_dev():
    return render_template("./pages/add_snmp_device.html")


@app.route("/")
def home():
    return render_template("./index.html")


if __name__ == "__main__":
    app.run(debug=True)
