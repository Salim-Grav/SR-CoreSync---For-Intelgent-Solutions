/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

const fs = require('fs');

const files = ['index.html', 'en/index.html', 'nl/index.html'].filter(f => fs.existsSync(f));
let hasError = false;

console.log('Starting S&R CoreSync automated quality assurance...');

files.forEach(file => {
    const content = fs.readFileSync(file, 'utf8');
    const styles = content.match(/<style[^>]*>([\s\S]*?)<\/style>/gi) || [];
    styles.forEach((style, idx) => {
        const openB = (style.match(/\{/g) || []).length;
        const closeB = (style.match(/\}/g) || []).length;
        if (openB !== closeB) {
            console.error('[ERROR] In ' + file + ' style #' + (idx + 1) + ': ' + openB + ' open "{" vs ' + closeB + ' close "}"');
            hasError = true;
        }
    });

    const scripts = content.match(/<script[^>]*>([\s\S]*?)<\/script>/gi) || [];
    scripts.forEach((script, idx) => {
        const openB = (script.match(/\{/g) || []).length;
        const closeB = (script.match(/\}/g) || []).length;
        if (openB !== closeB) {
            console.error('[ERROR] In ' + file + ' script #' + (idx + 1) + ': ' + openB + ' open "{" vs ' + closeB + ' close "}"');
            hasError = true;
        }
    });
});

if (hasError) {
    console.error('Validation FAILED.');
    process.exit(1);
} else {
    console.log('Validation PASSED: All HTML, CSS, and JS blocks are balanced and error-free.');
    process.exit(0);
}
