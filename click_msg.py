import re

with open('templates/parent_portal/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_msg = '''                    <div class="border-b border-gray-50 pb-3 last:border-0 last:pb-0">
                        <div class="flex justify-between items-start mb-1">
                            <span class="text-sm font-medium text-gray-800 truncate pr-2">{{ msg.subject }}</span>
                            {% if not msg.is_read %}
                            <span class="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 flex-shrink-0"></span>
                            {% endif %}
                        </div>
                        <p class="text-xs text-gray-500 truncate">From: {{ msg.sender.get_full_name|default:msg.sender.username }}</p>
                    </div>'''

new_msg = '''                    <a href="{% url 'parent_portal:message_detail' msg.pk %}" class="block border-b border-gray-50 pb-3 last:border-0 last:pb-0 hover:bg-gray-50 transition-colors p-2 -mx-2 rounded">
                        <div class="flex justify-between items-start mb-1">
                            <span class="text-sm font-medium text-gray-800 truncate pr-2">{{ msg.subject }}</span>
                            {% if not msg.is_read %}
                            <span class="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 flex-shrink-0"></span>
                            {% endif %}
                        </div>
                        <p class="text-xs text-gray-500 truncate">From: {{ msg.sender.get_full_name|default:msg.sender.username }}</p>
                    </a>'''

content = content.replace(old_msg, new_msg)

with open('templates/parent_portal/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated dashboard.html messages to be clickable")
