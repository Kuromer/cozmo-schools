import re

with open('templates/teacher_portal/attendance.html', 'r', encoding='utf-8') as f:
    content = f.read()

tabs_html = '''<div class="mb-6 flex border-b border-gray-200 gap-4">
    <a href="?tab=take" class="px-6 py-3 font-medium text-sm {% if tab != 'history' %}text-emerald-600 border-b-2 border-emerald-600{% else %}text-gray-500 hover:text-gray-700{% endif %}">Take/Edit Attendance</a>
    <a href="?tab=history" class="px-6 py-3 font-medium text-sm {% if tab == 'history' %}text-emerald-600 border-b-2 border-emerald-600{% else %}text-gray-500 hover:text-gray-700{% endif %}">Attendance History</a>
</div>

{% if tab == 'history' %}
<div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="overflow-x-auto">
        <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                    <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                    <th class="px-6 py-4 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Present</th>
                    <th class="px-6 py-4 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Absent</th>
                    <th class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                {% for item in history_list %}
                <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ item.date|date:"M d, Y" }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ item.class.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-center">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                            {{ item.present }}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-center">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {% if item.absent > 0 %}bg-red-100 text-red-800{% else %}bg-gray-100 text-gray-800{% endif %}">
                            {{ item.absent }}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right">
                        <a href="?tab=take&class_id={{ item.class.id }}&date={{ item.date|date:'Y-m-d' }}" class="text-sm font-medium text-emerald-600 hover:text-emerald-800">
                            Edit/View
                        </a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                        You haven't recorded any attendance yet.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% else %}
'''

if '{% if tab == \'history\' %}' not in content:
    content = content.replace('{% block content %}\n', '{% block content %}\n' + tabs_html)
    
    # We must close the {% endif %} at the very end of the content block
    # Find the last {% endblock %} which closes the content block.
    # The file ends with:
    # {% endblock %} (extra_js)
    # {% endblock %} (content)
    # But wait, extra_js is nested or not?
    # Actually, extra_js is its own block OUTSIDE content block.
    # Let's replace {% block extra_js %} with {% endif %}\n\n{% block extra_js %}
    content = content.replace('{% block extra_js %}', '{% endif %}\n\n{% block extra_js %}')
    
    with open('templates/teacher_portal/attendance.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated attendance.html")
else:
    print("attendance.html already updated")
