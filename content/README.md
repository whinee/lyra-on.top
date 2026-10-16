# Content Directory: content/

This directory holds the single source of truth for all content on `lyra-on.top`.
Content is written in simple YAML and Markdown files and validated by Pydantic models.

## How to add content in 3 lines

### 1. Add a new Project (`content/projects.yaml`)
Append to `projects`:
```yaml
- slug: my-cool-tool
  title: "My Cool Tool"
  summary: "A tiny Python utility for hackers :3"
  repo_url: "https://github.com/whinee/my-cool-tool"
  tags: ["python", "cli"]
  status: "active"
```

### 2. Add a Blog Post (`content/blog/<slug>.md`)
Create a new file e.g. `content/blog/hello-world.md`:
```markdown
---
title: "Hello World :3"
date: "2026-10-14"
summary: "First post on the new site!"
tags: ["intro", "foss"]
---
Nyahallo! Your favorite kittygirl hacker here :3

Write your post content here!
```

### 3. Add a Poem (`content/poems/<slug>.md`)
Create `content/poems/midnight-sparkle.md`:
```markdown
---
title: "Midnight Sparkle"
date: "2026-10-14"
---
paws on the keyboard
terminal glows blurple
stars in the sky :3
```

## Auto-Hide Rule
If a collection folder is empty or has only draft posts, the route and navigation links are automatically hidden from the site.
