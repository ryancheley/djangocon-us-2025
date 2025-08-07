async function loadSlides() {
    let allSlides = '';

    try {
        // First, fetch the list of files in the slides directory
        // Since we can't directly list directory contents in the browser,
        // we'll fetch a known file that lists all slides or use a different approach

        // For now, we'll create a list endpoint or use a different strategy
        // Let's try to fetch the slides directory listing
        const response = await fetch('slides/');
        const text = await response.text();

        // Parse the directory listing to find .md files
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const links = Array.from(doc.querySelectorAll('a'));

        // Extract .md files and sort them naturally
        const slideFiles = links
            .map(link => link.getAttribute('href'))
            .filter(href => href && href.endsWith('.md'))
            .sort((a, b) => {
                // Natural sort to handle numbers correctly
                return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
            });

        console.log('Found slide files:', slideFiles);

        if (slideFiles.length === 0) {
            throw new Error('No .md files found in slides directory');
        }

        // Load each slide file
        for (let i = 0; i < slideFiles.length; i++) {
            const file = slideFiles[i];
            console.log(`Loading ${file}...`);
            const slideResponse = await fetch(`slides/${file}`);

            if (!slideResponse.ok) {
                throw new Error(`HTTP error loading ${file}! status: ${slideResponse.status}`);
            }

            const content = await slideResponse.text();
            console.log(`Loaded ${file}, content length: ${content.length}`);

            allSlides += content;

            // Add separator between slides except for the last one
            if (i < slideFiles.length - 1) {
                allSlides += '\n\n---\n\n';
            }
        }


        console.log(`Total slides content length: ${allSlides.length}`);

        // Initialize remark directly with the content
        var slideshow = remark.create({
            source: allSlides,
            ratio: '16:9',
            highlightStyle: 'monokai',
            highlightLanguage: 'python',
            highlightLines: true,
            countIncrementalSlides: false,
            navigation: {
                scroll: false,
                touch: true,
                click: false
            }
        });

        console.log('Remark slideshow initialized successfully');

        // Add debounced navigation to prevent double-clicks from presentation pointers
        let lastNavigationTime = 0;
        const DEBOUNCE_DELAY = 300; // milliseconds

        // Override the default navigation functions with debounced versions
        const originalNext = slideshow.gotoNextSlide.bind(slideshow);
        const originalPrev = slideshow.gotoPreviousSlide.bind(slideshow);

        slideshow.gotoNextSlide = function() {
            const now = Date.now();
            if (now - lastNavigationTime > DEBOUNCE_DELAY) {
                lastNavigationTime = now;
                originalNext();
            }
        };

        slideshow.gotoPreviousSlide = function() {
            const now = Date.now();
            if (now - lastNavigationTime > DEBOUNCE_DELAY) {
                lastNavigationTime = now;
                originalPrev();
            }
        };

    } catch (error) {
        console.error('Error loading slides:', error);

        // Initialize remark with error message
        var slideshow = remark.create({
            source: `# Error Loading Slides\n\nUnable to load slides: ${error.message}`,
            ratio: '16:9'
        });
    }
}

// Load slides when page is ready
document.addEventListener('DOMContentLoaded', loadSlides);
