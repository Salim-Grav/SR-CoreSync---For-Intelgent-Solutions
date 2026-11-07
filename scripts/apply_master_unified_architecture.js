/**
 * Script to inject Sovereign Unified Design System and Master Shell
 * into all studio, portal, and satellite HTML files across the project.
 */

const fs = require('fs');
const path = require('path');

const projectDir = path.resolve(__dirname, '..');
const files = fs.readdirSync(projectDir).filter(f => f.endsWith('.html') && !f.startsWith('preview_') && !f.startsWith('preview-'));

console.log(`Scanning ${files.length} HTML files for sovereign unification...`);

let updatedCount = 0;

files.forEach(file => {
    const filePath = path.join(projectDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let changed = false;

    // 1. Inject CSS in <head> if not present
    if (!content.includes('sr-unified-design-system.css')) {
        // Place right after <head> or before first <link rel="stylesheet"
        if (content.includes('<link rel="stylesheet"')) {
            content = content.replace(
                '<link rel="stylesheet"',
                '<!-- Sovereign Unified Design System (UDS) -->\n    <link rel="stylesheet" href="./css/sr-unified-design-system.css">\n    <link rel="stylesheet"'
            );
            changed = true;
        } else if (content.includes('</head>')) {
            content = content.replace(
                '</head>',
                '    <!-- Sovereign Unified Design System (UDS) -->\n    <link rel="stylesheet" href="./css/sr-unified-design-system.css">\n</head>'
            );
            changed = true;
        }
    }

    // 2. Inject JS before </body> if not present
    if (!content.includes('sr-master-shell.js')) {
        if (content.includes('</body>')) {
            content = content.replace(
                '</body>',
                '    <!-- Sovereign Master Shell Engine (MSE) -->\n    <script src="./js/sr-master-shell.js"></script>\n</body>'
            );
            changed = true;
        }
    }

    if (changed) {
        fs.writeFileSync(filePath, content, 'utf8');
        updatedCount++;
        console.log(`Unified: ${file}`);
    }
});

console.log(`\nUnification complete! Successfully unified ${updatedCount} HTML files.`);
