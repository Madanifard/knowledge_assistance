import os
import json
from docling import Document


class PDFExtractor:
    def __init__(self, pdf_path, output_dir="outputs"):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.doc = Document(pdf_path)
        self.parsed = None
        self.metadata = {}

    def parse(self):
        self.parsed = self.doc.parse()

    # ---------------------------
    # Utility to get file size
    # ---------------------------
    def _file_size_kb(self, path):
        return round(os.path.getsize(path) / 1024, 3)

    # ---------------------------------------
    #  MARKDOWN
    # ---------------------------------------
    def save_markdown(self):
        md = self.parsed.to_markdown()
        path = os.path.join(self.output_dir, "output.md")

        with open(path, "w", encoding="utf8") as f:
            f.write(md)

        self.metadata["markdown"] = {
            "path": path,
            "size_kb": self._file_size_kb(path),
            "word_count": len(md.split())
        }

        return path

    # ---------------------------------------
    #  JSON
    # ---------------------------------------
    def save_json(self):
        js = self.parsed.to_json()
        path = os.path.join(self.output_dir, "output.json")

        with open(path, "w", encoding="utf8") as f:
            f.write(js)

        self.metadata["json"] = {
            "path": path,
            "size_kb": self._file_size_kb(path),
            "elements": len(json.loads(js).get("elements", []))
        }

        return path

    # ---------------------------------------
    #  TEXT
    # ---------------------------------------
    def save_text(self):
        txt = self.parsed.to_text()
        path = os.path.join(self.output_dir, "output.txt")

        with open(path, "w", encoding="utf8") as f:
            f.write(txt)

        self.metadata["text"] = {
            "path": path,
            "size_kb": self._file_size_kb(path),
            "char_count": len(txt),
            "line_count": len(txt.splitlines())
        }

        return path

    # ---------------------------------------
    #  HTML
    # ---------------------------------------
    def save_html(self):
        html = self.parsed.to_html()
        path = os.path.join(self.output_dir, "output.html")

        with open(path, "w", encoding="utf8") as f:
            f.write(html)

        self.metadata["html"] = {
            "path": path,
            "size_kb": self._file_size_kb(path),
            "tag_count": html.count("<")
        }

        return path

    # ---------------------------------------
    #  TABLES
    # ---------------------------------------
    def save_tables(self):
        table_paths = []
        table_meta = []

        for idx, table in enumerate(self.parsed.tables):
            csv_path = os.path.join(self.output_dir, f"table_{idx+1}.csv")
            with open(csv_path, "w", encoding="utf8") as f:
                f.write(table.to_csv())

            meta = {
                "path": csv_path,
                "rows": len(table.rows),
                "cols": len(table.columns),
                "page": table.page_number,
                "size_kb": self._file_size_kb(csv_path)
            }
            table_meta.append(meta)
            table_paths.append(csv_path)

        self.metadata["tables"] = table_meta
        return table_paths

    # ---------------------------------------
    #  IMAGES
    # ---------------------------------------
    def save_images(self):
        image_paths = []
        image_meta = []

        for idx, img in enumerate(self.parsed.images):
            img_bytes = img.to_image()
            img_path = os.path.join(self.output_dir, f"image_{idx+1}.png")

            with open(img_path, "wb") as f:
                f.write(img_bytes)

            meta = {
                "path": img_path,
                "width": img.width,
                "height": img.height,
                "page": img.page_number,
                "size_kb": self._file_size_kb(img_path),
            }

            image_meta.append(meta)
            image_paths.append(img_path)

        self.metadata["images"] = image_meta
        return image_paths

    # ---------------------------------------
    # EXPORT EVERYTHING
    # ---------------------------------------
    def export_all(self):
        self.parse()

        self.save_markdown()
        self.save_json()
        self.save_text()
        self.save_html()
        self.save_tables()
        self.save_images()

        return self.metadata
