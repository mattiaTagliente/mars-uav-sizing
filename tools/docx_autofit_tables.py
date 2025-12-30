import sys, zipfile, tempfile, shutil, os
from xml.etree import ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
def qn(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"

def ensure_child(parent, tag):
    child = parent.find(tag)
    if child is None:
        child = ET.Element(tag)
        parent.insert(0, child)
    return child

def patch_xml(path: str) -> bool:
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return False

    root = tree.getroot()
    changed = False

    for tbl in root.iter(qn("tbl")):
        tblPr = tbl.find(qn("tblPr"))
        if tblPr is None:
            tblPr = ET.Element(qn("tblPr"))
            tbl.insert(0, tblPr)
            changed = True

        # Force AutoFit table layout
        tblLayout = tblPr.find(qn("tblLayout"))
        if tblLayout is None:
            tblLayout = ET.Element(qn("tblLayout"))
            tblPr.append(tblLayout)
            changed = True
        if tblLayout.get(qn("type")) != "autofit":
            tblLayout.set(qn("type"), "autofit")
            changed = True

        # Preferred table width = auto
        tblW = tblPr.find(qn("tblW"))
        if tblW is None:
            tblW = ET.Element(qn("tblW"))
            tblPr.append(tblW)
            changed = True
        if tblW.get(qn("type")) != "auto" or tblW.get(qn("w")) != "0":
            tblW.set(qn("type"), "auto")
            tblW.set(qn("w"), "0")
            changed = True

        # Center the table (effective when table width < page width)
        jc = tblPr.find(qn("jc"))
        if jc is None:
            jc = ET.Element(qn("jc"))
            tblPr.append(jc)
            changed = True
        if jc.get(qn("val")) != "center":
            jc.set(qn("val"), "center")
            changed = True

        # Remove fixed cell widths by switching tcW to auto/0
        for tc in tbl.iter(qn("tc")):
            tcPr = tc.find(qn("tcPr"))
            if tcPr is None:
                tcPr = ET.Element(qn("tcPr"))
                tc.insert(0, tcPr)
                changed = True
            tcW = tcPr.find(qn("tcW"))
            if tcW is None:
                tcW = ET.Element(qn("tcW"))
                tcPr.append(tcW)
                changed = True
            if tcW.get(qn("type")) != "auto" or tcW.get(qn("w")) != "0":
                tcW.set(qn("type"), "auto")
                tcW.set(qn("w"), "0")
                changed = True

    if changed:
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return changed

def main(inp: str, outp: str):
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(inp, "r") as z:
            z.extractall(td)

        word_dir = os.path.join(td, "word")
        if os.path.isdir(word_dir):
            for fn in os.listdir(word_dir):
                if fn.lower().endswith(".xml"):
                    patch_xml(os.path.join(word_dir, fn))

        # Repack
        with zipfile.ZipFile(outp, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(td):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, td)
                    z.write(full, rel)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python tools/docx_autofit_tables.py input.docx output.docx")
    main(sys.argv[1], sys.argv[2])
