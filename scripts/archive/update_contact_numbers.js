/**
 * Updates official contact numbers for Salim and Raed across all pages and configs
 * Salim: +31 6 1811 1116 (31618111116)
 * Raed:  +31 6 8771 0290 (31687710290)
 */

const fs = require('fs');
const path = require('path');

const SALIM_RAW = '31618111116';
const SALIM_FMT = '+31 6 1811 1116';
const RAED_RAW  = '31687710290';
const RAED_FMT  = '+31 6 8771 0290';

// Files to update
const targetFiles = [
  'index.html',
  'nl/index.html',
  'en/index.html',
  'preview-header.html',
  'preview-services.html',
  'preview-roi.html',
  'software.html',
  'manifest.json',
  'api/email-notification-service.js'
];

let totalChanges = 0;

for (const relPath of targetFiles) {
  const filePath = path.resolve(__dirname, '..', relPath);
  if (!fs.existsSync(filePath)) {
    console.log(`Skipping non-existent file: ${relPath}`);
    continue;
  }

  let content = fs.readFileSync(filePath, 'utf8');
  let original = content;

  // 1. In index.html specifically: update founder cinema cards
  if (relPath === 'index.html') {
    // Salim contact
    content = content.replace(
      /contactUrl:\s*'https:\/\/wa\.me\/(?:31687764998|31612345678)\?text='\s*\+\s*encodeURIComponent\('مرحباً م\. سليم/g,
      `contactUrl: 'https://wa.me/${SALIM_RAW}?text=' + encodeURIComponent('مرحباً م. سليم`
    );
    // Raed contact
    content = content.replace(
      /contactUrl:\s*'https:\/\/wa\.me\/(?:31687764998|31612345678)\?text='\s*\+\s*encodeURIComponent\('مرحباً أ\. رائد/g,
      `contactUrl: 'https://wa.me/${RAED_RAW}?text=' + encodeURIComponent('مرحباً أ. رائد`
    );
  }

  // 2. Replace generic dummy numbers: 31612345678 -> Salim
  content = content.replace(/31612345678/g, SALIM_RAW);
  content = content.replace(/\+31 6 1234 5678/g, SALIM_FMT);
  content = content.replace(/\+31612345678/g, `+${SALIM_RAW}`);

  // 3. Replace old temp number 31687764998 -> Salim (except if specifically Raed)
  content = content.replace(/31687764998/g, SALIM_RAW);
  content = content.replace(/\+31 6 87764998/g, SALIM_FMT);
  content = content.replace(/\+31687764998/g, `+${SALIM_RAW}`);

  // 4. Replace old domain email info@coresync-solutions.com -> info@sr-coresync.com
  content = content.replace(/info@coresync-solutions\.com/g, 'info@sr-coresync.com');

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Updated numbers in: ${relPath}`);
    totalChanges++;
  } else {
    console.log(`ℹ️ No changes needed in: ${relPath}`);
  }
}

console.log(`\n🎉 Total files updated: ${totalChanges}`);
