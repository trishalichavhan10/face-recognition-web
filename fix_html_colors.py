import os
import glob

html_files = glob.glob("templates/*.html")
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Replace light text colors with darker ones suitable for light theme
    content = content.replace('#c8d0e0', '#333333')
    content = content.replace('#3a4060', '#74788d')
    content = content.replace('#4a5270', '#74788d')
    
    with open(f, 'w') as file:
        file.write(content)

print("HTML hardcoded colors updated.")
