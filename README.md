# Dr. Farzana Jamil Clinic

Dr. Farzana Jamil Clinic is an independent static website demonstration concept created by Bukhari AI for presentation purposes. It is a proposed design for a female gynecologist and women’s health clinic at City Hospital in Pakpattan, Punjab, Pakistan. It does not provide medical advice and is not for emergencies. The project has no patient form, booking flow, analytics, advertising pixels, or external runtime services.

## Project structure

- `index.html` is the main website.
- `assets/css/style.css` contains the complete visual system and responsive styles.
- `assets/js/main.js` contains the navigation, FAQ, demo notice and privacy interactions.
- `assets/images/` and `assets/icons/` contain all local visual assets.
- `privacy-notice.html`, `cookie-policy.html` and `website-terms.html` are the supporting legal pages.
- `tests/site_checks.py` contains the automated static-site checks.
- `docs/` contains the approved design specification and implementation plan.

## Use with GitHub

1. Extract the source ZIP.
2. Create an empty GitHub repository.
3. Upload all extracted files and folders, including `.gitignore` and `.htaccess`, to the repository root.
4. Commit the files to `main`. GitHub is then the source of truth for future edits.

## Use with Google AI Studio

1. Upload the extracted project or the full source ZIP to a new AI Studio workspace/chat that supports project files.
2. Tell AI Studio to inspect `README.md`, the files in `docs/`, and the existing implementation before editing.
3. Keep the current HTML, CSS and JavaScript architecture. This project has no Vite, React, Node.js, PHP or database dependency.
4. Ask AI Studio to change only the named scope, preserve unrelated behavior, and report the files changed plus the checks performed.
5. Download the revised project and commit the verified changes back to GitHub.

## Deploy to Hostinger

1. Keep the root files and `assets/` folder together; their relative paths are the production paths.
2. In Hostinger File Manager, open the target domain’s `public_html` directory.
3. Upload the public HTML files (`index.html`, `privacy-notice.html`, `cookie-policy.html`, `website-terms.html`), `.htaccess`, `robots.txt`, `favicon.svg` and the `assets` directory directly into Hostinger `public_html` (not in an enclosing subfolder).
4. No Node.js runtime, build step or npm command is required.
5. Confirm the domain serves `index.html`, stylesheet, JavaScript, images, legal pages, and the visitor-initiated WhatsApp link without missing assets.
6. Retain the `noindex, nofollow, noarchive, nosnippet` meta tag and `robots.txt` block while this remains a demonstration.

## Client conversion checklist

Before converting this demo into a live clinic site, replace or approve every demo item. Do not publish until the client has supplied and approved:

- Legal business name, public address, opening hours, verified contacts, and any approved external booking destination.
- Verified clinician facts, including approved credentials, registrations, services, emergency guidance, and claims that are permitted for the applicable jurisdiction.
- Approved facts, images, logo, favicon, image rights, reviews, and patient permissions where relevant; remove all AI-generated representative imagery unless it remains clearly disclosed and appropriate.
- The exact data practices: forms, storage, analytics, cookies, advertising pixels, maps, video, fonts, and other third-party services.
- A legal review of the Privacy Notice, Cookie Policy, and Website Terms for the clinic’s jurisdiction and actual data practices.
- A final test of all contacts, WhatsApp, maps, booking links, mobile layout, HTTPS, accessibility, and production indexing settings.

The only live contact in this demo is a visitor-initiated WhatsApp link to Bukhari AI. Replace it only with an approved public destination.

## Checks

```bash
python3 -m unittest tests/site_checks.py -v
node --check assets/js/main.js
git diff --check
```
