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
    // retrieve the pre-defined html table template from the server
    var tabular_html = data["table"];
    $("#tabs").html(tabular_html);

    // retrieve the container database and draw the topology
    var container_topology = data["db"];
    var tabular_html = '<div class="flex-box">';
    for (var i = 0; i < container_topology.length; i++) {
      var status = container_topology[i][3];
      if (status == 1) {
        container_div = '<div class="container-active">';
      } else {
        container_div = '<div class="container-inactive">';
      }
      container_div += "<p>" + container_topology[i] + "</p>";
      container_div += "</div>";
      tabular_html += container_div;
    }
    tabular_html += "</div>";
    // change the html for the topology div
    $("#topology").html(tabular_html);
  });
});
