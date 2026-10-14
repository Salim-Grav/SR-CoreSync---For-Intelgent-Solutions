const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const htmlFiles = [
    'index.html',
    'en/index.html',
    'nl/index.html',
    'demo.html',
    'logo-studio.html',
    'preview-checkout.html',
    'preview-comparison.html',
    'preview-header.html',
    'preview-invoice-quote.html',
    'preview-license-manager.html',
    'preview-roi.html',
    'preview-services.html',
    'preview-software-modal.html',
    'preview-software.html',
    'preview-welcome-email.html',
    'preview-work.html'
];

console.log('============================================================');
console.log('🔬 S&R CoreSync Solutions - Deep Project Diagnostics');
console.log('============================================================\n');

let totalIssues = 0;
const report = [];

function checkFileExists(relPath, baseFile) {
    if (!relPath || relPath.startsWith('http://') || relPath.startsWith('https://') || relPath.startsWith('//') || relPath.startsWith('data:') || relPath.startsWith('blob:') || relPath.startsWith('mailto:') || relPath.startsWith('tel:') || relPath.startsWith('javascript:') || relPath.startsWith('#')) {
        return true;
    }
    // Remove query params or hash
    const cleanPath = relPath.split('?')[0].split('#')[0];
    if (!cleanPath) return true;

    const baseDir = path.dirname(path.join(rootDir, baseFile));
    let targetPath;
    if (cleanPath.startsWith('/')) {
        targetPath = path.join(rootDir, cleanPath);
    } else {
        targetPath = path.resolve(baseDir, cleanPath);
    }

    return fs.existsSync(targetPath);
}

htmlFiles.forEach(file => {
    const fullPath = path.join(rootDir, file);
    if (!fs.existsSync(fullPath)) return;

    const content = fs.readFileSync(fullPath, 'utf8');
    const pageIssues = [];

    // 1. Check Script Syntax
    const scriptRegex = /<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let scriptIdx = 0;
    while ((match = scriptRegex.exec(content)) !== null) {
        scriptIdx++;
        const code = match[1].trim();
        if (!code || match[0].includes('application/ld+json')) continue;
        try {
            new Function(code);
        } catch (err) {
            pageIssues.push(`[JS Syntax Error] In inline script #${scriptIdx}: ${err.message}`);
        }
    }

    // 2. Check Duplicate IDs
    const idRegex = /\bid=["']([^"']+)["']/gi;
    const seenIds = new Set();
    const dupIds = new Set();
    while ((match = idRegex.exec(content)) !== null) {
        const id = match[1];
        if (seenIds.has(id)) {
            dupIds.add(id);
        }
        seenIds.add(id);
    }
    if (dupIds.size > 0) {
        pageIssues.push(`[Duplicate IDs] Found: ${Array.from(dupIds).join(', ')}`);
    }

    // 3. Check Resource References (src, href)
    const srcRegex = /\b(?:src|href)=["']([^"']+)["']/gi;
    const missingResources = [];
    while ((match = srcRegex.exec(content)) !== null) {
        const url = match[1];
        // Skip external or inline
        if (!checkFileExists(url, file)) {
            missingResources.push(url);
        }
    }
    if (missingResources.length > 0) {
        pageIssues.push(`[Missing Resources] (${missingResources.length}): ${missingResources.slice(0, 5).join(', ')}${missingResources.length > 5 ? '...' : ''}`);
    }

    // 4. Check Internal Anchor Targets (#...)
    const anchorRegex = /<a\b[^>]*\bhref=["']#([^"']+)["']/gi;
    const missingAnchors = [];
    while ((match = anchorRegex.exec(content)) !== null) {
        const hashId = match[1];
        if (hashId && !seenIds.has(hashId)) {
            // Check if there is an <a name="...">
            const nameRegex = new RegExp(`\\bname=["']${hashId}["']`, 'i');
            if (!nameRegex.test(content)) {
                missingAnchors.push('#' + hashId);
            }
        }
    }
    if (missingAnchors.length > 0) {
        const uniqueMissing = Array.from(new Set(missingAnchors));
        pageIssues.push(`[Unmatched Anchors] (${uniqueMissing.length}): ${uniqueMissing.join(', ')}`);
    }

    totalIssues += pageIssues.length;
    report.push({
        file,
        status: pageIssues.length === 0 ? '✅ PASS' : `❌ ${pageIssues.length} ISSUES`,
        issues: pageIssues
    });
});

report.forEach(r => {
    console.log(`Page: ${r.file} => ${r.status}`);
    if (r.issues.length > 0) {
        r.issues.forEach(iss => console.log(`   - ${iss}`));
    }
});

console.log('\n------------------------------------------------------------');
console.log(`Total Issues Found: ${totalIssues}`);
console.log('------------------------------------------------------------\n');
