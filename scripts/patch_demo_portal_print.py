with open('css/demo-portal.css', 'r', encoding='utf-8') as f:
    cnt = f.read()

# Replace visibility:visible whitelists to also include #srBlueprintPreviewModal
cnt = cnt.replace(
    '#printableExecutiveBrief,#printableExecutiveBrief *{visibility:visible!important}',
    '#printableExecutiveBrief,#printableExecutiveBrief *,#srBlueprintPreviewModal,#srBlueprintPreviewModal *{visibility:visible!important}'
)

cnt = cnt.replace(
    '.roi-cert-modal,.roi-cert-modal *{visibility:visible!important}',
    '.roi-cert-modal,.roi-cert-modal *,#srBlueprintPreviewModal,#srBlueprintPreviewModal *{visibility:visible!important}'
)

cnt = cnt.replace(
    '#contractOf2026FinModal,#contractOf2026FinModal *,#contractOf2026Modal,#contractOf2026Modal *{visibility:visible}',
    '#contractOf2026FinModal,#contractOf2026FinModal *,#contractOf2026Modal,#contractOf2026Modal *,#srBlueprintPreviewModal,#srBlueprintPreviewModal *{visibility:visible}'
)

with open('css/demo-portal.css', 'w', encoding='utf-8') as f:
    f.write(cnt)

print("SUCCESS: Updated css/demo-portal.css print whitelist!")
