import re

with open("static/css/style.css", "r") as f:
    css = f.read()

def replace_block(css, selector, new_content):
    # Find block starting with selector { ... }
    pattern = re.compile(re.escape(selector) + r'\s*\{[^}]*\}', re.MULTILINE)
    return pattern.sub(selector + " {\n" + new_content + "\n}", css)

# 1. body
css = replace_block(css, "body", """    font-family: 'Inter', sans-serif;
    background: #f4f5f8;
    color: #495057;
    -webkit-font-smoothing: antialiased;""")

# 2. .sidebar
css = replace_block(css, ".sidebar", """    width: 240px;
    min-width: 240px;
    background: #60519e;
    display: flex;
    flex-direction: column;
    padding: 20px 10px 20px 10px;
    border-right: none;""")

# 3. .logo-icon
css = replace_block(css, ".logo-icon", """    width: 34px;
    height: 34px;
    min-width: 34px;
    border-radius: 8px;
    background: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    color: #60519e;""")

# 4. .logo-text
css = replace_block(css, ".logo-text", """    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.5px;
    font-family: 'Inter', sans-serif;
    line-height: 1;""")

# 5. .logo-sub
css = replace_block(css, ".logo-sub", """    font-size: 9px;
    margin-top: 3px;
    color: #e0dced;
    font-weight: 500;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif;""")

# 6. .sidebar nav a
css = replace_block(css, ".sidebar nav a", """    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 14px;
    border-radius: 6px;
    color: #e0dced;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s;
    white-space: nowrap;""")

css = replace_block(css, ".sidebar nav a:hover", """    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;""")

css = replace_block(css, ".sidebar nav a.active", """    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
    border-left: 4px solid #ffffff;
    border-radius: 0 6px 6px 0;""")

css = replace_block(css, ".sidebar nav a.active:hover", """    color: #ffffff;""")

# 7. .main
css = replace_block(css, ".main", """    flex: 1;
    padding: 30px 40px;
    overflow-y: auto;
    background: #f4f5f8;""")

# 8. Headers
css = replace_block(css, ".page-header h1,\n.topbar h1,\n.topbar h2", """    font-size: 24px;
    font-weight: 700;
    color: #333333;
    margin: 0 0 4px 0;
    line-height: 1.2;""")

css = replace_block(css, ".page-sub", """    font-size: 12px;
    color: #74788d;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;""")

# 9. Badges
css = replace_block(css, ".badge-active", """    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #e5f8ed;
    color: #34c38f;
    font-size: 11px;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 12px;""")

css = replace_block(css, ".badge-active::before", """    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #34c38f;
    display: inline-block;""")

css = replace_block(css, ".section-label", """    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #495057;
    margin-bottom: 12px;
    display: block;""")

# 10. Panels
css = replace_block(css, ".panel", """    background: #ffffff;
    border: 1px solid #e2e5e8;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03);""")

css = replace_block(css, ".stat-card", """    background: #ffffff;
    border: 1px solid #e2e5e8;
    border-radius: 8px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03);""")

css = replace_block(css, ".stat-icon", """    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #f4f5f8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    color: #60519e;""")

css = replace_block(css, ".stat-icon.purple", """    background: rgba(96, 81, 158, 0.1);
    color: #60519e;""")
css = replace_block(css, ".stat-icon.green", """    background: rgba(52, 195, 143, 0.1);
    color: #34c38f;""")
css = replace_block(css, ".stat-icon.indigo", """    background: rgba(85, 110, 230, 0.1);
    color: #556ee6;""")

css = replace_block(css, ".stat-num", """    font-size: 24px;
    font-weight: 700;
    color: #333333;
    line-height: 1;""")
css = replace_block(css, ".stat-lbl", """    font-size: 11px;
    color: #74788d;
    text-transform: uppercase;
    margin-top: 4px;""")

# 11. Buttons
css = replace_block(css, ".btn-train", """    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #60519e;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;""")
css = replace_block(css, ".btn-train:hover", """    background: #52448a;
    color: #ffffff;""")

css = replace_block(css, ".btn-cyan", """    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #60519e;
    color: #ffffff;
    border: none;
    padding: 9px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;""")
css = replace_block(css, ".btn-cyan:hover", """    background: #52448a;
    color: #ffffff;
    transform: translateY(-1px);""")

css = replace_block(css, ".btn-purple", """    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #60519e;
    color: #ffffff;
    border: none;
    padding: 10px 22px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;""")
css = replace_block(css, ".btn-purple:hover", """    background: #52448a;
    color: #ffffff;""")

css = replace_block(css, ".badge-match", """    background: #e5f8ed;
    color: #34c38f;
    font-size: 10px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 12px;
    border: none;""")

# 12. Tables
css = replace_block(css, ".fra-table th", """    text-align: left;
    padding: 12px 14px;
    font-size: 11px;
    color: #74788d;
    border-bottom: 1px solid #e2e5e8;""")

css = replace_block(css, ".fra-table td", """    padding: 14px 14px;
    font-size: 13px;
    background: #ffffff;
    border-bottom: 1px solid #eff2f7;
    color: #495057;""")

css = replace_block(css, ".fra-table tr:hover td", """    background: #f8f9fa;""")

css = replace_block(css, ".activity-row", """    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px 16px;
    border-radius: 8px;
    background: #ffffff;
    border: 1px solid #e2e5e8;
    margin-bottom: 8px;
    transition: background 0.2s;""")
css = replace_block(css, ".activity-row:hover", """    background: #f8f9fa;""")
css = replace_block(css, ".activity-avatar", """    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(96, 81, 158, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #60519e;
    font-weight: 600;
    flex-shrink: 0;""")

css = replace_block(css, ".chart-panel", """    background: #ffffff;
    border: 1px solid #e2e5e8;
    border-radius: 12px;
    padding: 20px;
    margin-top: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03);""")

with open("static/css/style.css", "w") as f:
    f.write(css)

print("CSS updated.")
