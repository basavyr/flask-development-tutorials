//************************************************************************** */
//************************************************************************** */
//************************************************************************** */
//************************************************************************** */
//************************************************************************** */
// The system statistics app module

$("document").ready(() => {
  console.log("App-Stats started successfully");

  sio = io();

  sio.on("connect", () => {
    console.log("Connected to server");

    //emit a message to the server
    sio.emit("on_connect", {
      msg: "App is working fine!",
    });
  });

  sio.emit("refresh_instances_stats");

  // console log when user clicks on the System Statistics button in the navbar
  $("#system-statistics").on("click", () => {
    // $("#system-statistics").ready(() => {
    console.log("System Statistics button clicked");
  });

  let vm_id_list = [];
  let vm_name_list = [];

  //save the instances list from the server as an array
  sio.on("instances_stats", (data) => {
    // console log the data
    vms = data["vms"];

    vms.forEach((element) => {
      vm_id_list.push(element[0]);
      vm_name_list.push(element[1]);
    });
    //clean the "vm-list-stats" dropdown list first
    $("#vm-list-stats").empty();
    // add every item from vm_name_list to the "vm-list-stats" dropdown list
    vm_name_list.forEach((element) => {
      $("#vm-list-stats").append(
        '<a class="dropdown-item" href="#">' + element + "</a>"
      );
    });
  });

  //get the value of the "vm-list-stats" element when user clicks
  $("#vm-list-stats").on("click", (e) => {
    //check the position of the selected item in the vm-list-stats
    let selected_index = $("#vm-list-stats a").index(e.target) + 1;
    let selected_vm_id = vm_id_list[selected_index - 1];

    show_stats = true;

    if (e.target.text === "empty...") {
      show_stats = false;
    }

    if (show_stats === true) {
      sio.emit("get_vm_stats", { vm_id: selected_vm_id });
      html_element_name =
        "<h4><p>VM: <code>" +
        vm_name_list[selected_index - 1] +
        "</code></p></h4>";
      html_element_id =
        "<h4><p>VM ID: <code>" +
        vm_id_list[selected_index - 1] +
        "</code></p></h4>";

      //set the html for "box-vm-name" to html_element
      $("#box-vm-name").html(html_element_name);
      //set the html for "box-vm-id" to html_element
      $("#box-vm-id").html(html_element_id);

      //show the unified-vm-stats div
      $("#unified-vm-stats").css("display", "block");
      // change the html for the div "vm_id_stats" to the selected vm id
      $("#vm_id_stats").html(vm_id_list[selected_index - 1]);
      // change the html for the div "vm_name_stats" to the selected vm name
      $("#vm_name_stats").html(vm_name_list[selected_index - 1]);
    }
  });
});
