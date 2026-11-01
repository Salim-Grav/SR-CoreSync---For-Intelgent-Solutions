import io

with io.open('ckb/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add css in head
head_target = '<link rel="stylesheet" href="../css/inline-core.css">'
head_repl = '<link rel="stylesheet" href="../css/inline-core.css">\n    <link rel="stylesheet" href="../css/sr-agent-widget.css?v=20261101">'
if head_target in c:
    c = c.replace(head_target, head_repl, 1)
    print("Added sr-agent-widget.css to ckb/index.html")

# 2. Add script before </body>
script_target = '</body>'
script_repl = '<script src="../js/sr-agent-widget.js" defer></script>\n</body>'
if script_target in c:
    c = c.replace(script_target, script_repl, 1)
    print("Added sr-agent-widget.js to ckb/index.html")

with io.open('ckb/index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)
