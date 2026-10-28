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
 * S&R CoreSync For Intelligent Solutions - Comprehensive Site Quality & Accessibility Auditor
 * Audits index.html (AR), en/index.html (EN), nl/index.html (NL) for SEO & WCAG standards
 */

const fs = require('fs');
const path = require('path');

const PAGES = [
  { file: 'index.html', lang: 'ar', name: 'Arabic (Main)' },
  { file: 'en/index.html', lang: 'en', name: 'English' },
  { file: 'nl/index.html', lang: 'nl', name: 'Dutch' }
];

function auditPage(pageConfig) {
  const filePath = path.resolve(pageConfig.file);
  if (!fs.existsSync(filePath)) {
    return { error: `File not found: ${pageConfig.file}` };
  }

  const html = fs.readFileSync(filePath, 'utf8');
  const issues = [];
  const metrics = {};

  // 1. Check DOCTYPE and HTML lang
  const hasDoctype = /<!DOCTYPE html>/i.test(html);
  if (!hasDoctype) issues.push('Missing <!DOCTYPE html>');

  const htmlTagMatch = html.match(/<html([^>]*)>/i);
  if (!htmlTagMatch || !htmlTagMatch[1].includes('lang=')) {
    issues.push('Missing lang attribute on <html> element');
  } else {
    metrics.htmlLang = htmlTagMatch[1].match(/lang=["']([^"']+)["']/i)?.[1];
  }

  // 2. SEO Meta Tags
  const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
  metrics.title = titleMatch ? titleMatch[1].trim() : null;
  if (!metrics.title) issues.push('Missing or empty <title>');

  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']+)["'][^>]*>/i);
  metrics.description = descMatch ? descMatch[1].trim() : null;
  if (!metrics.description) issues.push('Missing meta description');

  const viewportMatch = html.match(/<meta[^>]*name=["']viewport["'][^>]*content=["']([^"']+)["'][^>]*>/i);
  if (!viewportMatch) issues.push('Missing meta viewport');

  const canonicalMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["'][^>]*>/i);
  metrics.canonical = canonicalMatch ? canonicalMatch[1].trim() : null;
  if (!metrics.canonical) issues.push('Missing canonical link');

  // Hreflang tags
  const hreflangs = [...html.matchAll(/<link[^>]*rel=["']alternate["'][^>]*hreflang=["']([^"']+)["'][^>]*href=["']([^"']+)["'][^>]*>/gi)];
  metrics.hreflangCount = hreflangs.length;
  if (hreflangs.length === 0) issues.push('Missing hreflang alternate links');

  // 3. Headings Structure (Single h1)
  const h1Matches = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)];
  metrics.h1Count = h1Matches.length;
  if (h1Matches.length === 0) issues.push('Missing <h1> element');
  if (h1Matches.length > 1) issues.push(`Multiple <h1> elements found (${h1Matches.length})`);

  // 4. Duplicate IDs
  const idRegex = /\sid=["']([^"']+)["']/gi;
  const idOccurrences = {};
  const lines = html.split('\n');
  lines.forEach((lineText, lineIdx) => {
    let m;
    const re = /\sid=["']([^"']+)["']/gi;
    while ((m = re.exec(lineText)) !== null) {
      const id = m[1];
      if (!idOccurrences[id]) idOccurrences[id] = [];
      idOccurrences[id].push(lineIdx + 1);
    }
  });

  const duplicateIds = Object.keys(idOccurrences).filter(id => idOccurrences[id].length > 1);
  metrics.duplicateIdsCount = duplicateIds.length;
  if (duplicateIds.length > 0) {
    issues.push(`Duplicate IDs detected: ${duplicateIds.join(', ')}`);
    metrics.duplicateDetails = duplicateIds.map(id => ({ id, lines: idOccurrences[id] }));
  }

  // 5. Image Accessibility (Alt tags)
  const imgRegex = /<img\b([^>]*)>/gi;
  let totalImgs = 0;
  let missingAlt = 0;
  let missingLazy = 0;
  while ((match = imgRegex.exec(html)) !== null) {
    totalImgs++;
    const attrs = match[1];
    if (!/alt=["']/i.test(attrs)) {
      missingAlt++;
    }
    if (!/loading=["']lazy["']/i.test(attrs) && !/loading=["']eager["']/i.test(attrs)) {
      missingLazy++;
    }
  }
  metrics.totalImages = totalImgs;
  metrics.missingAlt = missingAlt;
  if (missingAlt > 0) issues.push(`${missingAlt} images missing alt attribute`);

  // 6. Buttons without accessible text
  const buttonRegex = /<button\b([^>]*)>([\s\S]*?)<\/button>/gi;
  let emptyButtons = 0;
  while ((match = buttonRegex.exec(html)) !== null) {
    const attrs = match[1];
    const content = match[2].replace(/<[^>]+>/g, '').trim();
    const hasAria = /aria-label=["'][^"']+["']/i.test(attrs) || /title=["'][^"']+["']/i.test(attrs);
    if (!content && !hasAria) {
      emptyButtons++;
    }
  }
  metrics.emptyButtons = emptyButtons;
  if (emptyButtons > 0) issues.push(`${emptyButtons} buttons missing accessible label/text`);

  // 7. Icon-only links without accessible name
  const aRegex = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;
  let emptyLinks = 0;
  while ((match = aRegex.exec(html)) !== null) {
    const attrs = match[1];
    const content = match[2].replace(/<[^>]+>/g, '').trim();
    const hasAria = /aria-label=["'][^"']+["']/i.test(attrs) || /title=["'][^"']+["']/i.test(attrs);
    if (!content && !hasAria && !/href=["']#["']/i.test(attrs)) {
      emptyLinks++;
    }
  }
  metrics.emptyLinks = emptyLinks;
  if (emptyLinks > 0) issues.push(`${emptyLinks} links missing accessible label/text`);

  return {
    page: pageConfig.name,
    file: pageConfig.file,
    metrics,
    issues,
    status: issues.length === 0 ? 'PASS' : 'NEEDS_ATTENTION'
  };
}

console.log('============================================================');
console.log('🔍 S&R CoreSync For Intelligent Solutions - Comprehensive Audit');
console.log('============================================================\n');

PAGES.forEach(p => {
  const res = auditPage(p);
  console.log(`Page: ${res.page} (${res.file})`);
  console.log(`Status: ${res.status === 'PASS' ? '✅ PASS' : '⚠️ ISSUES DETECTED'}`);
  console.log(`Title: ${res.metrics.title}`);
  console.log(`Canonical: ${res.metrics.canonical || 'None'}`);
  console.log(`Hreflang tags: ${res.metrics.hreflangCount}`);
  console.log(`Images: ${res.metrics.totalImages} total (${res.metrics.missingAlt} missing alt)`);
  console.log(`Duplicate IDs: ${res.metrics.duplicateIdsCount}`);
  if (res.issues.length > 0) {
    console.log('Issues:');
    res.issues.forEach(i => console.log(`  - ${i}`));
  }
  if (res.metrics.duplicateDetails) {
    console.log('Duplicate ID Details:');
    res.metrics.duplicateDetails.forEach(d => {
      console.log(`  #${d.id}: lines ${d.lines.join(', ')}`);
    });
  }
  console.log('------------------------------------------------------------\n');
});
