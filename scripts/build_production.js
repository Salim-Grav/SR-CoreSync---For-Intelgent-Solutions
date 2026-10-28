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

/**
 * S&R CoreSync For Intelligent Solutions - Enterprise Production Optimizer
 * Automates CSS & JS asset minification, calculates compression ratios,
 * and generates deployment-ready bundles.
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

// Ensure working directory is always the Project root
process.chdir(path.join(__dirname, '..'));

function minifyCSS(css) {
  // Strip comments FIRST to prevent apostrophes in comments from corrupting string tokens
  let cleaned = css.replace(/\/\*[\s\S]*?\*\//g, '');

  // Tokenize strings & urls to protect them
  const tokens = [];
  let tokenized = cleaned.replace(/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|url\([^)]*\))/g, (match) => {
    tokens.push(match);
    return `___TOKEN_${tokens.length - 1}___`;
  });

  // Collapse whitespace
  tokenized = tokenized.replace(/\s+/g, ' ');

  // Remove whitespace around symbols
  tokenized = tokenized.replace(/\s*([{}:;,>~+])\s*/g, '$1');

  // Remove unnecessary trailing semicolons
  tokenized = tokenized.replace(/;}/g, '}');

  // Remove spaces around !important
  tokenized = tokenized.replace(/\s*!important/g, '!important');

  // Restore tokens
  tokenized = tokenized.replace(/___TOKEN_(\d+)___/g, (_, id) => tokens[id]);

  return tokenized.trim();
}

function minifyJS(js) {
  // Strip block comments
  let cleaned = js.replace(/\/\*[\s\S]*?\*\//g, '');

  // Process line by line to safely preserve ASI and regexes
  const lines = cleaned.split('\n');
  const processedLines = [];

  for (let line of lines) {
    let trimmed = line.trim();
    if (!trimmed) continue;
    // Skip single line comments
    if (trimmed.startsWith('//')) continue;
    // Strip trailing comments if safe (not in quotes)
    // For safety, remove inline // comments only if preceded by space and not inside string
    if (!trimmed.includes('://') && !trimmed.includes('"') && !trimmed.includes("'") && !trimmed.includes('`')) {
      const idx = trimmed.indexOf('//');
      if (idx !== -1) {
        trimmed = trimmed.substring(0, idx).trim();
      }
    }
    if (trimmed) {
      processedLines.push(trimmed);
    }
  }

  const result = processedLines.join('\n');
  return result;
}

function processAsset(inputPath, outputPath, type) {
  const content = fs.readFileSync(inputPath, 'utf8');
  const originalSize = Buffer.byteLength(content, 'utf8');

  let minified;
  if (type === 'css') {
    minified = minifyCSS(content);
  } else {
    minified = minifyJS(content);
  }

  // Syntax validation for JS
  if (type === 'js') {
    try {
      new Function(minified);
    } catch (err) {
      console.error(`JS Syntax Validation Error in ${inputPath}:`, err.message);
      process.exit(1);
    }
  }

  fs.writeFileSync(outputPath, minified, 'utf8');

  const minifiedSize = Buffer.byteLength(minified, 'utf8');
  const gzippedSize = zlib.gzipSync(minified).length;
  const savedPercent = ((1 - minifiedSize / originalSize) * 100).toFixed(1);

  return {
    file: path.basename(inputPath),
    output: path.basename(outputPath),
    originalKB: (originalSize / 1024).toFixed(2),
    minifiedKB: (minifiedSize / 1024).toFixed(2),
    gzippedKB: (gzippedSize / 1024).toFixed(2),
    savedPercent: `${savedPercent}%`
  };
}

console.log('------------------------------------------------------------');
console.log('🚀 S&R CoreSync For Intelligent Solutions - Building Production Assets...');
console.log('------------------------------------------------------------');

const results = [];

// 1. Minify CSS
if (fs.existsSync('css/enterprise-suite.css')) {
  results.push(processAsset('css/enterprise-suite.css', 'css/enterprise-suite.min.css', 'css'));
}
if (fs.existsSync('css/invoice-quote-email.css')) {
  results.push(processAsset('css/invoice-quote-email.css', 'css/invoice-quote-email.min.css', 'css'));
}
if (fs.existsSync('css/welcome-email.css')) {
  results.push(processAsset('css/welcome-email.css', 'css/welcome-email.min.css', 'css'));
}

// 2. Minify JS
if (fs.existsSync('css/enterprise-suite.js')) {
  results.push(processAsset('css/enterprise-suite.js', 'css/enterprise-suite.min.js', 'js'));
  if (fs.existsSync('js')) {
    results.push(processAsset('css/enterprise-suite.js', 'js/enterprise-suite.min.js', 'js'));
  }
}
if (fs.existsSync('js/sr-brand-inspector.js')) {
  results.push(processAsset('js/sr-brand-inspector.js', 'js/sr-brand-inspector.min.js', 'js'));
}

console.table(results);
console.log('✅ Production Assets Compiled & Verified Successfully!');
console.log('------------------------------------------------------------');
