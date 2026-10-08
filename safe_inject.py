with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if '<h3 class="text-lg font-semibold' in line:
        # Determine which section we are in
        url = None
        if 'Attendance Overview' in line or (i+2 < len(lines) and 'Attendance Overview' in lines[i+2]): url = 'attendance'
        elif 'Financial Overview' in line or (i+2 < len(lines) and 'Financial Overview' in lines[i+2]): url = 'fees'
        elif 'Active Warnings' in line or (i+2 < len(lines) and 'Active Warnings' in lines[i+2]): url = 'warnings'
        elif 'Recent Homework' in line or (i+2 < len(lines) and 'Recent Homework' in lines[i+2]): url = 'homework'
        elif 'Evaluations' in line or (i+1 < len(lines) and 'Evaluations' in lines[i+1]): url = 'evaluations'
        elif 'Recent Messages' in line or (i+1 < len(lines) and 'Recent Messages' in lines[i+1]): url = 'messages'
        
        if url:
            new_lines.append('            <div class="flex justify-between items-center mb-4">\n')
            # Remove mb-4 from h3
            line = line.replace(' mb-4', '')
            new_lines.append(line)
        else:
            new_lines.append(line)
    elif '</h3>' in line:
        new_lines.append(line)
        # Check if we just opened a view-all div
        # Look backwards to find what section it was
        section = None
        if 'Attendance Overview' in line or (i-1 >= 0 and 'Attendance Overview' in lines[i-1]): section = 'attendance'
        elif 'Financial Overview' in line or (i-1 >= 0 and 'Financial Overview' in lines[i-1]): section = 'fees'
        elif 'Active Warnings' in line or (i-1 >= 0 and 'Active Warnings' in lines[i-1]): section = 'warnings'
        elif 'Recent Homework' in line or (i-1 >= 0 and 'Recent Homework' in lines[i-1]): section = 'homework'
        elif 'Evaluations' in line or (i-1 >= 0 and 'Evaluations' in lines[i-1]): section = 'evaluations'
        elif 'Recent Messages' in line or (i-1 >= 0 and 'Recent Messages' in lines[i-1]): section = 'messages'
        
        if section:
            link = f'                <a href="{{% url \'parent_portal:{section}\' %}}?child_id={{{{ selected_child.id }}}}" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">View all &rarr;</a>\n'
            new_lines.append(link)
            new_lines.append('            </div>\n')
    else:
        new_lines.append(line)

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
