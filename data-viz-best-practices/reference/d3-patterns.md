# D3.js Patterns Reference

## Setup

```javascript
// ES Module
import * as d3 from 'd3';

// CDN
<script src="https://d3js.org/d3.v7.min.js"></script>
```

## Standard Chart Structure

```javascript
function createChart(container, data, options = {}) {
  const {
    width = 800,
    height = 400,
    margin = { top: 40, right: 30, bottom: 50, left: 60 }
  } = options;

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Clear previous render
  d3.select(container).selectAll('*').remove();

  // Create SVG with accessibility
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('role', 'img')
    .attr('aria-label', 'Chart description here');

  // Add title for screen readers
  svg.append('title').text('Chart Title');
  svg.append('desc').text('Detailed description of what this chart shows');

  // Main group with margins
  const g = svg.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  return { svg, g, innerWidth, innerHeight };
}
```

## Bar Chart

```javascript
function barChart(container, data, { xKey, yKey, color = '#3b82f6' }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  // Scales
  const x = d3.scaleBand()
    .domain(data.map(d => d[xKey]))
    .range([0, innerWidth])
    .padding(0.2);

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d[yKey])])
    .nice()
    .range([innerHeight, 0]);

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'rotate(-45)')
    .attr('text-anchor', 'end');

  g.append('g')
    .call(d3.axisLeft(y).ticks(5));

  // Bars with transition
  g.selectAll('.bar')
    .data(data)
    .join('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d[xKey]))
    .attr('width', x.bandwidth())
    .attr('y', innerHeight)
    .attr('height', 0)
    .attr('fill', color)
    .transition()
    .duration(600)
    .delay((d, i) => i * 50)
    .attr('y', d => y(d[yKey]))
    .attr('height', d => innerHeight - y(d[yKey]));
}
```

## Line Chart

```javascript
function lineChart(container, data, { xKey, yKey, color = '#3b82f6' }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  // Parse dates if needed
  const parseDate = d3.timeParse('%Y-%m-%d');
  const processedData = data.map(d => ({
    ...d,
    [xKey]: typeof d[xKey] === 'string' ? parseDate(d[xKey]) : d[xKey]
  }));

  // Scales
  const x = d3.scaleTime()
    .domain(d3.extent(processedData, d => d[xKey]))
    .range([0, innerWidth]);

  const y = d3.scaleLinear()
    .domain([0, d3.max(processedData, d => d[yKey])])
    .nice()
    .range([innerHeight, 0]);

  // Line generator
  const line = d3.line()
    .x(d => x(d[xKey]))
    .y(d => y(d[yKey]))
    .curve(d3.curveMonotoneX);

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x).ticks(6));

  g.append('g')
    .call(d3.axisLeft(y).ticks(5));

  // Line path
  const path = g.append('path')
    .datum(processedData)
    .attr('fill', 'none')
    .attr('stroke', color)
    .attr('stroke-width', 2)
    .attr('d', line);

  // Animate line drawing
  const length = path.node().getTotalLength();
  path
    .attr('stroke-dasharray', `${length} ${length}`)
    .attr('stroke-dashoffset', length)
    .transition()
    .duration(1000)
    .attr('stroke-dashoffset', 0);

  // Data points
  g.selectAll('.dot')
    .data(processedData)
    .join('circle')
    .attr('class', 'dot')
    .attr('cx', d => x(d[xKey]))
    .attr('cy', d => y(d[yKey]))
    .attr('r', 4)
    .attr('fill', color);
}
```

## Scatter Plot

```javascript
function scatterPlot(container, data, { xKey, yKey, sizeKey, colorKey }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d[xKey])).nice()
    .range([0, innerWidth]);

  const y = d3.scaleLinear()
    .domain(d3.extent(data, d => d[yKey])).nice()
    .range([innerHeight, 0]);

  const size = sizeKey
    ? d3.scaleSqrt()
        .domain(d3.extent(data, d => d[sizeKey]))
        .range([4, 20])
    : () => 6;

  const color = colorKey
    ? d3.scaleOrdinal(d3.schemeTableau10)
        .domain([...new Set(data.map(d => d[colorKey]))])
    : () => '#3b82f6';

  // Axes
  g.append('g')
    .attr('transform', `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x));

  g.append('g')
    .call(d3.axisLeft(y));

  // Points
  g.selectAll('.point')
    .data(data)
    .join('circle')
    .attr('class', 'point')
    .attr('cx', d => x(d[xKey]))
    .attr('cy', d => y(d[yKey]))
    .attr('r', d => size(d[sizeKey]))
    .attr('fill', d => color(d[colorKey]))
    .attr('opacity', 0.7);
}
```

## Tooltips

```javascript
function addTooltip(container) {
  const tooltip = d3.select(container)
    .append('div')
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('visibility', 'hidden')
    .style('background', '#1f2937')
    .style('color', '#fff')
    .style('padding', '8px 12px')
    .style('border-radius', '4px')
    .style('font-size', '12px')
    .style('pointer-events', 'none')
    .style('z-index', '1000');

  return {
    show: (event, html) => {
      tooltip
        .html(html)
        .style('visibility', 'visible')
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY - 10}px`);
    },
    hide: () => {
      tooltip.style('visibility', 'hidden');
    }
  };
}

// Usage with bars
const { show, hide } = addTooltip(container);

g.selectAll('.bar')
  .on('mouseover', (event, d) => show(event, `<strong>${d.name}</strong><br>Value: ${d.value}`))
  .on('mouseout', hide);
```

## Zoom and Pan

```javascript
function addZoom(svg, g, innerWidth, innerHeight, x, y, redraw) {
  const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .translateExtent([[0, 0], [innerWidth, innerHeight]])
    .on('zoom', (event) => {
      const newX = event.transform.rescaleX(x);
      const newY = event.transform.rescaleY(y);
      redraw(newX, newY);
    });

  svg.call(zoom);

  // Reset button
  d3.select('#reset-zoom').on('click', () => {
    svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
  });
}
```

## Responsive Sizing

```javascript
function makeResponsive(container, renderFn) {
  const resizeObserver = new ResizeObserver(entries => {
    for (const entry of entries) {
      const { width, height } = entry.contentRect;
      renderFn({ width, height });
    }
  });

  resizeObserver.observe(container);

  // Return cleanup function
  return () => resizeObserver.disconnect();
}
```

## Scales Quick Reference

| Scale | Use Case | Example |
|-------|----------|---------|
| `scaleLinear()` | Continuous numeric | Y-axis values |
| `scaleLog()` | Exponential data | Population, revenue |
| `scaleTime()` | Dates/times | X-axis timeline |
| `scaleBand()` | Categorical bars | X-axis categories |
| `scaleOrdinal()` | Categorical colors | Legend colors |
| `scaleSequential()` | Heatmap colors | `d3.interpolateBlues` |
| `scaleDiverging()` | Pos/neg values | `d3.interpolateRdBu` |

## Color Schemes

```javascript
// Categorical (up to 10)
d3.schemeTableau10
d3.schemeCategory10

// Sequential
d3.interpolateBlues
d3.interpolateViridis  // colorblind-safe
d3.interpolateCividis  // colorblind-safe

// Diverging
d3.interpolateRdBu
d3.interpolateBrBG
```

## Performance Tips

- >1000 elements: Use Canvas instead of SVG
- Debounce resize handlers: `d3.debounce(render, 150)`
- Use `.join()` instead of enter/update/exit
- Avoid layout thrashing: batch DOM reads, then writes
- For force simulations: reduce iterations, increase alpha decay
