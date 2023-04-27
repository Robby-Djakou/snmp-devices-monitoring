function Controller() {
    self = this;


    function getData() {

        /*Get Element from DOM*/
        var ipaddress = document.getElementById("ipaddress").value;
        var username = document.getElementById("username").value;
        var securitylevel = document.getElementById("securitylevel").value;
        var authenticationprotocol = document.getElementById("authenticationprotocol").value;
        var passphrase = document.getElementById("passphrase").value;
        var privacyprotocol = document.getElementById("privacyprotocol").value;
        var privacykeys = document.getElementById("privacykeys").value;
        var arr = ["add", ipaddress, username, securitylevel, authenticationprotocol, passphrase, privacyprotocol, privacykeys];
        ValidateIPaddress(ipaddress);
        var connection = new WebSocket("ws://localhost:8765/");

        connection.onopen = function() {
            console.log("Connected")
            if (ipaddress == "" || username == "" || passphrase == "") {
                alert("some fields (ipaddress, username, passphrase) are empty. Please fill it !");
            } else {
                btnText.innerHTML = "Submited!";
                btn.classList.add("active");
                connection.send(arr);
            }
        }

        connection.onerror = function() {
            alert("Please start Python File: backend.py");
        }

        connection.onclose = function() {
            console.log("Close")
        }

    }

    function DeleteData() {
        var ipaddress = document.getElementById("ipaddress").value;
        arr = ["delete", ipaddress];
        ValidateIPaddress(ipaddress);
        var connection = new WebSocket("ws://localhost:8765/");
        connection.onopen = function() {
            console.log("Connected")
            if (ipaddress == "") {
                alert("ipaddress is empty. Please fill it !");
            } else {
                btnText.innerHTML = "Submited!";
                btn1.classList.add("active");
                connection.send(arr);
            }
        }

        connection.onerror = function() {
            alert("Please start Python File: backend.py");
        }
    }

    this.onLoaded = function() {
        //window.document.getElementById("#btn").addEventListener("click", getData, false);
        const btn = document.querySelector("#btn");
        const btn1 = document.querySelector("#btn1");
        const btnText = document.querySelector("#btnText");

        if (btn != null) {
            btn.onclick = () => {
                getData();
            };
        }

        if (btn1 != null) {
            btn1.onclick = () => {
                DeleteData();
            };
        }


    };

    function ValidateIPaddress(inputText) {
        var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        if (inputText.match(ipformat)) {
            return true;
        } else {
            alert("You have entered an invalid IP address!");
            return false;
        }
    }
}