# -*- coding: utf-8 -*-
with open('css/enterprise-suite.min.css', 'r', encoding='utf-8') as f:
    content = f.read()

target = '.section-selected-work{position:relative;background:#010907;border-radius:28px;padding:60px 0 50px 0;overflow:hidden;border:1px solid rgba(197,168,128,0.16);box-shadow:0 30px 80px rgba(0,0,0,0.7)}'

replacement = target + '.section-selected-work--original .bg-img{position:absolute!important;inset:0!important;z-index:1!important;pointer-events:none!important;display:flex!important;align-items:flex-end!important;justify-content:center!important;opacity:0.28!important;mix-blend-mode:luminosity!important}.section-selected-work--original .bg-img img{width:100%!important;height:auto!important;max-height:380px!important;object-fit:cover!important;object-position:bottom center!important;transform:translateY(40px)!important;-webkit-mask-image:linear-gradient(180deg,transparent 0%,rgba(0,0,0,0.6) 35%,#000 100%)!important;mask-image:linear-gradient(180deg,transparent 0%,rgba(0,0,0,0.6) 35%,#000 100%)!important;filter:brightness(0.65) contrast(1.15)!important}.section-selected-work--original .work-head,.section-selected-work--original .tab-content,.section-selected-work--original .work-pane,.section-selected-work--original .content-wrap-1,.section-selected-work--original .content-wrap-2{position:relative!important;z-index:5!important}.section-selected-work--original .content-wrap-2{padding-bottom:25px!important}.section-selected-work--original #work-project-tags,.section-selected-work--original .group-btn-slider,.section-selected-work--original .work-year{position:relative!important;z-index:10!important}.section-selected-work--original #work-project-tags .tf-btn.style-2{background:rgba(12,21,17,0.92)!important;border:1px solid rgba(197,168,128,0.45)!important;color:#f3dfba!important;-webkit-backdrop-filter:blur(12px)!important;backdrop-filter:blur(12px)!important;box-shadow:0 4px 15px rgba(0,0,0,0.6)!important;font-size:0.85rem!important;padding:6px 14px!important;border-radius:999px!important;display:inline-flex!important;align-items:center!important;gap:6px!important}.section-selected-work--original .group-btn-slider .btn-nav-swiper{background:rgba(12,21,17,0.85)!important;border:1px solid rgba(197,168,128,0.35)!important;color:#f3dfba!important;padding:6px 14px!important;border-radius:999px!important;box-shadow:0 4px 15px rgba(0,0,0,0.5)!important;transition:all 0.25s ease!important}.section-selected-work--original .group-btn-slider .btn-nav-swiper:hover{border-color:#f3dfba!important;color:#fff!important;background:rgba(197,168,128,0.25)!important}'

if target in content:
    content = content.replace(target, replacement, 1)
    with open('css/enterprise-suite.min.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated enterprise-suite.min.css")
else:
    print("Target not found in enterprise-suite.min.css")
