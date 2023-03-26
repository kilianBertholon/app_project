// Récupérer la div pour la nouvelle table
var nouvelleTableDiv = document.getElementById("nouvelle-table");

// Ajouter un écouteur d'événement sur le formulaire pour intercepter sa soumission
var form = document.querySelector("form");
form.addEventListener("submit", function(event) {
  // Empêcher le formulaire de se soumettre normalement
  event.preventDefault();

  // Récupérer les données du formulaire
  var prenom = document.getElementById("prenom").value;
  var nom = document.getElementById("nom").value;
  var distance = document.getElementById("distance").value;

  // Créer une requête AJAX pour envoyer les données du formulaire au script Python
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "pente.py");
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onload = function() {
    // Récupérer les résultats de la requête AJAX
    var resultat = xhr.responseText;

    // Créer une nouvelle table pour afficher les résultats
    var table = document.createElement("table");
    var tbody = document.createElement("tbody");

    // Ajouter une rangée pour le prénom et le nom
    var row = document.createElement("tr");
    var cell1 = document.createElement("td");
    cell1.appendChild(document.createTextNode("Prénom :"));
    row.appendChild(cell1);
    var cell2 = document.createElement("td");
    cell2.appendChild(document.createTextNode(prenom));
    row.appendChild(cell2);
    tbody.appendChild(row);

    row = document.createElement("tr");
    cell1 = document.createElement("td");
    cell1.appendChild(document.createTextNode("Nom :"));
    row.appendChild(cell1);
    cell2 = document.createElement("td");
    cell2.appendChild(document.createTextNode(nom));
    row.appendChild(cell2);
    tbody.appendChild(row);

    // Ajouter une rangée pour la distance
    row = document.createElement("tr");
    cell1 = document.createElement("td");
    cell1