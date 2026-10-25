/**
 * S&R CoreSync For Intelligent Solutions - Zero Warnings Refactoring Engine
 * Extracts all inline styles from demo.html into css/demo-portal.css
 */
const fs = require('fs');
const path = require('path');

const projectDir = path.join(__dirname, '..');
const demoHtmlPath = path.join(projectDir, 'demo.html');
const demoCssPath = path.join(projectDir, 'css', 'demo-portal.css');

let html = fs.readFileSync(demoHtmlPath, 'utf8');
let css = fs.readFileSync(demoCssPath, 'utf8');

// Match HTML opening tags
const tagRegex = /<([a-zA-Z0-9\-]+)(\s+[^>]*?)>/g;

const uniqueStyles = new Map();
let classCounter = 1;
let modifiedCount = 0;

const newHtml = html.replace(tagRegex, (fullTag, tagName, tagAttrs) => {
  const styleMatch = tagAttrs.match(/\sstyle=(["'])([\s\S]*?)\1(?=[\s>/]|$)/);
  if (!styleMatch) {
    return fullTag;
  }

  const fullStyleAttr = styleMatch[0];
  const cssDeclarations = styleMatch[2].trim();

  let className;
  if (uniqueStyles.has(cssDeclarations)) {
    className = uniqueStyles.get(cssDeclarations);
  } else {
    className = `ds-u${classCounter++}`;
    uniqueStyles.set(cssDeclarations, className);
  }

  // Remove the style attribute from tagAttrs
  let newAttrs = tagAttrs.replace(fullStyleAttr, '');

  // Check if class attribute already exists
  const classMatch = newAttrs.match(/(\sclass=(["']))([\s\S]*?)\2/);
  if (classMatch) {
    const existingClasses = classMatch[3].trim();
    const updatedClassAttr = `${classMatch[1]}${existingClasses} ${className}${classMatch[2]}`;
    newAttrs = newAttrs.replace(classMatch[0], updatedClassAttr);
  } else {
    newAttrs = ` class="${className}"${newAttrs}`;
  }

  modifiedCount++;
  return `<${tagName}${newAttrs}>`;
});

// Format CSS rules
let generatedCSS = '\n\n/* ==========================================================================\n'
  + '   Zero Warnings Refactoring: Extracted Inline Styles Utility Classes\n'
  + '   ========================================================================== */\n';

for (const [rules, cls] of uniqueStyles.entries()) {
  let formattedRules = rules;
  if (!formattedRules.endsWith(';')) {
    formattedRules += ';';
  }
  generatedCSS += `.${cls} { ${formattedRules} }\n`;
}

// Write updated files
fs.writeFileSync(demoHtmlPath, newHtml, 'utf8');
fs.writeFileSync(demoCssPath, css + generatedCSS, 'utf8');

console.log(`✅ Success! Converted ${modifiedCount} inline style attributes into ${uniqueStyles.size} CSS classes.`);
