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

  //save the instances list from the server as an array
  sio.on("instances", (data) => {
    //remove the element from the vm-drp-list
    $("#vm-drp-list").empty();
    //print every element from the array
    data.vms.forEach((element) => {
      //add each array item into the "vm-drp-list" dropdown list
      $("#vm-drp-list").append(
        '<a class="dropdown-item" href="#">' + element + "</a>"
      );
    });

    //remove the element from the container-drp-list
    $("#container-drp-list").empty();
    //print every container into the dropdown list
    data.containers.forEach((element) => {
      //add each array item into the "container-drp-list" dropdown list
      $("#container-drp-list").append(
        '<a class="dropdown-item" href="#">' + element + "</a>"
      );
    });
  });

  //console log when user selects an item from container-drp-list
  $("#container-drp-list").on("click", "a", (e) => {
    console.log("Container selected: " + e.target.text);
    sio.emit("container_selected", {
      container: e.target.text,
    });
  });
});
