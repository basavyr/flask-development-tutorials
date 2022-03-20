$("document").ready(() => {
  console.log("App started successfully");

  sio = io();

  var retrieve_db_on_document_ready = true;
  if (retrieve_db_on_document_ready) {
    // console.log("Will retrieve db on document ready");
    sio.emit("get_container_db");
  } else console.log("No db retrieval required");

  sio.on("container_db", (data) => {
    console.log("Received the container db:\n" + data["db"]);
  });

  $("#tabular-view").click(() => {
    console.log("User requested tabular view");
    sio.emit("get_container_db");
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
    sio.emit("get_container_db");
    console.log("User requested topology view");

    if ($("#tabs").is(":visible")) {
      $("#tabs").hide();
    }

    $("#topology").toggle();

    //toggle the topology div only if the tabular view is not toggled
    if ($("#topology").is(":hidden")) {
      $("#tabs").hide();
    }
  });
});
