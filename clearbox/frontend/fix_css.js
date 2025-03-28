const fs = require("fs");
const file = "./src/App.css";

let css = fs.readFileSync(file, "utf8");
css = css.replace(
  /input:disabled,\s+button:disabled\s+{\s+opacity:\s+0\.5;\s+\/\* Enhanced font/,
  "input:disabled,\nbutton:disabled {\n  opacity: 0.5;\n}\n/* Enhanced font"
);
fs.writeFileSync(file, css);