import requests
import os

script_dir = os.path.dirname(__file__)
output_file = os.path.join(script_dir, "_includes/data.html")

doh = requests.get("https://floridahealthcovid19.gov/").text
gatherings = "Refrain from gatherings of more than 10 people" not in doh
crowds = "Avoid crowds" not in doh
masks = "Residents are advised to wear face coverings" in doh

safe = gatherings and crowds

data = """
    <h1>Is it safe to return to church?</h1>
    <div class="outcome {safe}">{is_safe}</div>
    <ul>
        <li>{gatherings}</li>
        <li>{crowds}</li>
    </ul>

    <h1>Do I need to wear a mask?</h1>
    <div class="outcome">{mask}</a>
    {mask_info}
""".format(
    safe="text-warning" if safe else "text-danger",
    is_safe="NO" if not safe else "MAYBE",
    gatherings="The Florida Department of Health recommends refraining from gatherings of more than 10 people" if not gatherings else "",
    crowds="The Florida Department of Health recommends avoiding crowds" if not crowds else "",
    mask="YES" if masks else "UNKNOWN",
    mask_info="<p>Check the <a href='https://floridahealthcovid19.gov/'>Florida Department of Health's COVID-19 response</a> for more information" if not masks else "",
)

with open(output_file, "w") as f:
    f.write(data)