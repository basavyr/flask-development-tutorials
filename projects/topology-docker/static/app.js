$("document").ready(() => {
  console.log("App started successfully");
  sio = io();

  $("#docker_view").click(() => {
    sio.emit("get_container_db");
  });

  $("#map-button").click(() => {
    console.log("User clicked the topology button");
    $("#added-text").html("<p>Will show the map.</p>");
  });
});
