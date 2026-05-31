import re

with open("static/js/dashboard.js", "r") as f:
    js = f.read()

# Update gradients and colors
js = js.replace('"rgba(34, 211, 238, 0.4)"', '"rgba(96, 81, 158, 0.4)"')
js = js.replace('"rgba(34, 211, 238, 0.0)"', '"rgba(96, 81, 158, 0.0)"')
js = js.replace('"#22d3ee"', '"#60519e"')
js = js.replace('"#12141c"', '"#ffffff"')
js = js.replace('"rgba(255, 255, 255, 0.05)"', '"rgba(0, 0, 0, 0.05)"')
js = js.replace('"#5a6480"', '"#74788d"')

with open("static/js/dashboard.js", "w") as f:
    f.write(js)

print("JS updated.")
