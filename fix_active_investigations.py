import re

with open('meta/active_investigations.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Answer for Q3 (Brand Name) again (since the previous script didn't apply properly)
q3_pattern = r'(Τίτλος Έρευνας: \s*Ποιο θα είναι το όνομα του startup μας;\nΓιατί είναι κρίσιμη:.*?\nAI Prompt:.*?\nΑπάντηση / Δεδομένα: )→'
q3_replacement = r'\1Ο χρήστης δεν θυμάται ακριβώς, αλλά έχει σημειώσει προηγουμένως ιδέες (TapServe, EasyTab, QResto, Breeze, Velo, Kima, Lio, Zeno). Χρειάζεται τελική επιλογή (π.χ. με ψηφοφορία στην ομάδα).'
content = re.sub(q3_pattern, q3_replacement, content, flags=re.DOTALL)

# Remove Q2 (Analytics)
q2_pattern = r'\*\*Τίτλος Έρευνας: \*\* Τι data tracking/analytics setup \(π.χ. PostHog vs Mixpanel\).*?\nΑπάντηση / Δεδομένα: →\n\n'
content = re.sub(q2_pattern, '', content, flags=re.DOTALL)

# Remove Q5 (Sales Strategy)
q5_pattern = r'\*\*Τίτλος Έρευνας: \*\* Πώς ακριβώς θα προσεγγίσουμε τους πρώτους 10 πελάτες;.*?\nΑπάντηση / Δεδομένα: →\n\n'
content = re.sub(q5_pattern, '', content, flags=re.DOTALL)

with open('meta/active_investigations.md', 'w', encoding='utf-8') as f:
    f.write(content)
