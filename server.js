import express from "express";
import fs from "fs";
import path from "path";
import { generatePoster } from "./generate.js";

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));
app.use("/assets", express.static("assets"));
app.use("/output", express.static("output"));
app.use("/fonts", express.static("fonts"));

app.post("/generate", async (req, res) => {
  const data = req.body;

  fs.writeFileSync(
    "data/poster.json",
    JSON.stringify(data, null, 2)
  );

  await generatePoster();

  res.redirect("/output/poster.png");
});

app.listen(PORT, () => {
  console.log(`Poster Generator running on http://localhost:${PORT}`);
});
