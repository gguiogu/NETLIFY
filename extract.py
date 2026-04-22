import sys

with open(r'C:\Users\mlkml\.gemini\antigravity\brain\cef681a8-7f78-4475-acdb-5984b185ec36\.system_generated\logs\overview.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start_str = '<!DOCTYPE html>'
start_idx = text.find(start_str)

if start_idx != -1:
    end_str = '<div class="rvf'
    end_idx = text.find(end_str, start_idx) + len(end_str)
    
    html_content = text[start_idx:end_idx]
    
    with open(r'e:\KOUKI SHOP\new_theme_base.html', 'w', encoding='utf-8') as out:
        out.write(html_content)
    print(f'Wrote {len(html_content)} bytes to new_theme_base.html')
else:
    print('Failed to find start string')
