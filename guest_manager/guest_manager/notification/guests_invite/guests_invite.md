<p>Good day, {{ doc.title }} {{ doc.full_name }},</p><br>
<p>You are being invited as a guest to the residence of {{ doc.resident.title }}
{{ doc.resident.full_name }} at {{ doc.address }}.</p><br>
<p>You are expected to arrive at about {{ doc.expected_arrival_time.strftime("%m/%d/%Y, %H:%M:%S") }}</p>
<i>Please present this email and passcode <em>{{ doc.name }}</em> to the estate security
for proper entry clearance</i>