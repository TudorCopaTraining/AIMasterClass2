import os
import shutil
import zipfile

print("Building 6-module MC2 sequential SCORM package...")

modules = [
    {
        "html": "Processimprovement.html",
        "css": "ProcessImprovement.css",
        "title": "1. Process Improvement",
    },
    {
        "html": "process_map_builder.html",
        "css": "ProcessMapping.css",
        "title": "2. Process Map Builder",
    },
    {
        "html": "Processwaste.html",
        "css": "ProcessImprovement.css",
        "title": "3. Process Waste",
    },
    {
        "html": "fivewhys.html",
        "css": "ProcessImprovement.css",
        "title": "4. Five Whys Analysis",
    },
    {
        "html": "automation.html",
        "css": "ProcessImprovement.css",
        "title": "5. Automation Activity",
    },
    {
        "html": "improvementopp.html",
        "css": "ProcessImprovement.css",
        "title": "6. Improvement Opportunities",
    },
]

output_zip = "MC2_Complete_SCORM.zip"
temp_dir = "temp_mc2_build"

if os.path.exists(temp_dir):
  shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# Build manifest dynamically for all 6 items
items_xml = ""
resources_xml = ""

for i, mod in enumerate(modules, start=1):
  items_xml += f"""
      <item identifier="item_{i}" identifierref="res_{i}">
        <title>{mod['title']}</title>
      </item>"""

  css_file_tag = (
      f'<file href="{mod["css"]}"/>'
      if mod.get("css") and os.path.exists(mod["css"])
      else ""
  )
  resources_xml += f"""
    <resource identifier="res_{i}" type="webcontent" adlcp:scormtype="sco" href="{mod['html']}">
      <file href="{mod['html']}"/>
      {css_file_tag}
    </resource>"""

manifest_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.mc2.masterclass" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1 imscp_rootv1p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlnet_rootv1p2.xsd">
  <organizations default="mc2_org">
    <organization identifier="mc2_org">
      <title>MC2 Masterclass Complete Sequence</title>
      {items_xml}
    </organization>
  </organizations>
  <resources>
    {resources_xml}
  </resources>
</manifest>
"""

# Copy files into temp dir
for mod in modules:
  html_file = mod["html"]
  css_file = mod.get("css")

  if os.path.exists(html_file):
    shutil.copy(html_file, os.path.join(temp_dir, html_file))
    print(f"[OK] Added HTML: {html_file}")
  else:
    print(f"[WARNING] Missing HTML file: {html_file}")

  if css_file and os.path.exists(css_file):
    shutil.copy(css_file, os.path.join(temp_dir, css_file))
    print(f"[OK] Added CSS: {css_file}")

# Write manifest directly into temp dir root
with open(os.path.join(temp_dir, "imsmanifest.xml"), "w") as f:
  f.write(manifest_template)
print("[OK] Generated master imsmanifest.xml")

# Zip contents directly flat (no nested wrapper folder)
with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
  for filename in os.listdir(temp_dir):
    file_path = os.path.join(temp_dir, filename)
    if os.path.isfile(file_path):
      zipf.write(file_path, arcname=filename)

shutil.rmtree(temp_dir)
print(f"\nSuccessfully created clean single package: {output_zip}")
