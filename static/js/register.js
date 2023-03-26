

var form = document.getElementById("myForm");

form.addEventListener("submit", function(event) {
    if (!password.value.matches(rePassword.value)) {
        event.preventDefault();
        alert("The passwords do not match. Please try again.");
    }
});
