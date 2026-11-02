with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

print_css = """
        @media print {
            *, *::before, *::after {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
            }
            @page {
                size: A4 portrait;
                margin: 8mm;
            }
            body {
                background: #020d18 !important;
                color: #ffffff !important;
            }
            .clgid-topbar {
                display: block !important;
                border-bottom: 2px solid #c5a880 !important;
            }
            .clgid-nav {
                display: none !important;
            }
            .clgid-container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            .clgid-hero {
                padding: 16px 0 !important;
            }
            .clgid-badge {
                border: 1px solid #c5a880 !important;
            }
            .clgid-stat-card, .clgid-paper-card, .clgid-price-card {
                background: #0a1b2a !important;
                border: 1px solid rgba(255,255,255,0.2) !important;
                break-inside: avoid !important;
            }
        }
    </style>"""

cnt = cnt.replace('</style>', print_css)

with open('clgid-prototype.html', 'w', encoding='utf-8') as f:
    f.write(cnt)

print("SUCCESS: Added @media print to clgid-prototype.html")
