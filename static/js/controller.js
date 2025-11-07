function Controller() {
  const self = this;

  function validateIPaddress(inputText) {
    var ipformat =
      /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if (ipaddress.match(ipformat)) {
      return true;
    }
    return false;
  }

  function validateFormularAddDev(messageBox) {
    /*Get Elements from DOM*/
    var ipaddress = document.getElementById("ipaddress").value;
    var username = document.getElementById("username").value;
    var passphrase = document.getElementById("passphrase").value;
    var privacykeys = document.getElementById("privacykeys").value;

    if (!ipaddress || !username || !passphrase || !privacykeys) {
      messageBox.style.color = "red";
      messageBox.innerText =
        "Some fields (SNMP ip address, SNMP username, Authentication protocol passphrase, and SNMP privacy keys) are empty. Please fill it !";
      messageBox.style.fontSize = "20px";
      return false;
    }
    if (!validateIPaddress(ipaddress)) {
      messageBox.style.color = "red";
      messageBox.innerText = "You have entered an invalid IP address!";
      messageBox.style.fontSize = "20px";
      return false;
    }

    return true;
  }

  function validateFormularRemoveDev(messageBox) {
    var ipaddress = document.getElementById("ipaddress").value;

    if (!ipaddress) {
      messageBox.style.color = "red";
      messageBox.innerText = "The IP address field is empty. Please fill it!";
      messageBox.style.fontSize = "20px";
      return false;
    }
    if (!validateIPaddress(ipaddress)) {
      messageBox.style.color = "red";
      messageBox.innerText = "You have entered an invalid IP address!";
      messageBox.style.fontSize = "20px";
      return false;
    }

    return true;
  }

  this.onLoaded = function () {
    const submitAddBtn = document.querySelector("#submit-add-btn-id");
    const submitRemoveBtn = document.querySelector("#submit-remove-btn-id");
    const submitText = document.querySelector("#submit-text-id");
    const messageBox = document.getElementById("message-id");

    if (submitAddBtn) {
      submitAddBtn.onclick = async () => {
        /*Get all elements from DOM*/
        var ipaddress = document.getElementById("ipaddress").value;
        var username = document.getElementById("username").value;
        var securitylevel = document.getElementById("securitylevel").value;
        var authenticationprotocol = document.getElementById(
          "authenticationprotocol"
        ).value;
        var passphrase = document.getElementById("passphrase").value;
        var privacyprotocol = document.getElementById("privacyprotocol").value;
        var privacykeys = document.getElementById("privacykeys").value;
        if (validateFormularAddDev(messageBox)) {
          const response = await fetch("/api/add_dev", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              ipaddress: ipaddress,
              username: username,
              securitylevel: securitylevel,
              authenticationprotocol: authenticationprotocol,
              passphrase: passphrase,
              privacyprotocol: privacyprotocol,
              privacykeys: privacykeys,
            }),
          });

          if (response.ok) {
            messageBox.style.color = "green";
            messageBox.innerText = (await response.json()).message;
            messageBox.style.fontSize = "20px";
          } else {
            messageBox.style.color = "red";
            messageBox.innerText = (await response.json()).message;
            messageBox.style.fontSize = "20px";
          }
          submitText.innerHTML = "Submited!";
          submitAddBtn.classList.add("active");
          setTimeout(() => {
            submitAddBtn.classList.remove("active");
            submitText.innerHTML = "Submit";
            submitAddBtn.disabled = false;
          }, 5000);
        }
      };
    }

    if (submitRemoveBtn) {
      submitRemoveBtn.onclick = async () => {
        if (validateFormularRemoveDev(messageBox)) {
          var ipaddress = document.getElementById("ipaddress").value;
          submitRemoveBtn.onclick = async () => {
            const response = await fetch("/api/remove_dev", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                ipaddress: ipaddress,
              }),
            });

            if (response.ok) {
              messageBox.style.color = "green";
              messageBox.innerText = (await response.json()).message;
              messageBox.style.fontSize = "20px";
            } else {
              messageBox.style.color = "red";
              messageBox.innerText = (await response.json()).message;
              messageBox.style.fontSize = "20px";
            }
            submitText.innerHTML = "Submited!";
            submitRemoveBtn.classList.add("active");
            setTimeout(() => {
              submitRemoveBtn.classList.remove("active");
              submitText.innerHTML = "Submit";
              submitRemoveBtn.disabled = false;
            }, 5000);
          };
        }
      };
    }
  };
}
