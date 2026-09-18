import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestPhysioClinicSite(unittest.TestCase):
    def setUp(self):
        self.html_files = [
            os.path.join(BASE_DIR, "index.html"),
            os.path.join(BASE_DIR, "cookie-policy.html"),
            os.path.join(BASE_DIR, "privacy-notice.html"),
            os.path.join(BASE_DIR, "website-terms.html")
        ]
        self.banned_patterns = [
            r"farzana",
            r"jamil",
            r"gyneco",
            r"matern",
            r"pregnan",
            r"city hospital",
            r"6949109",
            r"0300-6949109"
        ]

    def test_html_files_exist(self):
        for filepath in self.html_files:
            self.assertTrue(os.path.isfile(filepath), f"Missing file: {filepath}")

    def test_no_legacy_terms_in_html(self):
        for filepath in self.html_files:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            for pattern in self.banned_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                self.assertIsNone(
                    match,
                    f"Found legacy term '{pattern}' in {os.path.basename(filepath)}"
                )

    def test_new_branding_in_index(self):
        index_path = os.path.join(BASE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Physio Clinic", content)
        self.assertIn("Dr. Talib Hussain", content)
        self.assertIn("Al Fareed Garden", content)
        self.assertIn("Pakpattan", content)
        self.assertIn("https://www.facebook.com/physiopakpattan/", content)
        self.assertIn("Physio+Clinic+Al+Fareed+Garden+Pakpattan", content)
        self.assertIn("noindex, nofollow, noarchive, nosnippet", content)

    def test_no_clinic_whatsapp_buttons_in_html(self):
        for filepath in self.html_files:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(
                "wa.me/923224658174",
                content,
                f"Found clinic WhatsApp link in {os.path.basename(filepath)}"
            )
            self.assertNotIn(
                "WhatsApp Now",
                content,
                f"Found 'WhatsApp Now' button in {os.path.basename(filepath)}"
            )

    def test_assets_exist(self):
        images_dir = os.path.join(BASE_DIR, "assets", "images")
        required_images = [
            "physio-clinic-logo.png",
            "physio-hero.webp",
            "physio-doctor.webp",
            "physio-clinic.webp",
            "physio-consultation.webp",
            "topic-pain-management.webp",
            "topic-spine-back-care.webp",
            "topic-joint-rehabilitation.webp",
            "topic-posture-ergonomics.webp",
            "topic-sports-injury.webp",
            "topic-follow-up-care.webp",
            "map-artwork.svg",
            "pattern-care.svg"
        ]
        for img in required_images:
            img_path = os.path.join(images_dir, img)
            self.assertTrue(os.path.isfile(img_path), f"Missing asset: {img_path}")

    def test_no_legacy_terms_in_svg(self):
        images_dir = os.path.join(BASE_DIR, "assets", "images")
        for svg_name in ["map-artwork.svg", "pattern-care.svg"]:
            svg_path = os.path.join(images_dir, svg_name)
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            for pattern in self.banned_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                self.assertIsNone(
                    match,
                    f"Found legacy term '{pattern}' in {svg_name}"
                )

    def test_design_and_readme_updated(self):
        for doc in ["physio-clinic-design.md", "README.md"]:
            doc_path = os.path.join(BASE_DIR, doc)
            self.assertTrue(os.path.isfile(doc_path), f"Missing doc file: {doc_path}")
            with open(doc_path, "r", encoding="utf-8") as f:
                content = f.read()
            for pattern in self.banned_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                self.assertIsNone(
                    match,
                    f"Found legacy term '{pattern}' in {doc}"
                )

    def test_desktop_header_order(self):
        index_path = os.path.join(BASE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        brand_idx = content.find('class="brand"')
        nav_idx = content.find('class="primary-navigation"')
        call_btn_idx = content.find('class="button button--primary header-call-btn"')

        self.assertTrue(brand_idx != -1 and nav_idx != -1 and call_btn_idx != -1)
        self.assertLess(brand_idx, nav_idx, "Brand logo must appear before primary navigation in header")
        self.assertLess(nav_idx, call_btn_idx, "Primary navigation must appear before Call Now button in header")

    def test_robots_txt(self):
        robots_path = os.path.join(BASE_DIR, "robots.txt")
        self.assertTrue(os.path.isfile(robots_path))
        with open(robots_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Disallow: /", content)

if __name__ == "__main__":
    unittest.main()
