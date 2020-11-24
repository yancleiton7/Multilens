function show_article(id_pedido){

    var infos = document.getElementById(id_pedido);

    if (infos.style.display === "none") {
        infos.style.display = "block";
      } else {
        infos.style.display = "none";
      }
}

