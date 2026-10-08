with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_cache_fix = '''<script>
        // Force reload if page is loaded from bfcache (e.g. using browser Back button)
        window.addEventListener('pageshow', function(event) {
            if (event.persisted) {
                window.location.reload();
            }
        });
        
        document.addEventListener('DOMContentLoaded', function() {'''

if 'event.persisted' not in content:
    content = content.replace("document.addEventListener('DOMContentLoaded', function() {", js_cache_fix)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated base.html with BFCache fix")
