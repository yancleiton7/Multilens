function show_article(id){

    var infos = document.getElementById(id);

    if (infos.style.display === "none") {
        infos.style.display = "block";
      } else {
        infos.style.display = "none";
      }
}

