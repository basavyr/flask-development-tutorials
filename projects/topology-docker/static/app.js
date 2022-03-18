$("document").ready(() => {
  console.log("App started successfully");
  sio = io();
  
  $("#docker_view").click(() => {
    sio.emit("get_container_db");
  });
  
  // set the added-text div to hidden
  $("#added-text").hide();

  $("#map-button").click(() => {
    console.log("User clicked the topology button");
    //show the added-text div
    $("#added-text").toggle();
    // $("#added-text").html("<p>Will show the map.</p>");
  });
});
