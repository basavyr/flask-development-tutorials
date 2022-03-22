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
    // console.log("Received a new container db");
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
      container_div +=
        "<p> <strong>Container #" + container_topology[i][0] + "</strong></p>";
      // container_div +=
      //   "<p> <strong>Container #" + container_topology[i][0] + "</strong></p>";
      container_div += "</div>";
      tabular_html += container_div;
    }
    tabular_html += "</div>";
    // change the html for the topology div
    $("#topology").html(tabular_html);

    //access the action-stop-container class and add a click event listener
    $(".action-stop-container").click(() => {
      // console.log("User clicked STOP container");
    });

    //access the action-start-container class and add a click event listener
    $(".action-start-container").click(() => {
      // console.log("User clicked START container");
    });

    // get the table row when the start button of a particular container is clicked
    // source https://codepedia.info/jquery-get-table-cell-td-value-div
    // source https://stackoverflow.com/questions/14460421/get-the-contents-of-a-table-row-with-a-button-click
    // source https://stackoverflow.com/questions/376081/how-to-get-a-table-cell-value-using-jquery
    // source https://stackoverflow.com/questions/19832621/how-to-get-the-value-of-tr-of-a-table-using-jquery-on-click
    $(".docker-tabular").on("click", ".action-start-container", function () {
      var current_container = $(this).closest("tr");
      var container_id = current_container.find("td:eq(1)").text();

      sio.emit("docker_action", { req: "START", container_id: container_id });
    });

    $(".docker-tabular").on("click", ".action-stop-container", function () {
      var current_container = $(this).closest("tr");
      var container_id = current_container.find("td:eq(1)").text();

      sio.emit("docker_action", { req: "STOP", container_id: container_id });
    });
  });

  $(".topology").on("click", ".container-active", function () {
    // console.log("User clicked on active container");
    box_text = $(this).find("p").text();
    container_id = box_text.substring(box_text.indexOf("#") + 1);
    // console.log(container_id);
    sio.emit("request_container_details", {
      container_id: container_id,
      req: "STOP",
    });
  });

  sio.on("response_container_details", function (msg) {
    console.log(msg.status);
    var cont = $(".topology").find(".container-active p");
    console.log(cont);
    cont.append("<p>" + msg.status + "</p>");
  });

  $(".topology").on("click", ".container-inactive", function () {
    // console.log("User clicked on inactive container");
    box_text = $(this).find("p").text();
    container_id = box_text.substring(box_text.indexOf("#") + 1);
    // sio.emit("request_container_details");
  });
});
