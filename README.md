# SNMP Device Monitoring Dashboard

**SNMP Device Monitoring Dashboard** is a web-based application to manage and monitor SNMP-enabled network devices. It provides an intuitive interface to add/remove devices, validate SNMP credentials, and visualize real-time metrics using Grafana.

---

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)
- [TODO](#TODO)

---

## Features

- Add or remove SNMP devices from the dashboard
- Seamless integration with Grafana for metrics visualization
- User-friendly web interface for network management

---

## Technologies

- Python 3.12
- Flask
- HTML, CSS, JavaScript
- Grafana (for dashboards)
- SNMP Protocol (v2/v3)

---

## Installation

1. Use `Ubuntu >= 20.04`
2. Install [grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)
3. Install [telegraf](https://docs.influxdata.com/telegraf/v1/install/)
4. Install [influxdb](https://docs.influxdata.com/influxdb/v2/install/?t=Linux)
5. Import [snmp_dashboard](grafana/snmp_dashboard.json) file into grafana to load the **snmp dashboard**

6. Clone the repository:

```bash
git clone https://github.com/robbydjakou/snmp-dashboard.git

cd snmp-dashboard

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

python app.py
```

7. Open your browser at http://127.0.0.1:5000

## Usage

Use Add Device or Remove Device buttons to manage SNMP devices.

Validate IP addresses and credentials before submitting.

Monitor device metrics directly in Grafana dashboards.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Author

Robby Courbis Tatchou Djakou — Software Engineer

📧 Email: [robbycourbistatchoudjakou@gmail.com](mailto:robbycourbistatchoudjakou@gmail.com)

🌐 GitHub: [Robby Djakou](https://github.com/Robby-Djakou)

💼 LinkedIn: [Robby Courbis Tatchou Djakou](https://www.linkedin.com/in/robby-courbis-tatchou-djakou-13b404171)

## License

See [MIT License](LICENSE)

## TODO

See [TODO.md](./TODO.md) for planned features and improvements.
