function checkOnly(checkbox) {
    var checkboxes = document.getElementsByClassName("form-check-input");
    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = false;
    }
    checkbox.checked = true;
  }

