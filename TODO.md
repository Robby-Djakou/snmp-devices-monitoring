# 📝 TODO List

### 🚀 Features

- [ ] Display all registred devices from database to the Frontend (impelement API `GET /api/devices` to list devices)
- [ ] Implement user authentication
- [ ] Add ability to **edit existing SNMP devices** (impelement API `PUT /api/update_dev` to update existing device)
- [ ] Add **search and filtering** by IP address or device name
- [ ] Add a **connection test (ping)**
      before adding a device
- [ ] Create a **dark/light mode toggle**
- [ ] ???

### 🐞 Bugs

- [ ] ???

### 💡 Improvements

- [ ] Add confirmation dialog before removing a device
- [ ] Add a log file to the project
- [ ] Update the function `validateIPaddress` from [validateIPaddress](static/js/controller.js) and use `require('net')`
- [ ] Display a **loading spinner** while API requests are in progress
- [ ] Make the interface **responsive** for mobile and tablet
- [ ] Improve **logging system**
- [ ] Handle **SNMP-related exceptions** gracefully with clear messages
- [ ] Add **unit tests** for all API endpoints
- [ ] Update the `POST`method to delete a existing device to `DELETE`
- [ ] ???
