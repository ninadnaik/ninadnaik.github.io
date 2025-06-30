# Personal Website Directory Structure

This document shows the complete directory structure for the personal website project.

```
personal_website/
├── .DS_Store
├── .github/
│   └── workflows/
│       └── hugo.yml
├── .gitmodules
├── .hugo_build.lock
├── CNAME
├── LICENSE
├── archetypes/
│   └── default.md
├── assets/
├── content/
│   ├── .DS_Store
│   ├── about.md
│   └── posts/
│       ├── .DS_Store
│       └── 1_what_is_intelligence.md
├── data/
├── hugo.toml
├── i18n/
├── layouts/
├── notes/
├── public/
│   ├── .DS_Store
│   ├── 404.html
│   ├── about/
│   │   └── index.html
│   ├── assets/
│   │   └── css/
│   │       └── stylesheet.d6fcd20a4fb86efa4dfac8ec95da60244cc8871042183da1ef28e3a762ad79c8.css
│   ├── categories/
│   │   ├── index.html
│   │   └── index.xml
│   ├── index.html
│   ├── index.xml
│   ├── posts/
│   │   ├── .DS_Store
│   │   ├── 1_what_is_intelligence/
│   │   │   └── index.html
│   │   ├── index.html
│   │   ├── index.xml
│   │   ├── page/
│   │   │   └── 1/
│   │   │       └── index.html
│   │   └── welcome/
│   │       └── index.html
│   ├── robots.txt
│   ├── sitemap.xml
│   └── tags/
│       ├── .DS_Store
│       ├── ai/
│       │   ├── index.html
│       │   ├── index.xml
│       │   └── page/
│       │       └── 1/
│       │           └── index.html
│       ├── index.html
│       ├── index.xml
│       ├── intelligence/
│       │   ├── index.html
│       │   ├── index.xml
│       │   └── page/
│       │       └── 1/
│       │           └── index.html
│       ├── product-management/
│       │   ├── index.html
│       │   ├── index.xml
│       │   └── page/
│       │       └── 1/
│       │           └── index.html
│       └── technology/
│           ├── index.html
│           ├── index.xml
│           └── page/
│               └── 1/
│                   └── index.html
├── research/
│   ├── inbox/
│   └── processed/
├── scripts/
├── static/
└── themes/
    ├── .DS_Store
    └── PaperMod/
        ├── .DS_Store
        ├── .git/
        ├── .github/
        │   ├── ISSUE_TEMPLATE/
        │   │   ├── bug.yaml
        │   │   ├── config.yml
        │   │   └── enhancement.yaml
        │   ├── PULL_REQUEST_TEMPLATE.md
        │   └── workflows/
        │       └── gh-pages.yml
        ├── LICENSE
        ├── README.md
        ├── assets/
        │   ├── css/
        │   │   ├── common/
        │   │   │   ├── 404.css
        │   │   │   ├── archive.css
        │   │   │   ├── footer.css
        │   │   │   ├── header.css
        │   │   │   ├── main.css
        │   │   │   ├── post-entry.css
        │   │   │   ├── post-single.css
        │   │   │   ├── profile-mode.css
        │   │   │   ├── search.css
        │   │   │   └── terms.css
        │   │   ├── core/
        │   │   │   ├── license.css
        │   │   │   ├── reset.css
        │   │   │   ├── theme-vars.css
        │   │   │   └── zmedia.css
        │   │   ├── extended/
        │   │   │   └── blank.css
        │   │   └── includes/
        │   │       ├── chroma-mod.css
        │   │       ├── chroma-styles.css
        │   │       └── scroll-bar.css
        │   └── js/
        │       ├── fastsearch.js
        │       ├── fuse.basic.min.js
        │       └── license.js
        ├── go.mod
        ├── i18n/
        │   ├── ar.yaml
        │   ├── be.yaml
        │   ├── bg.yaml
        │   ├── bn.yaml
        │   ├── ca.yaml
        │   ├── ckb.yaml
        │   ├── cs.yaml
        │   ├── da.yaml
        │   ├── de.yaml
        │   ├── el.yaml
        │   ├── en.yaml
        │   ├── eo.yaml
        │   ├── es.yaml
        │   ├── fa.yaml
        │   ├── fr.yaml
        │   ├── he.yaml
        │   ├── hi.yaml
        │   ├── hr.yaml
        │   ├── hu.yaml
        │   ├── id.yaml
        │   ├── it.yaml
        │   ├── ja.yaml
        │   ├── ko.yaml
        │   ├── ku.yaml
        │   ├── mn.yaml
        │   ├── ms.yaml
        │   ├── nl.yaml
        │   ├── no.yaml
        │   ├── oc.yaml
        │   ├── pa.yaml
        │   ├── pl.yaml
        │   ├── pnb.yaml
        │   ├── pt.yaml
        │   ├── ro.yaml
        │   ├── ru.yaml
        │   ├── sk.yaml
        │   ├── sv.yaml
        │   ├── sw.yaml
        │   ├── th.yaml
        │   ├── tr.yaml
        │   ├── uk.yaml
        │   ├── uz.yaml
        │   ├── vi.yaml
        │   ├── zh-tw.yaml
        │   └── zh.yaml
        ├── images/
        │   ├── screenshot.png
        │   └── tn.png
        ├── layouts/
        │   ├── 404.html
        │   ├── _default/
        │   │   ├── _markup/
        │   │   │   └── render-image.html
        │   │   ├── archives.html
        │   │   ├── baseof.html
        │   │   ├── index.json
        │   │   ├── list.html
        │   │   ├── rss.xml
        │   │   ├── search.html
        │   │   ├── single.html
        │   │   └── terms.html
        │   ├── partials/
        │   │   ├── anchored_headings.html
        │   │   ├── author.html
        │   │   ├── breadcrumbs.html
        │   │   ├── comments.html
        │   │   ├── cover.html
        │   │   ├── edit_post.html
        │   │   ├── extend_footer.html
        │   │   ├── extend_head.html
        │   │   ├── footer.html
        │   │   ├── head.html
        │   │   ├── header.html
        │   │   ├── home_info.html
        │   │   ├── index_profile.html
        │   │   ├── post_canonical.html
        │   │   ├── post_meta.html
        │   │   ├── post_nav_links.html
        │   │   ├── share_icons.html
        │   │   ├── social_icons.html
        │   │   ├── svg.html
        │   │   ├── templates/
        │   │   │   ├── _funcs/
        │   │   │   │   └── get-page-images.html
        │   │   │   ├── opengraph.html
        │   │   │   ├── schema_json.html
        │   │   │   └── twitter_cards.html
        │   │   ├── toc.html
        │   │   └── translation_list.html
        │   ├── robots.txt
        │   └── shortcodes/
        │       ├── collapse.html
        │       ├── figure.html
        │       ├── inTextImg.html
        │       ├── ltr.html
        │       ├── rawhtml.html
        │       └── rtl.html
        └── theme.toml
```

## Directory Summary

This is a Hugo static site generator project with the following structure:

- **Root configuration**: `hugo.toml`, `CNAME`, `.gitmodules`, `.hugo_build.lock`
- **Content**: Blog posts and pages in `content/` directory
- **Themes**: Using PaperMod theme as a Git submodule in `themes/PaperMod/`
- **Generated site**: Built files in `public/` directory
- **GitHub Actions**: Automated deployment via `.github/workflows/hugo.yml`
- **Static assets**: Empty `assets/` and `static/` directories for custom resources
- **Research**: New `research/` directory with `inbox/` and `processed/` subdirectories for content organization
- **Scripts**: New `scripts/` directory for automation and build scripts
- **Notes**: New `notes/` directory for development notes and documentation

The site appears to be a personal blog with posts about AI, intelligence, product management, and technology topics.