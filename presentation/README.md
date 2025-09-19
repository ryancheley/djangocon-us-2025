# Django `db_comment`: Self-Documenting Healthcare Databases

DjangoCon US 2025 Presentation by Ryan Cheley

## Running the Presentation

### Quick Start with just
```bash
# Start presentation server and open browser
just present

# Stop the server when done
just stop

# List all available commands
just
```

### Manual Setup (Alternative)
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
- **Total slides**: 86 slides
- **Duration**: ~25 minutes
- **Format**: Individual markdown files in `slides/` directory
- **Framework**: Remark.js

### Current Slide Organization
The presentation is organized into sections with incremental reveals:

**Opening & Problem (slides 00-09)**
- `00-start.md` - Starting slide
- `01-title.md` - Title slide
- `02a-02d-intro-ryan.md` - Speaker introduction (4 slides)
- `03a-03d-cross-team-confusion-*.md` - Problem scenario (4 slides)
- `04a-04b-real-cost.md` - Business impact (2 slides)

**Current State Analysis (slides 05-09)**
- `05a-05f-current-state.md` - Database state examples (6 slides)
- `06a-06e-documentation-gap.md` - Why docs fail (5 slides)
- `07a-07z-help-text-limitation.md` - help_text problems (5 slides)

**Stakeholder Analysis (slides 08a-08u)**
- `08a-table-header.md` - Table introduction
- `08b-08u-*-stakeholder.md` - Multi-stakeholder comparison:
  - End Users (4 slides)
  - Developers (4 slides)
  - DBAs (4 slides)
  - Auditors (4 slides)
  - Analysts (4 slides)
- `09-help-text-falls-short.md` - Summary

**Solution Introduction (slides 10-18)**
- `10a-10f-django-db-comment.md` - Solution intro (6 slides)
- `11a-11c-what-this-generates.md` - SQL output (3 slides)
- `12a-12g-before-mystery-fields.md` - Before example (6 slides)
- `13a-13d-after-self-documenting.md` - After example (4 slides)
- `14a-14c-complex-json-example.md` - JSON & combined features (3 slides)
- `15a-16b-table-level-docs.md` - Table-level comments (4 slides)
- `18-full-table.md` - Complete example

**Implementation & Closing (slides 19-22)**
- `19a-19f-start-today-*.md` - Implementation steps (6 slides)
- `20-make-documentation-a-habit.md` - Call to action
- `21-thank-you.md` - Closing
- `22-find-me.md` - Contact info
- `22-questions.md` - Q&A

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
5. **Engage with audience** during stakeholder table sequence (slides 08b-08u)
6. **Time your sections** - use incremental reveals to control pacing

### Directory Structure
```
presentation/
├── index.html              # Main presentation file
├── justfile               # Command runner (present/stop)
├── slides.js              # Slide loading logic
├── styles.css             # Presentation styling
├── remark-latest.min.js   # Remark.js framework
├── presentation-outline.md # Original outline
├── images/                # Presentation images
├── fonts/                 # Custom fonts
├── slides/                # 86 individual slide files
├── transcript/            # Development transcripts
└── feedback/              # Iterative feedback files
```

### Customization
- **Edit slides**: Modify individual `.md` files in `slides/` directory
- **Update speaker notes**: Add content after `???` in any slide file
- **Adjust styling**: Modify `styles.css`
- **Add slides**: Update slide loading in `slides.js`

---

For questions about the presentation setup, contact Ryan Cheley:
- 🐘 @ryancheley@mastodon.social
- 💼 linkedin.com/in/ryan-cheley
- 📝 ryancheley.com
