# Dashboard & Multi-Chart Patterns

## Layout Principles

### Visual Hierarchy
1. **Most important metric** → largest area, top-left position
2. **Supporting metrics** → smaller cards or secondary charts
3. **Detail views** → bottom or expandable sections

### Grid System
```
┌─────────────────────────────────────┐
│          KEY METRIC (large)         │
├─────────────────┬───────────────────┤
│   Chart A       │     Chart B       │
│   (trend)       │   (breakdown)     │
├─────────────────┴───────────────────┤
│         Detail Table / List         │
└─────────────────────────────────────┘
```

### Recommended Limits
- **3-5 key metrics** per dashboard
- **4-6 charts** maximum (avoid scrolling for key insights)
- **1 primary action** per view

## Small Multiples

Same chart repeated for each category—powerful for comparison.

```javascript
function smallMultiples(container, data, { groupKey, xKey, yKey, columns = 3 }) {
  const groups = d3.group(data, d => d[groupKey]);
  const groupNames = Array.from(groups.keys());

  const cellWidth = 200;
  const cellHeight = 150;
  const margin = { top: 30, right: 10, bottom: 30, left: 40 };

  const rows = Math.ceil(groupNames.length / columns);

  const svg = d3.select(container)
    .append('svg')
    .attr('width', columns * cellWidth)
    .attr('height', rows * cellHeight);

  // Shared scales for comparison
  const allX = data.map(d => d[xKey]);
  const allY = data.map(d => d[yKey]);

  const x = d3.scaleLinear()
    .domain(d3.extent(allX))
    .range([margin.left, cellWidth - margin.right]);

  const y = d3.scaleLinear()
    .domain([0, d3.max(allY)])
    .range([cellHeight - margin.bottom, margin.top]);

  groupNames.forEach((groupName, i) => {
    const col = i % columns;
    const row = Math.floor(i / columns);

    const cell = svg.append('g')
      .attr('transform', `translate(${col * cellWidth},${row * cellHeight})`);

    // Title
    cell.append('text')
      .attr('x', cellWidth / 2)
      .attr('y', 15)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('font-weight', 'bold')
      .text(groupName);

    // Mini axes
    cell.append('g')
      .attr('transform', `translate(0,${cellHeight - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(3).tickSize(3));

    cell.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y).ticks(3).tickSize(3));

    // Data
    const groupData = groups.get(groupName);
    const line = d3.line()
      .x(d => x(d[xKey]))
      .y(d => y(d[yKey]));

    cell.append('path')
      .datum(groupData)
      .attr('fill', 'none')
      .attr('stroke', '#3b82f6')
      .attr('stroke-width', 1.5)
      .attr('d', line);
  });
}
```

## Linked Brushing

Select in one chart, highlight in another.

```javascript
function linkedCharts(container, data) {
  const dispatch = d3.dispatch('brush', 'clear');

  // Chart 1: Scatter plot
  function scatterPlot(sel) {
    // ... create scatter plot ...

    const brush = d3.brush()
      .extent([[0, 0], [innerWidth, innerHeight]])
      .on('brush end', (event) => {
        if (!event.selection) {
          dispatch.call('clear');
          return;
        }
        const [[x0, y0], [x1, y1]] = event.selection;
        const selected = data.filter(d =>
          x(d.xVal) >= x0 && x(d.xVal) <= x1 &&
          y(d.yVal) >= y0 && y(d.yVal) <= y1
        );
        dispatch.call('brush', null, selected);
      });

    g.append('g').call(brush);
  }

  // Chart 2: Bar chart that responds to brush
  function barChart(sel) {
    // ... create bar chart ...

    dispatch.on('brush.bar', (selected) => {
      const selectedIds = new Set(selected.map(d => d.id));
      g.selectAll('.bar')
        .attr('opacity', d => selectedIds.has(d.id) ? 1 : 0.2);
    });

    dispatch.on('clear.bar', () => {
      g.selectAll('.bar').attr('opacity', 1);
    });
  }

  scatterPlot(d3.select('#scatter'));
  barChart(d3.select('#bars'));
}
```

## Sparklines

Tiny inline charts for dashboards.

```javascript
function sparkline(container, values, { width = 100, height = 25, color = '#3b82f6' } = {}) {
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const x = d3.scaleLinear()
    .domain([0, values.length - 1])
    .range([2, width - 2]);

  const y = d3.scaleLinear()
    .domain(d3.extent(values))
    .range([height - 2, 2]);

  const line = d3.line()
    .x((d, i) => x(i))
    .y(d => y(d))
    .curve(d3.curveMonotoneX);

  svg.append('path')
    .datum(values)
    .attr('fill', 'none')
    .attr('stroke', color)
    .attr('stroke-width', 1.5)
    .attr('d', line);

  // End point indicator
  svg.append('circle')
    .attr('cx', x(values.length - 1))
    .attr('cy', y(values[values.length - 1]))
    .attr('r', 2)
    .attr('fill', color);
}
```

## KPI Cards

```html
<div class="kpi-card">
  <div class="kpi-label">Monthly Revenue</div>
  <div class="kpi-value">$1.2M</div>
  <div class="kpi-change positive">▲ 12.5%</div>
  <div class="kpi-sparkline" id="revenue-spark"></div>
</div>

<style>
.kpi-card {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.kpi-label { color: #6b7280; font-size: 12px; }
.kpi-value { font-size: 28px; font-weight: 600; }
.kpi-change { font-size: 14px; }
.kpi-change.positive { color: #22c55e; }
.kpi-change.negative { color: #ef4444; }
</style>
```

## Cross-Filtering Pattern

```javascript
class DashboardState {
  constructor() {
    this.filters = {};
    this.listeners = [];
  }

  setFilter(key, value) {
    this.filters[key] = value;
    this.notify();
  }

  clearFilter(key) {
    delete this.filters[key];
    this.notify();
  }

  getFilteredData(data) {
    return data.filter(d =>
      Object.entries(this.filters).every(([key, value]) =>
        Array.isArray(value) ? value.includes(d[key]) : d[key] === value
      )
    );
  }

  subscribe(fn) {
    this.listeners.push(fn);
  }

  notify() {
    this.listeners.forEach(fn => fn(this.filters));
  }
}

// Usage
const state = new DashboardState();

state.subscribe(() => {
  const filtered = state.getFilteredData(rawData);
  updateChart1(filtered);
  updateChart2(filtered);
  updateChart3(filtered);
});

// When user clicks a bar
bar.on('click', (event, d) => {
  state.setFilter('category', d.category);
});
```

## Responsive Dashboard Grid (CSS)

```css
.dashboard {
  display: grid;
  gap: 16px;
  padding: 16px;
}

/* Mobile: single column */
.dashboard {
  grid-template-columns: 1fr;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
  .dashboard .featured {
    grid-column: span 2;
  }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(3, 1fr);
  }
  .dashboard .featured {
    grid-column: span 2;
  }
}
```

## Dashboard Checklist

- [ ] Clear visual hierarchy (most important = biggest)
- [ ] Consistent color encoding across all charts
- [ ] Shared axes where comparing same metrics
- [ ] Cross-filtering or linked selection
- [ ] Loading states for async data
- [ ] Error states for failed fetches
- [ ] Responsive layout
- [ ] Keyboard accessible controls
- [ ] Print-friendly option
