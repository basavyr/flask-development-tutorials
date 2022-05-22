$("document").ready(() => {
  console.log("App started successfully");

  sio = io();

  sio.on("connect", () => {
    console.log("Connected to server");
    //emit a message to the server
    sio.emit("on_message", {
        data: "Hello from the client"
    });
  });
});
