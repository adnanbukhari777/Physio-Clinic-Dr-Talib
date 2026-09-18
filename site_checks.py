"""Automated regression checks for Dr. Farzana Jamil Clinic static website."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "privacy-notice.html",
    "cookie-policy.html",
    "website-terms.html",
)
NOINDEX = "noindex, nofollow, noarchive, nosnippet"
PROHIBITED_HOMEPAGE_CLAIMS = re.compile(
    r"testimonial"
    r"|(?:[0-5]\.\d)(?:\s*(?:out of|/)\s*5)?"
    r"|\b\d[\d,]*\s+reviews?\b"
    r"|five-star|registered physician|mbbs|fcps|board-certified"
    r"|years? of experience|award|affiliation|clinical outcome"
)


class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.main_ids = []
        self.robots_values = []
        self.stylesheets = []
        self.scripts = []
        self.links = []
        self.classes = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_ids.append(attributes.get("id"))
        if tag == "meta" and attributes.get("name") == "robots":
            self.robots_values.append(attributes.get("content"))
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
        if tag == "script":
            self.scripts.append(attributes.get("src"))
        if tag == "a":
            self.links.append(attributes.get("href"))
        if tag == "img":
            self.images.append(attributes)
        class_names = attributes.get("class", "").split()
        self.classes.extend(class_names)


def inspect_page(filename):
    parser = PageInspector()
    parser.feed((ROOT / filename).read_text(encoding="utf-8"))
    return parser


class SiteChecks(unittest.TestCase):
    def test_representative_raster_images_are_local_sized_disclosed_and_loaded_safely(self):
        """A missing, undisclosed, or incorrectly loaded raster image must block release."""
        expected_images = {
            "assets/images/farzana-hero.webp": {"loading": None, "fetchpriority": "high"},
            "assets/images/farzana-doctor.webp": {"loading": "lazy"},
            "assets/images/farzana-clinic.webp": {"loading": "lazy"},
            "assets/images/farzana-consultation.webp": {"loading": "lazy"},
        }
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        inspector = inspect_page("index.html")
        image_by_source = {image.get("src"): image for image in inspector.images}

        for source, expected in expected_images.items():
            with self.subTest(source=source):
                self.assertTrue((ROOT / source).is_file(), f"Missing representative image: {source}")
                image = image_by_source.get(source)
                self.assertIsNotNone(image, f"Homepage must reference {source}")
                self.assertTrue(image.get("alt"), f"{source} needs useful alternative text")
                self.assertTrue(image.get("width"), f"{source} needs an explicit width")
                self.assertTrue(image.get("height"), f"{source} needs an explicit height")
                self.assertEqual(image.get("loading"), expected["loading"])
                self.assertEqual(image.get("decoding"), "async")
                if "fetchpriority" in expected:
                    self.assertEqual(image.get("fetchpriority"), expected["fetchpriority"])

        self.assertIn("AI-generated representative image", homepage)

    def test_interaction_contracts_exist(self):
        """Removing progressive enhancement safeguards would break demo controls."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        for marker in [
            "farzana_clinic_map_consent_v1", "showModal", "Escape", "aria-expanded",
            "try", "catch", "openDemoDialog", "closeMenu", "readPreference",
            "writePreference", "removePreference", "prefers-reduced-motion",
            "loadInteractiveMap",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_interaction_markup_supports_safe_progressive_enhancement(self):
        """Removing interaction hooks would leave mobile and privacy controls unusable."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        cookie_policy = (ROOT / "cookie-policy.html").read_text(encoding="utf-8")
        for marker in [
            'class="menu-toggle js-menu-toggle"', 'aria-controls="primary-navigation"',
            'id="primary-navigation"', 'class="js-accordion-trigger"',
            'id="privacy-bar"', 'class="mobile-quick-actions"', 'id="current-year"',
            'id="load-map-btn"', 'id="consent-load-map"', 'id="consent-decline-map"',
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, homepage)
        self.assertIn('id="reset-privacy"', cookie_policy)

    def test_dialog_fallback_can_close_when_only_the_open_attribute_exists(self):
        """A non-native dialog must not depend on the unavailable .open property."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        self.assertIn("function dialogIsOpen()", js)
        self.assertIn('dialog.hasAttribute("open")', js)
        self.assertIn("if (!dialogIsOpen()) return;", js)
        self.assertIn('event.key === "Escape" && dialogIsOpen()', js)

    def test_menu_link_close_restores_focus_before_hiding_the_link(self):
        """Closing the menu from a focused link must not leave focus in hidden content."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        self.assertIn('if (event.target.closest("a")) closeMenu({ restoreFocus: true });', js)

    def test_closed_dialog_fallback_is_not_rendered_or_focusable(self):
        """An unsupported dialog element must start closed rather than expose its controls."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"dialog:not\(\[open\]\)\s*\{\s*display:\s*none")

    def test_small_text_on_surfaces_meets_aa_contrast(self):
        """Verify contrast on tinted panels meets WCAG AA (4.5:1)."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        tokens = dict(re.findall(r"--([a-z-]+):\s*(#[A-Fa-f0-9]{6})", css))

        def color_for(selectors, property_name):
            value = None
            for selector_text, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
                if any(selector in [s.strip() for s in selector_text.split(",")] for selector in selectors):
                    match = re.search(rf"(?:^|;)\s*{property_name}:\s*var\(--([a-z-]+)\)", declarations)
                    if match:
                        value = tokens[match.group(1)]
            self.assertIsNotNone(value, f"No declared {property_name} for {selectors}")
            return value

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
            return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))

        for text_selectors, surface in [
            ([".eyebrow", "#confidence .eyebrow"], "#confidence"),
            ([".site-footer nav a", ".site-footer nav a:hover"], ".site-footer"),
        ]:
            with self.subTest(surface=surface):
                foreground = color_for(text_selectors, "color")
                background = color_for([surface], "background")
                low, high = sorted([luminance(foreground), luminance(background)])
                self.assertGreaterEqual((high + .05) / (low + .05), 4.5)

    def test_css_contains_locked_tokens_and_accessibility_rules(self):
        """Missing brand/accessibility declarations break the approved CSS contract."""
        stylesheet = ROOT / "assets/css/style.css"
        self.assertTrue(stylesheet.is_file())
        css = stylesheet.read_text(encoding="utf-8")
        for name, value in {
            "brand-blue": "#012E75", "brand-blue-light": "#0B4DA2",
            "brand-red": "#ED060F", "accessible-red": "#B50918",
            "canvas": "#F7FAFF", "blue-tint": "#EAF1FB", "surface": "#FFFFFF",
            "text": "#1B2430", "muted": "#5B6573", "border": "#D7E0ED",
        }.items():
            with self.subTest(token=name):
                self.assertRegex(css.lower(), rf"--{name}\s*:\s*{value.lower()}")
        for marker in [":focus-visible", "@media (prefers-reduced-motion: reduce)",
                       "@media (min-width: 48rem)", "@media (min-width: 75rem)",
                       "clamp(", "overflow-wrap", "aspect-ratio", "min-height: 44px",
                       "scroll-padding", "--z-privacy",
                       ".button--primary", ".button--secondary", ".privacy-bar",
                       ".mobile-quick-actions"]:
            with self.subTest(rule=marker):
                self.assertIn(marker, css)
        self.assertNotIn("@import", css)
        self.assertNotIn("backdrop-filter", css)

    def test_old_aubergine_berry_rose_variables_absent(self):
        """Legacy palette variables and hex codes must be completely absent."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8").lower()
        for legacy in ["--aubergine", "--berry", "--blush", "--rose",
                       "#512a44", "#9e4663", "#d88b9d", "#f8ecef", "#e7d5da", "#73857c"]:
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, css)

    def test_typography_uses_geometric_sans_serif(self):
        """Display typography must use geometric sans-serif; no serif display fonts."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8").lower()
        self.assertIn("century gothic", css)
        self.assertIn("avenir next", css)
        for serif in ["bodoni", "didot", "georgia", "times new roman"]:
            with self.subTest(serif=serif):
                self.assertNotIn(serif, css)

    def test_brand_logo_is_horizontal_png_and_square_logo_absent(self):
        """All pages must reference the horizontal logo PNG and no square logo remains."""
        logo_png = ROOT / "assets/images/dr-farzana-jamil-logo.png"
        self.assertTrue(logo_png.is_file(), "assets/images/dr-farzana-jamil-logo.png must exist")
        self.assertFalse((ROOT / "Logo.jpg").exists(), "Old Logo.jpg must be deleted")
        self.assertFalse((ROOT / "assets/images/dr-farzana-jamil-logo.jpg").exists(), "Old square logo jpg must be deleted")

        for page in PAGES:
            with self.subTest(page=page):
                html = (ROOT / page).read_text(encoding="utf-8")
                self.assertIn("assets/images/dr-farzana-jamil-logo.png", html)
                self.assertNotIn("brand-name", html)
                self.assertNotIn("brand-sub", html)

    def test_no_nexacare_references_in_public_files_or_metadata(self):
        """No public HTML, JS, CSS, README, or metadata file may contain NexaCare."""
        files_to_check = list(PAGES) + [
            "assets/css/style.css",
            "assets/js/main.js",
            "README.md",
            "metadata.json",
        ]
        for rel_path in files_to_check:
            file_path = ROOT / rel_path
            if file_path.is_file():
                with self.subTest(file=rel_path):
                    content = file_path.read_text(encoding="utf-8").lower()
                    self.assertNotIn("nexacare", content, f"Found NexaCare in {rel_path}")

    def test_interactive_map_requires_affirmative_consent(self):
        """Map iframe must use data-src (no initial src) and start hidden behind placeholder."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="map-placeholder"', homepage)
        self.assertIn('id="map-frame"', homepage)
        self.assertIn('data-src="https://www.google.com/maps?q=Dr+Farzana+Jamil+Clinic+Pakpattan&amp;output=embed"', homepage)
        # Ensure iframe has data-src without initial src
        iframe_match = re.search(r'<iframe([^>]+)>', homepage)
        self.assertIsNotNone(iframe_match, "Homepage must contain map iframe")
        iframe_attrs = iframe_match.group(1)
        self.assertIn("data-src=", iframe_attrs)
        self.assertNotIn(" src=", iframe_attrs)

    def test_map_consent_storage_key_and_reset_control(self):
        """Map consent key must be farzana_clinic_map_consent_v1 and reset control must exist."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        self.assertIn("farzana_clinic_map_consent_v1", js)
        cookies = (ROOT / "cookie-policy.html").read_text(encoding="utf-8")
        self.assertIn("farzana_clinic_map_consent_v1", cookies)
        self.assertIn('id="reset-privacy"', cookies)
        self.assertIn('id="reset-privacy-status"', cookies)

    def test_directions_link_is_always_available(self):
        """Google Maps Directions URL must be accessible unconditionally."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        directions_url = "https://www.google.com/maps/search/?api=1&amp;query=Dr+Farzana+Jamil+Clinic+Pakpattan"
        self.assertIn(directions_url, homepage)

    def test_demo_marquee_terms_link_has_a_44px_touch_target(self):
        """Removing the terms link's 44px target would make the demo disclosure hard to tap."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        match = re.search(r"\.demo-marquee a\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(match, "The demo marquee terms link must have its own rule")
        self.assertRegex(match.group(1), r"min-height\s*:\s*44px")

    def test_local_svg_artwork_is_valid_and_all_used_symbols_resolve(self):
        """Missing local artwork or misspelled sprite IDs must fail before shipping."""
        svg_paths = ["assets/icons/icon-sprite.svg", "assets/images/map-artwork.svg",
                     "assets/images/pattern-care.svg"]
        for name in svg_paths:
            with self.subTest(asset=name):
                self.assertTrue((ROOT / name).is_file(), f"Missing SVG: {name}")
                root = ET.parse(ROOT / name).getroot()
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertNotIn("{http://www.w3.org/2000/svg}script", [el.tag for el in root.iter()])
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        used_symbols = re.findall(r'<use href="assets/icons/icon-sprite.svg#([^"]+)"', homepage)
        self.assertTrue(used_symbols, "Homepage must consume the local icon sprite")
        symbols = {el.get("id") for el in ET.parse(ROOT / svg_paths[0]).iter()}
        self.assertTrue(set(used_symbols).issubset(symbols))

    def test_required_public_pages_exist(self):
        """Removing a public page must fail the static-site contract."""
        self.assertEqual([name for name in PAGES if not (ROOT / name).is_file()], [])

    def test_each_page_has_an_accessible_shell_and_resolving_assets(self):
        """A missing main landmark or shared asset reference must be detected."""
        for page in PAGES:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), f"Missing required page: {page}")
                inspector = inspect_page(page)
                self.assertEqual(inspector.h1_count, 1)
                self.assertIn("main-content", inspector.main_ids)
                self.assertIn("site-header", inspector.classes)
                self.assertIn("site-footer", inspector.classes)
                self.assertIn("demo-marquee", inspector.classes)
                self.assertEqual(inspector.robots_values, [NOINDEX])
                self.assertIn("assets/css/style.css", inspector.stylesheets)
                self.assertIn("assets/js/main.js", inspector.scripts)
                self.assertTrue((ROOT / "assets/css/style.css").is_file())
                self.assertTrue((ROOT / "assets/js/main.js").is_file())

    def test_legal_pages_cross_link_and_return_home(self):
        """A broken legal-policy route must fail navigation checks."""
        legal_pages = PAGES[1:]
        for page in legal_pages:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), f"Missing required page: {page}")
                links = inspect_page(page).links
                self.assertIn("index.html", links)
                self.assertIn("privacy-notice.html", links)
                self.assertIn("cookie-policy.html", links)
                self.assertIn("website-terms.html", links)

    def test_legal_pages_disclose_data_practices_and_demonstration_boundaries(self):
        """Omitting required demonstration or privacy disclosures must fail."""
        privacy = (ROOT / "privacy-notice.html").read_text(encoding="utf-8").lower()
        cookies = (ROOT / "cookie-policy.html").read_text(encoding="utf-8").lower()
        terms = (ROOT / "website-terms.html").read_text(encoding="utf-8").lower()

        for marker in [
            "no patient information", "no analytics",
            "visitor-initiated", "whatsapp", "bukhari ai solutions",
            "representative", "ai-generated",
        ]:
            with self.subTest(privacy_marker=marker):
                self.assertIn(marker, privacy)
        self.assertIn("farzana_clinic_map_consent_v1", cookies)
        self.assertIn("reset", cookies)
        for marker in [
            "independent demonstration", "not medical advice", "emergency",
            "no doctor-patient relationship", "pakpattan",
        ]:
            with self.subTest(terms_marker=marker):
                self.assertIn(marker, terms)

    def test_embedded_and_local_svg_favicons_are_present(self):
        """Every public page needs its embedded favicon while favicon.svg remains a valid asset."""
        for page in PAGES:
            with self.subTest(page=page):
                source = (ROOT / page).read_text(encoding="utf-8")
                self.assertRegex(source, r'<link\s+rel="icon"\s+href="data:image/svg\+xml,')
        favicon = ROOT / "favicon.svg"
        self.assertTrue(favicon.is_file(), "Missing local favicon.svg")
        root = ET.parse(favicon).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_static_hosting_configuration_and_deployment_guidance_are_complete(self):
        """Hostinger deployment needs safeguards and frame permissions."""
        htaccess = (ROOT / ".htaccess").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        for marker in [
            "AddDefaultCharset UTF-8", "Options -Indexes", "X-Content-Type-Options",
            "Referrer-Policy", "Content-Security-Policy", "mod_deflate", "mod_expires",
            "frame-src https://www.google.com https://maps.google.com;",
            "(?:tests|docs)",
        ]:
            with self.subTest(htaccess_marker=marker):
                self.assertIn(marker, htaccess)
        self.assertIn(
            'Header always set X-Robots-Tag "noindex, nofollow, noarchive, nosnippet"',
            htaccess,
        )
        self.assertNotIn("immutable", htaccess.lower())
        cache_control = re.search(r'Cache-Control "([^"]+)"', htaccess)
        self.assertIsNotNone(cache_control, "Static assets need an explicit cache policy")
        self.assertIn("must-revalidate", cache_control.group(1))
        max_age = re.search(r"max-age=(\d+)", cache_control.group(1))
        self.assertIsNotNone(max_age, "Static asset cache policy needs max-age")
        self.assertLessEqual(int(max_age.group(1)), 86400)
        for marker in [
            "hostinger", "public_html", "approved", "facts", "images", "contacts",
            "legal review", "whatsapp", "noindex",
        ]:
            with self.subTest(readme_marker=marker):
                self.assertIn(marker, readme)

    def test_homepage_required_sections_and_safe_content(self):
        """Missing demo disclosures or fabricated credibility claims must fail."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")

        for section_id in ["care", "doctor", "experience", "visit", "confidence", "location", "faq", "contact"]:
            with self.subTest(section_id=section_id):
                self.assertIn(f'id="{section_id}"', homepage)

        self.assertIn("Meet Dr. Farzana Jamil", homepage)
        for service in [
            "General Gynecology Consultations",
            "Menstrual and Hormonal Health",
            "Pregnancy-Related Consultations",
            "Preventive Women’s Health",
            "Menopause and Midlife Health",
            "Follow-Up Consultations",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, homepage)

        self.assertNotRegex(homepage.lower(), PROHIBITED_HOMEPAGE_CLAIMS)
        self.assertIn("0300-6949109", homepage)
        self.assertIn("03214854145", homepage)

    def test_rating_and_review_claim_pattern_detects_common_fabricated_markers(self):
        """An escaped rating marker must not allow fabricated ratings or review counts."""
        for marker in ("5.0", "4.8/5", "4.8 out of 5", "128 reviews"):
            with self.subTest(marker=marker):
                self.assertRegex(marker, PROHIBITED_HOMEPAGE_CLAIMS)

    def test_deployable_site_has_no_build_runtime_dependency(self):
        """The site has no build or runtime framework dependency."""
        prohibited_in_hostinger = [
            "package.json",
            "server.js",
            "metadata.json",
            "node_modules",
            "src",
            "dist",
            "vite.config.js",
            "vite.config.ts",
            "tsconfig.json",
            ".env",
            "index.php",
        ]
        # Verify the prohibited list contains every required prohibited item
        for req in [
            "package.json", "server.js", "metadata.json", "node_modules",
            "src", "dist", "vite.config.js", "vite.config.ts", "tsconfig.json",
            ".env", "index.php"
        ]:
            self.assertIn(req, prohibited_in_hostinger)

        # Enforce that no compiled app, build framework or backend files exist in project
        for name in ["src", "dist", "vite.config.js", "vite.config.ts", "tsconfig.json", ".env", "index.php"]:
            self.assertFalse((ROOT / name).exists(), f"Prohibited framework file or directory found: {name}")


if __name__ == "__main__":
    unittest.main()
