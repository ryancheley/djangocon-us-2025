# Django `db_comment`: Self-Documenting Healthcare Databases

DjangoCon US 2025 Presentation by Ryan Cheley

## Running the Presentation

### Setup
1. **Start a local web server** from this directory:
   ```bash
   python3 -m http.server 8002
   ```

2. **Open the presentation** in your browser:
   ```
   http://localhost:8002/index.html
   ```

### Presenter Mode

#### Opening Presenter Mode
- **Press `P`** - Opens presenter mode in a new window
- The presenter window shows:
  - Current slide (left side)
  - Next slide preview (right side)
  - Speaker notes (bottom)
  - Elapsed time timer

#### Setting Up for Presentation
1. **Open presenter mode**: Press `P`
2. **Clone for audience**: Press `C` to open audience view in new window
3. **Position windows**:
   - Put presenter view on your laptop screen
   - Put audience view on projector/external display
4. **Fullscreen audience view**: Press `F` on the audience window

### Navigation Controls
- **Arrow keys** or **Spacebar**: Advance slides
- **Shift + Arrow keys**: Go back
- **Home**: Go to first slide
- **End**: Go to last slide
- **ESC**: Exit fullscreen mode

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `P` | Open/close presenter mode |
| `C` | Clone presentation (open audience view) |
| `F` | Toggle fullscreen |
| `?` | Show help |
| `ESC` | Exit fullscreen |

### Presentation Structure
- **Total slides**: 23 slides
- **Duration**: ~25 minutes
- **Format**: Individual markdown files in `slides/` directory
- **Framework**: Remark.js

### Slide Organization
```
01-title.md                    - Title slide
02-intro-ryan.md              - Speaker introduction
03a-cross-team-confusion-part1.md - Problem scenario (part 1)
03b-cross-team-confusion-part2.md - Problem scenario (part 2)
04-real-cost.md               - Business impact
05-current-state.md           - Current database state
06-documentation-gap.md       - Why docs fail
07-help-text-limitation.md    - help_text problems
08a-08u-*.md                  - Table comparison (21 slides)
09-help-text-falls-short.md   - More help_text issues
10-django-db-comment.md       - Solution introduction
11-what-this-generates.md     - SQL output
12-before-mystery-fields.md   - Before example
13-after-self-documenting.md  - After example
14-complex-json-example.md    - JSON field example
15-table-level-docs.md        - Table-level comments
16-the-migration.md           - Migration safety
17-both-features-together.md  - Combined approach
18a-18d-dba-view-*.md        - DBA perspective
19-start-today.md             - Implementation steps
20-resources.md               - Links and QR codes
21-find-me.md                 - Contact information
22-questions.md               - Q&A
23-thank-you.md               - Closing
```

### Speaker Notes
Every slide includes presenter notes accessible in presenter mode. Notes include:
- Talking points
- Transition guidance
- Key messages to emphasize
- Timing suggestions
- Healthcare-specific context

### Technical Details
- **Framework**: Remark.js
- **Slide format**: Markdown
- **Animations**: Incremental reveals using `--`
- **Styling**: Custom CSS for healthcare presentation theme
- **Images**: Sized with HTML `<img>` tags for better control

### Troubleshooting
- **Slides not loading**: Ensure web server is running from presentation directory
- **Images not showing**: Check that `images/` directory is in same folder as `index.html`
- **Presenter mode not working**: Make sure pop-ups are enabled in your browser
- **Fonts not loading**: Check internet connection (fonts loaded from Google Fonts)

### Tips for Presenting
1. **Practice with presenter mode** before your talk
2. **Test on presentation setup** (projector, laptop, etc.)
3. **Have backup plan** - export to PDF if needed
4. **Use speaker notes** as talking point reminders, not scripts
5. **Engage with audience** during table animation sequence (slides 8a-8u)

### Customization
- **Edit slides**: Modify individual `.md` files in `slides/` directory
- **Update speaker notes**: Add content after `???` in any slide file
- **Adjust styling**: Modify CSS in `index.html`
- **Add slides**: Add filename to `slideFiles` array in `index.html`

---

For questions about the presentation setup, contact Ryan Cheley:
- 🐘 @ryancheley@mastodon.social
- 💼 linkedin.com/in/ryan-cheley
- 📝 ryancheley.com
