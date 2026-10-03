#!/usr/bin/env python3
"""Generate the Girih icon theme (run from anywhere; writes next to this file).

scalable/  64-unit SVGs for file views: Emerald tab folders with a Brass edge,
           Ivory outline documents with a 45° cut corner, chamfered devices.
16/        sidebar size: the theme's small diamonds (places outlined Brass,
           devices Emerald-filled, network Lapis).
Anything not drawn here falls through to Adwaita.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

EMERALD, EMERALD_LIT = "#0F6B4F", "#15845F"
BRASS, GOLD, IVORY = "#C9A24A", "#E6C36A", "#F2EAD8"
SLATE, LAPIS, RED = "#1A2233", "#3F74D0", "#C0503F"


def svg(size, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}">{body}</svg>\n')


def write(rel, content, names):
    for name in names:
        path = ROOT / rel / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


# ---- glyphs (drawn inside a ~20-unit box centred on 32,39) ----------------

G = f'fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linejoin="miter" stroke-linecap="square"'
GLYPHS = {
    "star": f'<rect x="26" y="33" width="12" height="12" {G}/>'
            f'<rect x="26" y="33" width="12" height="12" transform="rotate(45 32 39)" {G}/>',
    "lines": f'<path d="M23 33H41M23 39H41M23 45H35" {G}/>',
    "down": f'<path d="M25 34L32 41L39 34M24 47H40" {G}/>',
    "note": f'<path d="M36 30V44M36 30L42 33" {G}/><rect x="28" y="41" width="6" height="6" transform="rotate(45 31 44)" fill="{GOLD}"/>',
    "picture": f'<path d="M22 47L29 37L34 43L37 40L42 47Z" {G}/><rect x="36" y="29" width="4" height="4" transform="rotate(45 38 31)" fill="{GOLD}"/>',
    "play": f'<path d="M27 31L40 39L27 47Z" {G}/>',
    "dashed": f'<rect x="24" y="31" width="16" height="16" {G} stroke-dasharray="3 3"/>',
    "share": f'<path d="M25 44L32 33L39 44Z" {G}/>',
    "desktop": f'<path d="M22 31H42V43H22ZM28 48H36M32 43V48" {G}/>',
    "remote": f'<circle cx="32" cy="39" r="8" {G}/><path d="M24 39H40M32 31C28 35 28 43 32 47C36 43 36 35 32 31" {G}/>',
    "prompt": f'<path d="M24 33L30 39L24 45M33 46H41" {G}/>',
    "gem": f'<rect x="27" y="34" width="10" height="10" transform="rotate(45 32 39)" fill="{GOLD}"/>'
           f'<rect x="24" y="31" width="16" height="16" transform="rotate(45 32 39)" {G}/>',
    "bars": f'<path d="M24 45V39M29 45V33M34 45V36M39 45V41" {G}/>',
    "zip": f'<path d="M32 26V30M29 30H35M32 33V35M29 36H35M32 39V41M28 44H36V50H28Z" {G}/>',
    "pdf": f'<rect x="21" y="36" width="22" height="9" fill="{RED}"/><path d="M21 49H43" {G}/>',
    "code": f'<path d="M27 32L21 39L27 46M37 32L43 39L37 46" {G}/>',
    "grid": f'<path d="M22 32H42V46H22ZM22 39H42M29 32V46M36 32V46" {G}/>',
    "slide": f'<path d="M22 32H42V44H22ZM32 44V49" {G}/>',
    "font": f'<path d="M24 47L32 30L40 47M27 41H37" {G}/>',
}

# ---- folders ------------------------------------------------------------------

FOLDER_BASE = (
    f'<path d="M6 15H26L31 21H58V50L54 54H10L6 50Z" fill="{EMERALD}" stroke="{BRASS}" stroke-width="2" stroke-linejoin="miter"/>'
    f'<path d="M7 27H57" stroke="{BRASS}" stroke-opacity="0.45" stroke-width="1.5"/>'
    f'<path d="M7 28H57V50L54 53H10L7 50Z" fill="{EMERALD_LIT}" fill-opacity="0.35"/>'
)

FOLDERS = {
    None: ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
    "star": ["user-home", "folder-home"],
    "lines": ["folder-documents"],
    "down": ["folder-download"],
    "note": ["folder-music"],
    "picture": ["folder-pictures"],
    "play": ["folder-videos"],
    "dashed": ["folder-templates"],
    "share": ["folder-publicshare"],
    "desktop": ["user-desktop"],
    "remote": ["folder-remote", "network-workgroup"],
}

for glyph, names in FOLDERS.items():
    body = FOLDER_BASE + (GLYPHS[glyph] if glyph else "")
    ctx = "mimetypes" if names[0] == "folder" else "places"
    write(f"scalable/{ctx}", svg(64, body), names)
    if glyph is None:
        write("scalable/places", svg(64, body), names)

# ---- documents ------------------------------------------------------------

def document(glyph, accent=IVORY):
    return svg(64,
        f'<path d="M14 6H40L50 16V58H14Z" fill="{IVORY}" fill-opacity="0.05" stroke="{accent}" '
        f'stroke-opacity="0.8" stroke-width="2" stroke-linejoin="miter"/>'
        f'<path d="M40 6V16H50" fill="none" stroke="{accent}" stroke-opacity="0.8" stroke-width="2"/>'
        + (GLYPHS[glyph].replace(GOLD, BRASS) if glyph else ""))

DOCUMENTS = {
    None: ["application-x-generic", "unknown", "empty"],
    "lines": ["text-x-generic", "text-plain", "x-office-document", "text-markdown", "text-x-readme"],
    "prompt": ["text-x-script", "application-x-shellscript", "text-x-python", "text-x-makefile"],
    "gem": ["application-x-executable", "application-x-sharedlib"],
    "picture": ["image-x-generic"],
    "bars": ["audio-x-generic"],
    "play": ["video-x-generic"],
    "zip": ["package-x-generic", "application-x-archive", "application-zip",
            "application-x-compressed-tar", "application-x-tar"],
    "pdf": ["application-pdf"],
    "code": ["text-html", "application-json", "text-x-csrc", "text-x-c++src", "text-x-javascript"],
    "grid": ["x-office-spreadsheet"],
    "slide": ["x-office-presentation"],
    "font": ["font-x-generic"],
}

for glyph, names in DOCUMENTS.items():
    write("scalable/mimetypes", document(glyph), names)

# ---- devices, trash --------------------------------------------------------

def device(inner):
    return svg(64,
        f'<path d="M12 18H52L56 22V42L52 46H12L8 42V22Z" fill="{SLATE}" stroke="{BRASS}" stroke-width="2"/>'
        + inner)

LED = f'<rect x="44" y="35" width="5" height="5" transform="rotate(45 46.5 37.5)" fill="{GOLD}"/>'
write("scalable/devices", device(f'<path d="M15 32H36" stroke="{BRASS}" stroke-opacity="0.5" stroke-width="2"/>{LED}'),
      ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"])
write("scalable/devices", svg(64,
    f'<path d="M22 8H42V20H22Z" fill="none" stroke="{BRASS}" stroke-width="2"/>'
    f'<path d="M18 20H46V52L42 56H22L18 52Z" fill="{SLATE}" stroke="{BRASS}" stroke-width="2"/>'
    f'<rect x="28" y="34" width="8" height="8" transform="rotate(45 32 38)" fill="{GOLD}"/>'),
      ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"])
write("scalable/devices", svg(64,
    f'<circle cx="32" cy="32" r="22" fill="{SLATE}" stroke="{BRASS}" stroke-width="2"/>'
    f'<circle cx="32" cy="32" r="5" fill="none" stroke="{GOLD}" stroke-width="2"/>'),
      ["drive-optical", "media-optical"])
write("scalable/devices", svg(64,
    f'<path d="M10 10H54V42H10Z" fill="{SLATE}" stroke="{BRASS}" stroke-width="2"/>'
    f'<path d="M24 54H40M32 42V54" stroke="{BRASS}" stroke-width="2"/>'
    f'<rect x="27" y="21" width="10" height="10" transform="rotate(45 32 26)" fill="{EMERALD}" stroke="{GOLD}" stroke-width="1.5"/>'),
      ["computer", "video-display"])

TRASH = (f'<path d="M14 18H50M26 18V12H38V18" fill="none" stroke="{BRASS}" stroke-width="2"/>'
         f'<path d="M17 22H47L44 56H20Z" fill="{SLATE}" stroke="{BRASS}" stroke-width="2"/>')
write("scalable/places", svg(64, TRASH + f'<path d="M27 30V48M37 30V48" stroke="{BRASS}" stroke-opacity="0.45" stroke-width="2"/>'),
      ["user-trash"])
write("scalable/places", svg(64, TRASH + f'<rect x="27" y="33" width="10" height="10" transform="rotate(45 32 38)" fill="{GOLD}"/>'),
      ["user-trash-full"])

# ---- 16px sidebar diamonds ---------------------------------------------------

def diamond(stroke, fill="none"):
    return svg(16, f'<rect x="4.5" y="4.5" width="7" height="7" transform="rotate(45 8 8)" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')

write("16/places", diamond(BRASS), sum(FOLDERS.values(), []) + [
    "user-trash", "user-trash-full", "go-home", "document-open-recent", "folder-recent",
    "user-bookmarks", "bookmark-new"])
write("16/places", diamond(LAPIS), ["folder-remote", "network-workgroup", "network-server"])
write("16/devices", diamond(BRASS, EMERALD),
      ["drive-harddisk", "drive-harddisk-system", "drive-multidisk", "drive-removable-media",
       "drive-harddisk-usb", "media-removable", "media-flash", "drive-optical", "media-optical",
       "computer", "video-display"])

(ROOT / "index.theme").write_text("""[Icon Theme]
Name=Girih
Comment=Emerald tab folders, Ivory documents, Brass diamonds
Inherits=Adwaita,hicolor
Example=folder

Directories=16/places,16/devices,scalable/places,scalable/mimetypes,scalable/devices

[16/places]
Size=16
Context=Places
Type=Fixed

[16/devices]
Size=16
Context=Devices
Type=Fixed

[scalable/places]
Size=64
MinSize=20
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[scalable/devices]
Size=64
MinSize=20
MaxSize=512
Context=Devices
Type=Scalable
""")
import subprocess
subprocess.run(["gtk-update-icon-cache", "-f", "-t", str(ROOT)], check=False)
print("Girih icons written to", ROOT)
