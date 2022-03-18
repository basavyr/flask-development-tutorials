$("document").ready(() => {
  console.log("App started successfully");
  sio = io();

  $("#docker_view").click(() => {
    sio.emit("get_container_db");
  });
});
