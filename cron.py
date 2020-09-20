import os
import re
from datetime import datetime
import requests

script_dir = os.path.dirname(__file__)
output_file = os.path.join(script_dir, "_includes/data.html")

doh = requests.get("https://floridahealthcovid19.gov/").text
gatherings = "Refrain from gatherings of more than 10 people" not in doh
crowds = "Avoid crowds" not in doh
masks = "Residents are advised to wear face coverings" in doh

scorecard = requests.get("https://thefloridascorecard.org/pillar&c=64&pillar=0").text
positivity = 0.0
try:
    positivity = float(re.search('data-target="#covid-percent-positiveModal">([0-9.]+)%</a>', scorecard).group(1))
except:
    pass
positivity_nominal = positivity > 0.0 and positivity < 3.0

safe = gatherings and crowds

data = """
    <h1>Is it safe to return to church?</h1>
    <div class="outcome {safe_class}">{is_safe}</div>
    {gatherings}
    {crowds}
    {positivity}

    <h1>Do I need to wear a mask?</h1>
    <div class="outcome {mask_class}">{mask}</div>
    {mask_info}

    <p>Last updated {updated}</p>
""".format(
    safe_class="text-warning" if safe else "text-danger",
    is_safe="NO" if not safe else "MAYBE",
    gatherings="""<div class="alert alert-warning" role="alert">The Florida Department of Health recommends refraining from gatherings of more than 10 people</div>""" if not gatherings else "",
    positivity="""<div class="alert alert-warning" role="alert">Positivity rate of {0}%% is too high</div>""".format(positivity) if not positivity_nominal else "",
    crowds="""<div class="alert alert-warning" role="alert">The Florida Department of Health recommends avoiding crowds</div>""" if not crowds else "",
    mask="YES" if masks else "UNKNOWN",
    mask_class="text-danger" if masks else "text-warning",
    mask_info="<p>Check the <a href='https://floridahealthcovid19.gov/'>Florida Department of Health's COVID-19 response</a> for more information" if not masks else "",
    updated=datetime.now().strftime("%A, %B %d at %H:%M %p"),
)

with open(output_file, "w") as f:
    f.write(data)
