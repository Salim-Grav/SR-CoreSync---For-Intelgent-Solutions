const fs = require('fs');
const path = require('path');

const demoHtmlPath = path.join(__dirname, '..', 'demo.html');
let html = fs.readFileSync(demoHtmlPath, 'utf8');

// Match any HTML opening tag: <tagname ... >
// Note: handles multiline tags
const tagRegex = /<([a-zA-Z0-9\-]+)(\s+[^>]*?)>/g;

const uniqueStyles = new Map();
let classCounter = 1;

let modifiedCount = 0;

const newHtml = html.replace(tagRegex, (fullTag, tagName, tagAttrs) => {
  // Check if tag has style attribute
  const styleMatch = tagAttrs.match(/\sstyle=(["'])([\s\S]*?)\1(?=[\s>/]|$)/);
  if (!styleMatch) {
    return fullTag;
  }

  const fullStyleAttr = styleMatch[0];
  const css = styleMatch[2].trim();

  let className;
  if (uniqueStyles.has(css)) {
    className = uniqueStyles.get(css);
  } else {
    className = `ds-u${classCounter++}`;
    uniqueStyles.set(css, className);
  }

  // Remove the style attribute from tagAttrs
  let newAttrs = tagAttrs.replace(fullStyleAttr, '');

  // Check if class attribute already exists
  const classMatch = newAttrs.match(/(\sclass=(["']))([\s\S]*?)\2/);
  if (classMatch) {
    // Append className
    const existingClasses = classMatch[3].trim();
    const updatedClassAttr = `${classMatch[1]}${existingClasses} ${className}${classMatch[2]}`;
    newAttrs = newAttrs.replace(classMatch[0], updatedClassAttr);
  } else {
    // Add class attribute
    newAttrs = ` class="${className}"${newAttrs}`;
  }

  modifiedCount++;
  return `<${tagName}${newAttrs}>`;
});

console.log('Modified tags count:', modifiedCount);
console.log('Unique CSS classes created:', uniqueStyles.size);

// Verify if any style= remains
const remaining = newHtml.match(/\sstyle=/g);
console.log('Remaining style= instances:', remaining ? remaining.length : 0);
