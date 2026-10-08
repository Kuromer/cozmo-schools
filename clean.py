with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i in range(len(lines)):
    if '            <div class="flex justify-between items-center mb-4">\n' in lines[i] and '                <div class="flex justify-between items-center mb-4">\n' in lines[i-1]:
        continue
    new_lines.append(lines[i])

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
