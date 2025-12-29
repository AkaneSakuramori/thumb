import express from "express";
import fs from "fs";
import path from "path";
import multer from "multer";
import { generatePoster } from "./generate.js";

const app = express();
const PORT = 5000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(express.static("public"));
app.use("/assets", express.static("assets"));
app.use("/fonts", express.static("fonts"));
app.use("/data", express.static("data"));
app.use("/templates", express.static("templates"));
app.use("/output", express.static("output"));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (file.fieldname === "backgroundImage") {
      cb(null, "assets/backgrounds");
    } else {
      cb(null, "assets/characters");
    }
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

app.post(
  "/generate",
  upload.fields([
    { name: "backgroundImage", maxCount: 1 },
    { name: "characterImage", maxCount: 1 }
  ]),
  async (req, res) => {
    const body = req.body;

    const posterData = {
      title: body.title,
      subtitle: body.subtitle,
      badge: body.badge,
      nav: body.nav,
      synopsis: body.synopsis,
      genres: body.genres,
      accentColor: body.accentColor,
      backgroundImage: `/assets/backgrounds/${req.files.backgroundImage[0].filename}`,
      characterImage: `/assets/characters/${req.files.characterImage[0].filename}`
    };

    if (!fs.existsSync("data")) fs.mkdirSync("data");

    fs.writeFileSync("data/poster.json", JSON.stringify(posterData, null, 2));

    await generatePoster();

    res.redirect("/output/poster.png");
  }
);

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Poster Generator running on http://localhost:${PORT}`);
});
