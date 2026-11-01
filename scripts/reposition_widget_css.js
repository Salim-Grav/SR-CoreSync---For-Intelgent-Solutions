const fs = require('fs');

let css = fs.readFileSync('css/sr-agent-widget.css', 'utf8');

// Hide the standalone floating launcher
css = css.replace(/\.sr-agent-launcher\s*\{[\s\S]*?\}/, `.sr-agent-launcher {
    display: none !important;
}`);

// Reposition the chat window to open from the left beside the floating follow social bar
css = css.replace(/\.sr-agent-window\s*\{[\s\S]*?\}/, `.sr-agent-window {
    position: fixed;
    bottom: 24px;
    left: 72px;
    right: auto;
    z-index: 99998;
    width: 410px;
    max-width: calc(100vw - 88px);
    height: 600px;
    max-height: calc(100vh - 48px);
    background: var(--sr-widget-bg);
    border: 1px solid var(--sr-widget-border);
    border-radius: 20px;
    box-shadow: var(--sr-widget-shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
    transform: translateY(20px) scale(0.96);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    direction: rtl;
    text-align: right;
    font-family: 'Alexandria', 'Tajawal', system-ui, sans-serif;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}`);

// Update mobile media queries
css = css.replace(/@media\s*\(max-width:\s*640px\)\s*\{[\s\S]*?\}/, `@media (max-width: 640px) {
    .sr-agent-window {
        bottom: 12px;
        left: 12px;
        right: 12px;
        width: calc(100vw - 24px);
        max-width: calc(100vw - 24px);
        height: calc(100vh - 24px);
        max-height: calc(100vh - 24px);
    }
}`);

fs.writeFileSync('css/sr-agent-widget.css', css, 'utf8');
console.log('Successfully updated css/sr-agent-widget.css to hide floating FAB and position next to social bar');
