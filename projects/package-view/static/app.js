$("document").ready(() => {
  console.log("App started successfully");

  sio = io();

  sio.on("connect", () => {
    console.log("Connected to server");

    //emit a message to the server
    sio.emit("on_connect", {
      msg: "App is working fine!",
    });
  });

  // console log when user clicks on "instance-refresher" button
  $("#instance-refresher").click(() => {
    console.log("Refreshing instances");
    sio.emit("refresh_instances");
  });

  //save the active_instances list from the server as an array
  sio.on("active_instances", (data) => {
    console.log(data);
  });
});
