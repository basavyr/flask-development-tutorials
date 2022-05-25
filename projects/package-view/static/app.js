$("document").ready(() => {
  console.log("App started successfully");

  sio = io();

  let vm_id_list = [];
  let vm_name_list = [];

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

    data.vms.forEach((element) => {
      let vm_name = element[1];
      let vm_id = element[0];

      //add each array item into the "vm-drp-list" dropdown list
      $("#vm-drp-list").append(
        '<a class="dropdown-item" href="#">' + vm_name + "</a>"
      );

      // add the id to the vm_id_list array
      vm_id_list.push(vm_id);
      // add the name to the vm_name_list array
      vm_name_list.push(vm_name);
    });
  });

  //actions when the user selects an item from vm-drp-list
  $("#vm-drp-list").on("click", "a", (e) => {
    //assume the table should be created
    make_table = true;

    //clear the vm-table first
    $("#vm-table > tbody").empty();

    //do not create a table if there is no vm list
    if (e.target.text === "empty...") {
      make_table = false;
    }

    if (make_table === true) {
      selected_vm = e.target.text;
      //check the position of the selected item in the vm-drp-list
      let selected_vm_index = $("#vm-drp-list a").index(e.target) + 1;

      sio.emit("vm_selected", {
        vm_id: vm_id_list[selected_vm_index - 1],
        vm_name: vm_name_list[selected_vm_index - 1],
      });

      //wait for the server to send the packages on the VM that was previously selected
      sio.on("vm_packages", (data) => {
        // tuple list which contains the package name and the package version
        vm_packages = data["vm_packages"];

        $("#vm-table > tbody").empty();
        $("#vm-name-title").css("display", "block");
        // $("#vm-name-title").html(
        //   "<code>VM: " + vm_name_list[selected_vm_index - 1] + "</code>"
        // );
        $("#vm-name-title").html(vm_name_list[selected_vm_index - 1]);
        $("#vm-name-title").css("font-weight", "bold");
        $("#vm-name-title").css("font-family", "console");
        $("#vm-id-title").css("display", "block");
        $("#vm-id-title").html(vm_id_list[selected_vm_index - 1]);
        // $("#vm-id-title").html(
        //   "<code>VM ID: " + vm_id_list[selected_vm_index - 1] + "</code>"
        // );
        $("#vm-id-title").css("font-weight", "bold");
        $("#vm-id-title").css("font-family", "console");

        //after user selects an item from the dropdown list, generate a table with two columns and 5 rows
        //make the table visible
        $("#vm-table").css("display", "block");

        // make the vm-table empty but do not remove the table header
        // https://stackoverflow.com/questions/370013/jquery-delete-all-table-rows-except-first
        // https://stackoverflow.com/a/8053924/8295213
        $("#vm-table > tbody").empty();

        // $("#vm-table").append("<tbody>");

        //add each tuple item from vm_packages to the table
        //console log every item from vm_packages
        for (let i = 0; i < vm_packages.length; i++) {
          $("#vm-table > tbody").append(
            '<tr class="table-primary"><td>' +
              vm_packages[i][0] +
              "</td><td>" +
              vm_packages[i][1] +
              "</td>" +
              "<td>" +
              vm_packages[i][2] +
              "</td>" +
              "<td>" +
              //make a button called CHECK
              '<button type="button" class="btn btn-primary btn-sm" id="check-update-button">' +
              "CHECK" +
              "</button>" +
              "</td>" +
              //make a button called UPDATE
              '<td><button type="button" class="btn btn-danger btn-sm" id="update-button">' +
              "UPDATE" +
              "</button></td>" +
              "</tr>"
          );
        }

        $("#vm-table").append("</tbody>");
      });

      //when user selects an item from vm-drp-list, show the "vm-container-box" div
      $("#vm-container-box").css("display", "block");

      //get the text from the "vm-name-for-containers" paragraph
      let paragraph = "The containerized services that run on the VM ";
      let vm_name = $("#vm-name-for-containers").text();
      let new_paragraph =
        "<p>" +
        paragraph +
        " <b style='font-family: console;'>" +
        e.target.text +
        "</b>." +
        "<p>";

      //set the value for the "vm-name-for-containers" to the new paragraph
      $("#vm-name-for-containers").html(new_paragraph);
      // $("#vm-name-for-containers").css("font-family", "console");
      // $("#vm-name-for-containers").css("font-weight", "bold");
    }
  });

  //once the user selected a virtual machine, generate the available containers list for that specific VM
  sio.on("available_vm_containers", (data) => {
    //remove the first element from the container-drp-list
    $("#container-drp-list").empty();

    //append the data to the container-drp-list dropdown list
    data["vm_containers"].forEach((element) => {
      let containerName = element[0];
      let containerId = element[1];
      $("#container-drp-list").append(
        '<a class="dropdown-item" href="#">' + containerName + "</a>"
      );
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

      // //add the data into the container-table
      // // make the vm-table empty but do not remove the table header
      // // https://stackoverflow.com/questions/370013/jquery-delete-all-table-rows-except-first
      // // https://stackoverflow.com/a/8053924/8295213
      // $("#container-table > tbody").empty();

      // $("#container-table").append("<tbody>");
      // $("#container-table").append('<tr class="table-success">');

      // for (let i = 0; i < 3; i++) {
      //   $("#container-table").append(
      //     "<tr><td>" +
      //       "package-" +
      //       i +
      //       "</td><td>" +
      //       "version-" +
      //       i +
      //       "</td></tr>"
      //   );
      // }
      // $("#container-table").append("</tr>");
      // $("#container-table").append("</tbody>");
    }
  });

  //check when the user clicks on the "check-update-button" button from the vm-table
  $("#vm-table").on("click", "#check-update-button", (e) => {
    //select the first element of the selected row
    let package_name = e.target.parentNode.parentNode.children[0].textContent;

    //get the current "vm-name-title"
    let vm_name = $("#vm-name-title").text();
    let vm_id = $("#vm-id-title").text();
    console.log(
      "Will check updates for " + package_name + "on the VM with ID: " + vm_id
    );
    sio.emit("check_update", { vm_id: vm_id, package: package_name });
  });

  //check when the user clicks on the "update-button" button from the vm-table
  $("#vm-table").on("click", "#update-button", (e) => {
    //select the first element of the selected row
    let package_name = e.target.parentNode.parentNode.children[0].textContent;

    //get the current "vm-name-title"
    let vm_name = $("#vm-name-title").text();
    let vm_id = $("#vm-id-title").text();
    console.log(
      "Will update " + package_name + " for the VM with ID: " + vm_id
    );
    sio.emit("update", { vm_id: vm_id, package: package_name });
  });
});
