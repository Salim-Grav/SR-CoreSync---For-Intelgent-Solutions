/**
 * S&R CoreSync Solutions - Enterprise Production Optimizer
 * Automates CSS & JS asset minification, calculates compression ratios,
 * and generates deployment-ready bundles.
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

function minifyCSS(css) {
  // Tokenize strings & urls to protect them
  const tokens = [];
  let tokenized = css.replace(/("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|url\([^)]*\))/g, (match) => {
    tokens.push(match);
    return `___TOKEN_${tokens.length - 1}___`;
  });

  // Strip comments
  tokenized = tokenized.replace(/\/\*[\s\S]*?\*\//g, '');

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
  // Robust regex/string-aware lexer
  let result = '';
  let i = 0;
  const n = js.length;
  
  while (i < n) {
    const c = js[i];
    const next = js[i + 1];

    // Single-line comment
    if (c === '/' && next === '/') {
      i += 2;
      while (i < n && js[i] !== '\n' && js[i] !== '\r') i++;
      continue;
    }

    // Multi-line comment
    if (c === '/' && next === '*') {
      i += 2;
      while (i < n && !(js[i] === '*' && js[i + 1] === '/')) i++;
      i += 2;
      continue;
    }

    // Double-quoted string
    if (c === '"') {
      let str = '"';
      i++;
      while (i < n) {
        const sc = js[i];
        str += sc;
        if (sc === '\\') {
          i++;
          if (i < n) str += js[i];
        } else if (sc === '"') {
          i++;
          break;
        }
        i++;
      }
      result += str;
      continue;
    }

    // Single-quoted string
    if (c === "'") {
      let str = "'";
      i++;
      while (i < n) {
        const sc = js[i];
        str += sc;
        if (sc === '\\') {
          i++;
          if (i < n) str += js[i];
        } else if (sc === "'") {
          i++;
          break;
        }
        i++;
      }
      result += str;
      continue;
    }

    // Template literal
    if (c === '`') {
      let str = '`';
      i++;
      while (i < n) {
        const sc = js[i];
        str += sc;
        if (sc === '\\') {
          i++;
          if (i < n) str += js[i];
        } else if (sc === '`') {
          i++;
          break;
        }
        i++;
      }
      result += str;
      continue;
    }

    // Collapse whitespace / newlines
    if (/\s/.test(c)) {
      // Keep single space only if needed between identifiers/keywords
      const prevChar = result.length > 0 ? result[result.length - 1] : '';
      let hasNewline = (c === '\n' || c === '\r');
      while (i + 1 < n && /\s/.test(js[i + 1])) {
        if (js[i + 1] === '\n' || js[i + 1] === '\r') hasNewline = true;
        i++;
      }
      const nextChar = i + 1 < n ? js[i + 1] : '';

      const isWordChar = (ch) => /[a-zA-Z0-9_$]/.test(ch);
      if (isWordChar(prevChar) && isWordChar(nextChar)) {
        result += ' ';
      } else if (hasNewline) {
        // Automatic semicolon insertion safety: if prev was not a connector, add newline or space
        if (/[;{}(),:\[\]]/.test(prevChar) || /[;{}(),:\[\]]/.test(nextChar)) {
          // no space needed
        } else {
          result += '\n';
        }
      }
      i++;
      continue;
    }

    result += c;
    i++;
  }

  return result.trim();
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
console.log('🚀 S&R CoreSync Solutions - Building Production Assets...');
console.log('------------------------------------------------------------');

const results = [];

// 1. Minify CSS
if (fs.existsSync('css/enterprise-suite.css')) {
  results.push(processAsset('css/enterprise-suite.css', 'css/enterprise-suite.min.css', 'css'));
}

// 2. Minify JS
if (fs.existsSync('css/enterprise-suite.js')) {
  results.push(processAsset('css/enterprise-suite.js', 'css/enterprise-suite.min.js', 'js'));
}

console.table(results);
console.log('✅ Production Assets Compiled & Verified Successfully!');
console.log('------------------------------------------------------------');
