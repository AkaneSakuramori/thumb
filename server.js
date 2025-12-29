import express from "express";
import fs from "fs";
import path from "path";
import { generatePoster } from "./generate.js";

const app = express();
const PORT = 5000; // keep 5000 since you are using it already

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ==========================
// STATIC FILES (IMPORTANT)
// ==========================
app.use(express.static("public"));
app.use("/assets", express.static("assets"));
app.use("/fonts", express.static("fonts"));
app.use("/data", express.static("data"));
app.use("/templates", express.static("templates"));
app.use("/output", express.static("output"));

// ==========================
// GENERATE POSTER
// ==========================
app.post("/generate", async (req, res) => {
  try {
    const data = req.body;

    // Ensure data directory exists
    if (!fs.existsSync("data")) {
      fs.mkdirSync("data");
    }

    fs.writeFileSync(
      "data/poster.json",
      JSON.stringify(data, null, 2)
    );

    await generatePoster();

    res.redirect("/output/poster.png");
  } catch (err) {
    console.error("Poster generation failed:", err);
    res.status(500).send("Poster generation failed");
  }
});

// ==========================
// START SERVER
// ==========================
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Poster Generator running on http://localhost:${PORT}`);
});
