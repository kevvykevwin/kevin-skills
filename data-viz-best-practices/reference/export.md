# Export & Publication Reference

## SVG Export

### Download SVG from DOM

```javascript
function downloadSVG(svgElement, filename = 'chart.svg') {
  // Clone to avoid modifying original
  const clone = svgElement.cloneNode(true);

  // Inline computed styles
  inlineStyles(clone);

  // Add XML declaration
  const serializer = new XMLSerializer();
  let svgString = serializer.serializeToString(clone);
  svgString = '<?xml version="1.0" encoding="UTF-8"?>\n' + svgString;

  // Create blob and download
  const blob = new Blob([svgString], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();

  URL.revokeObjectURL(url);
}

function inlineStyles(element) {
  const computed = getComputedStyle(element);
  const styles = ['font-family', 'font-size', 'font-weight', 'fill', 'stroke', 'stroke-width', 'opacity'];

  styles.forEach(style => {
    element.style[style] = computed[style];
  });

  Array.from(element.children).forEach(inlineStyles);
}
```

### SVG to PNG Conversion

```javascript
function downloadPNG(svgElement, filename = 'chart.png', scale = 2) {
  const clone = svgElement.cloneNode(true);
  inlineStyles(clone);

  const svgString = new XMLSerializer().serializeToString(clone);
  const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);

  const img = new Image();
  img.onload = () => {
    const canvas = document.createElement('canvas');
    canvas.width = svgElement.clientWidth * scale;
    canvas.height = svgElement.clientHeight * scale;

    const ctx = canvas.getContext('2d');
    ctx.scale(scale, scale);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);

    canvas.toBlob(blob => {
      const pngUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = pngUrl;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(pngUrl);
    }, 'image/png');

    URL.revokeObjectURL(url);
  };

  img.src = url;
}
```

## Plotly Export

```javascript
// Built-in export
Plotly.downloadImage(graphDiv, {
  format: 'png',  // 'png', 'svg', 'jpeg', 'webp'
  width: 1200,
  height: 800,
  scale: 2,       // Retina
  filename: 'my-chart'
});

// Get SVG string
Plotly.toImage(graphDiv, { format: 'svg' })
  .then(dataUrl => {
    // dataUrl is base64 SVG
  });
```

## Print Optimization

### CSS for Print

```css
@media print {
  /* Hide non-essential UI */
  .controls, .filters, .export-buttons {
    display: none !important;
  }

  /* Ensure charts are visible */
  .chart-container {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  /* Force colors (browsers often remove them) */
  .chart-container {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Adjust sizes for paper */
  .chart-container {
    width: 100% !important;
    max-width: 7in;
    margin: 0 auto;
  }

  /* Lighter backgrounds for ink saving */
  .kpi-card {
    background: #fff !important;
    border: 1px solid #ccc !important;
    box-shadow: none !important;
  }
}
```

### Print-Specific Considerations

1. **Color**: Use darker colors—light colors may not print well
2. **Line width**: Minimum 1pt (1.33px) for visibility
3. **Font size**: Minimum 8pt for labels
4. **Resolution**: Export at 300 DPI for print (scale: 3-4 for retina)
5. **Margins**: Leave space for binding if needed

## Publication-Ready Dimensions

| Output | Width | Height | Notes |
|--------|-------|--------|-------|
| **Web full-width** | 800-1200px | 400-600px | 16:9 or 4:3 aspect |
| **Web half-width** | 400-600px | 300-400px | For side-by-side |
| **Journal single column** | 3.5in (252pt) | varies | ~300 DPI |
| **Journal double column** | 7in (504pt) | varies | ~300 DPI |
| **Presentation (16:9)** | 1920px | 1080px | Full slide |
| **Social media** | 1200x630px | — | Facebook/LinkedIn |
| **Twitter/X** | 1200x675px | — | 16:9 works |

## Font Embedding for SVG

```javascript
function embedFonts(svgElement) {
  const fontFace = `
    @font-face {
      font-family: 'Inter';
      src: url(data:font/woff2;base64,...) format('woff2');
    }
  `;

  const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
  style.textContent = fontFace;
  svgElement.insertBefore(style, svgElement.firstChild);
}
```

## Batch Export Script (Node.js)

```javascript
const puppeteer = require('puppeteer');

async function exportCharts(urls, outputDir) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  for (const { url, filename } of urls) {
    await page.goto(url, { waitUntil: 'networkidle0' });
    await page.waitForSelector('svg');

    // PNG export
    const element = await page.$('.chart-container');
    await element.screenshot({
      path: `${outputDir}/${filename}.png`,
      omitBackground: false
    });

    // SVG export
    const svgContent = await page.$eval('svg', el => el.outerHTML);
    fs.writeFileSync(`${outputDir}/${filename}.svg`, svgContent);
  }

  await browser.close();
}
```

## Accessibility in Exports

### Include Alt Text Metadata

```javascript
// Add metadata to SVG
function addMetadata(svg, { title, description }) {
  const titleEl = document.createElementNS('http://www.w3.org/2000/svg', 'title');
  titleEl.textContent = title;

  const descEl = document.createElementNS('http://www.w3.org/2000/svg', 'desc');
  descEl.textContent = description;

  svg.insertBefore(descEl, svg.firstChild);
  svg.insertBefore(titleEl, svg.firstChild);

  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', title);
}
```

### Provide Data Table Alternative

```javascript
function generateDataTable(data, columns) {
  const table = document.createElement('table');
  table.className = 'sr-only'; // Screen reader only

  // Header
  const thead = table.createTHead();
  const headerRow = thead.insertRow();
  columns.forEach(col => {
    const th = document.createElement('th');
    th.textContent = col.label;
    headerRow.appendChild(th);
  });

  // Body
  const tbody = table.createTBody();
  data.forEach(row => {
    const tr = tbody.insertRow();
    columns.forEach(col => {
      const td = tr.insertCell();
      td.textContent = row[col.key];
    });
  });

  return table;
}
```

## Quick Export Buttons Component

```html
<div class="export-controls">
  <button onclick="downloadSVG(chart, 'chart.svg')">⬇ SVG</button>
  <button onclick="downloadPNG(chart, 'chart.png', 2)">⬇ PNG</button>
  <button onclick="window.print()">🖨 Print</button>
</div>

<style>
.export-controls {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
.export-controls button {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
}
.export-controls button:hover {
  background: #f3f4f6;
}
</style>
```
