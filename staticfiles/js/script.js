function validateForm() {
  var valid = document.forms["recipeForm"]["id_url"].value;
  if (valid == "+") {
    alert("Please enter a valid website!");
    return false;
  }
}