$("document").ready(() => {
  console.log("App started successfully");

  sio = io();

  var retrieve_db_on_document_ready = true;
  if (retrieve_db_on_document_ready) {
    // console.log("Will retrieve db on document ready");
    sio.emit("request_container_db");
  } else console.log("No db retrieval required");

  $("#tabular-view").click(() => {
    console.log("User requested tabular view");
    sio.emit("request_container_db");

    // if the topology view is selected, hide it when tabular view is selected
    if ($("#topology").is(":visible")) {
      $("#topology").hide();
    }

    $("#tabs").toggle();

    //toggle the topology div only if the tabular view is not toggled
    if ($("#tabs").is(":hidden")) {
      $("#topology").hide();
    }
  });

  $("#topology-view").click(() => {
    console.log("User requested topology view");
    sio.emit("request_container_db");

    // if the tabular view is selected, hide it when topology view is selected
    if ($("#tabs").is(":visible")) {
      $("#tabs").hide();
    }

    $("#topology").toggle();

    //toggle the topology div only if the tabular view is not toggled
    if ($("#topology").is(":hidden")) {
      $("#tabs").hide();
    }
  });

  sio.on("receive_container_db", (data) => {
    var container_db = data["db"];
    //change the container_db to a string
    var container_db_string = JSON.stringify(container_db);

    var container_table = data["table"];
    $("#tabs").html(container_table);

    // change the html for the topology div
    var updated_html = '<div class="flex-box">';
    for (var i = 0; i < container_db.length; i++) {
      var status = container_db[i][3];
      if (status == 1) {
        docker_div = '<div class="container-active">';
      } else {
        docker_div = '<div class="container-inactive">';
      }
      docker_div += "<p>" + container_db[i] + "</p>";
      docker_div += "</div>";
      updated_html += docker_div;
    }
    updated_html += "</div>";
    $("#topology").html(updated_html);
  });
});
