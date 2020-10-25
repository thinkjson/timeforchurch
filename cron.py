import os
import re
from datetime import datetime
import requests
import csv

script_dir = os.path.dirname(__file__)
output_file = os.path.join(script_dir, "_includes/data.html")

# Grab latest FDOH guidance
doh = requests.get("https://floridahealthcovid19.gov/prevention/").text
masks_doh = "Cover your mouth and nose" in doh

# Grab R0 data
r0 = requests.get("https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv").text
masks_r0 = 0.0
r0_last_updated = ""
for line in r0.split("\n"):
    row = line.split(",")
    if len(row) > 3 and row[1] == "FL" and row[0] > r0_last_updated:
        r0_last_updated = row[0]
        masks_r0 = float(row[3])

# Determine mask guidance
masks = masks_doh or masks_r0 > 1.0

# Grab Volusia scorecard
scorecard = requests.get(
    "https://thefloridascorecard.org/pillar&c=64&pillar=0").text
positivity = 0.0
try:
    positivity = float(re.search(
        'data-target="#covid-percent-positiveModal">([0-9.]+)%</a>', scorecard).group(1))
except:
    pass
positivity_nominal = positivity > 0.0 and positivity < 3.0

# Determine safe to return
safe = masks_r0 < 1.0

data = """
    <h1>Is it safe to return to church?</h1>
    <div class="outcome {safe_class}">{is_safe}</div>
    {positivity}
    {r0}

    <p>NOTE: Guidance from the Florida Department of Health no longer includes language about avoiding crowds.</p>

    <h1>Do I need to wear a mask?</h1>
    <div class="outcome {mask_class}">{mask}</div>
    {mask_info}

    <p>Last updated {updated}</p>
""".format(
    safe_class="text-warning" if safe else "text-danger",
    is_safe="NO" if not safe else "MAYBE",
    positivity="""<div class="alert alert-danger" role="alert">Positivity rate of {0}% is above the 5.0% threshold for reopening announced in April 2020</div>""".format(
        positivity) if not positivity_nominal else "",
    mask="YES" if masks else "UNKNOWN",
    mask_class="text-success" if masks else "text-warning",
    r0="""<div class="alert alert-danger" role="alert">R0 is greater than 1.0 in the state of Florida</div>""" if masks_r0 > 1.0 else "",
    mask_info="<p>Check the <a href='https://floridahealthcovid19.gov/prevention/'>Florida Department of Health's COVID-19 response</a> for more information" if not masks_doh else """<div class="alert alert-info" role="alert">The Florida Department of Health recommends wearing a face covering when in public</div>""",
    updated=datetime.now().strftime("%A, %B %d at %H:%M %p"),
)

with open(output_file, "w") as f:
    f.write(data)
