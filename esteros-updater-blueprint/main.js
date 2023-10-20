import Gio from "gi://Gio";

const path = Gio.File.new_for_uri(
  workbench.resolve("esteros25.svg"),
).get_path();

workbench.builder.get_object("icon1").file = path;

