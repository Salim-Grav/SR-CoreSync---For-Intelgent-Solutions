/**
 * S&R CoreSync Solutions - Enterprise Production Packager
 * Compiles minified bundles, filters production assets, and generates
 * a clean deployment ZIP package ready for live server deployment.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('============================================================');
console.log('📦 S&R CoreSync Solutions - Generating Deployment Package...');
console.log('============================================================');

// Step 1: Ensure latest minified bundles are built
console.log('⚡ Step 1/3: Compiling latest production minified assets...');
execSync('node scripts/build_production.js', { stdio: 'inherit' });

// Step 2: Prepare clean staging directory
const distDir = path.resolve(__dirname, '../dist');
const stagingDir = path.resolve(distDir, 'staging');
const outputZip = path.resolve(distDir, 'SR-CoreSync-Solutions-Production-v2.0.zip');

if (fs.existsSync(stagingDir)) {
  fs.rmSync(stagingDir, { recursive: true, force: true });
}
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}
fs.mkdirSync(stagingDir, { recursive: true });

console.log('📁 Step 2/3: Gathering verified production assets...');

// Production Files
const rootFiles = [
  'index.html',
  'demo.html',
  'preview-software.html',
  'preview-checkout.html',
  'preview-license-manager.html',
  'preview-roi.html',
  'preview-services.html',
  'preview-header.html',
  'preview-comparison.html',
  'preview-software-modal.html',
  'logo-studio.html',
  'manifest.json',
  'sw.js',
  'sitemap.xml',
  'robots.txt'
];

rootFiles.forEach(file => {
  const src = path.resolve(__dirname, '..', file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(stagingDir, file));
  }
});

// Production Directories
const prodDirs = ['assets', 'css', 'js', 'downloads', 'en', 'nl'];

function copyDirRecursive(srcDir, destDir) {
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

prodDirs.forEach(dir => {
  const src = path.resolve(__dirname, '..', dir);
  if (fs.existsSync(src)) {
    copyDirRecursive(src, path.join(stagingDir, dir));
  }
});

// Calculate total uncompressed size and count
let totalFiles = 0;
let totalBytes = 0;

function auditStaging(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      auditStaging(p);
    } else {
      totalFiles++;
      totalBytes += fs.statSync(p).size;
    }
  }
}
auditStaging(stagingDir);

console.log(`📊 Staged ${totalFiles} clean files (${(totalBytes / (1024 * 1024)).toFixed(2)} MB uncompressed).`);

// Step 3: Create ZIP Archive using PowerShell Compress-Archive
console.log('🗜️ Step 3/3: Creating high-compression deployment ZIP archive...');
if (fs.existsSync(outputZip)) {
  fs.unlinkSync(outputZip);
}

const psCommand = `powershell -NoProfile -Command "Compress-Archive -Path '${stagingDir}\\*' -DestinationPath '${outputZip}' -CompressionLevel Optimal -Force"`;
execSync(psCommand, { stdio: 'inherit' });

// Cleanup staging
fs.rmSync(stagingDir, { recursive: true, force: true });

const zipSize = fs.statSync(outputZip).size;

console.log('============================================================');
console.log('🎉 DEPLOYMENT PACKAGE READY FOR PRODUCTION HOSTING!');
console.log(`📦 Package File: ${outputZip}`);
console.log(`💾 Final Package Size: ${(zipSize / (1024 * 1024)).toFixed(2)} MB`);
console.log(`📈 Compression Ratio: ${((1 - zipSize / totalBytes) * 100).toFixed(1)}% savings`);
console.log('============================================================');
