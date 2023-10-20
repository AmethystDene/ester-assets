import Gio from "gi://Gio";

const path = Gio.File.new_for_uri(
  workbench.resolve("esteros25.svg"),
).get_path();

workbench.builder.get_object("icon1").file = path;

const button = workbench.builder.get_object("mainbutton");
button.connect("clicked", onClicked);

function onClicked(button) {
  console.log("Installation started");
}

