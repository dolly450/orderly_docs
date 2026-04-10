with open("meta/knowledge-health.md", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.startswith("### 2026-04-11") and i == 44:
        new_lines.append("### 2026-04-10\n")
    else:
        new_lines.append(line)

with open("meta/knowledge-health.md", "w") as f:
    f.writelines(new_lines)
