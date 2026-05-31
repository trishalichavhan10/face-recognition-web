import re

with open("static/css/style.css", "r") as f:
    css = f.read()

# Replace camera box
css = re.sub(r'\.camera-box \{[^}]*\}', 
""".camera-box {
    background: #ffffff;
    border: 1px solid #e2e5e8;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03);
}""", css)

# Replace inputs
css = re.sub(r'\.fra-input \{[^}]*\}',
""".fra-input {
    width: 100%;
    background: #ffffff;
    border: 1px solid #e2e5e8;
    color: #495057;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    outline: none;
    transition: border-color 0.2s;
}""", css)

css = re.sub(r'\.fra-input:focus \{[^}]*\}',
""".fra-input:focus {
    border-color: #60519e;
    box-shadow: 0 0 0 3px rgba(96, 81, 158, 0.1);
    color: #333333;
}""", css)

css = re.sub(r'\.fra-input::placeholder \{[^}]*\}',
""".fra-input::placeholder {
    color: #adb5bd;
}""", css)

# Replace profile photo
css = re.sub(r'\.profile-photo \{[^}]*\}',
""".profile-photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid rgba(96, 81, 158, 0.2);
    background: #f4f5f8;
    display: block;
    margin: 0 auto 14px;
}""", css)

# Replace filter tabs
css = re.sub(r'\.filter-tabs \{[^}]*\}',
""".filter-tabs {
    display: inline-flex;
    background: #e2e5e8;
    border-radius: 8px;
    padding: 4px;
    gap: 2px;
    margin-bottom: 16px;
}""", css)

css = re.sub(r'\.filter-tab\.active,\s*\.filter-tab:hover \{[^}]*\}',
""".filter-tab.active,
.filter-tab:hover {
    background: #60519e;
    color: #ffffff;
}""", css)

with open("static/css/style.css", "w") as f:
    f.write(css)

print("CSS minor fixes updated.")
