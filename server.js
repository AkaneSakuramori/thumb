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
    const ext = path.extname(file.originalname);
    cb(null, Date.now() + ext);
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
    try {
      const body = req.body;

      const posterData = {
        title: body.title,
        subtitle: body.subtitle,
        tag: body.tag,
        synopsis: body.synopsis,
        accentColor: body.accentColor,
        backgroundImage: `/assets/backgrounds/${req.files.backgroundImage[0].filename}`,
        characterImage: `/assets/characters/${req.files.characterImage[0].filename}`
      };

      if (!fs.existsSync("data")) {
        fs.mkdirSync("data");
      }

      fs.writeFileSync("data/poster.json", JSON.stringify(posterData, null, 2));

      await generatePoster();

      res.redirect("/output/poster.png");
    } catch (err) {
      console.error(err);
      res.status(500).send("Poster generation failed");
    }
  }
);

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Poster Generator running on http://localhost:${PORT}`);
});
