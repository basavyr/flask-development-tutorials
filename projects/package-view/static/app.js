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

    //when user clicks on "instance-refresher" button, clear the "container-table" table
    $("#vm-table > tbody").empty();
    //hide the table
    $("#vm-table").hide();
    //hide the "container-name-title" div
    $("#vm-name-title").hide();

    //when user clicks on "instance-refresher" button, clear the "container-table" table
    $("#container-table > tbody").empty();
    //hide the table
    $("#container-table").hide();
    //hide the "container-name-title" div
    $("#container-name-title").hide();

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

    // //remove the element from the container-drp-list
    // $("#container-drp-list").empty();
    // //print every container into the dropdown list
    // data.containers.forEach((element) => {
    //   //extract the container name and container id
    //   let containerName = element[0];
    //   let containerId = element[1];
    // //   console.log(containerName);
    // //   console.log(containerId);
    //   //add each array item into the "container-drp-list" dropdown list
    //   $("#container-drp-list").append(
    //     '<a class="dropdown-item" href="#">' + containerName + "</a>"
    //   );
    // });
  });

  //actions when the user selects an item from vm-drp-list
  $("#vm-drp-list").on("click", "a", (e) => {
    console.log("VM selected: " + e.target.text);

    make_table = true;
    //do not create a table if there is no vm list
    if (e.target.text === "empty...") {
      make_table = false;
    }

    if (make_table === true) {
      $("#vm-name-title").css("display", "block");
      $("#vm-name-title").text(e.target.text);
      $("#vm-name-title").css("font-weight", "bold");
      $("#vm-name-title").css("font-family", "console");

      //after user selects an item from the dropdown list, generate a table with two columns and 5 rows
      //make the table visible
      $("#vm-table").css("display", "block");

      // make the vm-table empty but do not remove the table header
      // https://stackoverflow.com/questions/370013/jquery-delete-all-table-rows-except-first
      // https://stackoverflow.com/a/8053924/8295213
      $("#vm-table > tbody").empty();

      $("#vm-table").append("<tbody>");
      $("#vm-table").append('<tr class="table-success">');

      //generate a random number between 1 and 8
      let num_of_columns = Math.floor(Math.random() * (8 - 3 + 1)) + 3;
      for (let i = 0; i < num_of_columns; i++) {
        $("#vm-table").append(
          "<tr><td>" +
            "package-" +
            i +
            "</td><td>" +
            "version-" +
            i +
            "</td></tr>"
        );
      }
      $("#vm-table").append("</tr>");
      $("#vm-table").append("</tbody>");
      //when user selects an item from vm-drp-list, show the "vm-container-box" div
      $("#vm-container-box").css("display", "block");

      //get the text from the "vm-name-for-containers" paragraph
      let vm_name = $("#vm-name-for-containers").text();
      let new_paragraph = vm_name + " " + e.target.text + ".";
      //set the value for the "vm-name-for-containers" paragraph to new_paragraph
      $("#vm-name-for-containers").text(new_paragraph);
    }

    sio.emit("vm_selected", {
      vm: e.target.text,
    });
  });

  //actions when the user selects an item from container-drp-list
  $("#container-drp-list").on("click", "a", (e) => {
    console.log("Container selected: " + e.target.text);

    make_table = true;
    //do not create a table if there is no vm list
    if (e.target.text === "empty...") {
      make_table = false;
    }

    if (make_table === true) {
      //after user selects an item from the dropdown list, generate a table with two columns and 5 rows

      //make the "container-name-title" div visible
      $("#container-name-title").css("display", "block");
      //set the "container-name-title" div to the selected container name
      $("#container-name-title").text(e.target.text);
      //set the font weight of the "container-name-title" div to bold
      $("#container-name-title").css("font-weight", "bold");
      //set the font of the "container-name-title" div to console
      $("#container-name-title").css("font-family", "console");

      //make the table visible
      $("#container-table").css("display", "block");

      // make the vm-table empty but do not remove the table header
      // https://stackoverflow.com/questions/370013/jquery-delete-all-table-rows-except-first
      // https://stackoverflow.com/a/8053924/8295213
      $("#container-table > tbody").empty();

      $("#container-table").append("<tbody>");
      $("#container-table").append('<tr class="table-success">');

      //generate a random number between 1 and 3
      let num_of_columns = Math.floor(Math.random() * (3 - 1 + 1)) + 1;
      for (let i = 0; i < num_of_columns; i++) {
        $("#container-table").append(
          "<tr><td>" +
            "package-" +
            i +
            "</td><td>" +
            "version-" +
            i +
            "</td></tr>"
        );
      }
      $("#container-table").append("</tr>");
      $("#container-table").append("</tbody>");
    }
    sio.emit("container_selected", {
      container: e.target.text,
    });
  });
});
