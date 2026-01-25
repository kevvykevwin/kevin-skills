---
name: data-viz-best-practices
description: Data visualization best practices for charts, graphs, and dashboards. Use when creating visualizations, choosing chart types, reviewing chart design, or working with D3/Plotly/Chart.js. Covers chart selection, color accessibility, Tufte principles, and export.
argument-hint: <data-description-or-file>
metadata:
  author: kevinnguyen
  version: "1.0.0"
---

# Data Visualization Best Practices

> Transform data into clear, accurate, accessible visual stories.

## When This Skill Activates

Use when user requests: visualization, chart, graph, plot, dashboard, D3, Plotly, data graphic, heatmap, histogram, or asks "how should I visualize this?"

## Core Principles

### 1. Data-Ink Ratio (Tufte)
Maximize data, minimize decoration.
- Remove: chartjunk, 3D effects, gradient fills, unnecessary gridlines, redundant legends
- Keep: data points, essential labels, minimal axes
- Ask: "Does this pixel represent data?" If no, justify or remove.

### 2. Chart Selection Framework

```
What are you showing?
│
├─ COMPARISON
│  ├─ Few categories (≤7) → Bar chart (horizontal if labels long)
│  ├─ Many categories → Lollipop or dot plot
│  └─ Over time → Line chart
│
├─ DISTRIBUTION
│  ├─ Single variable → Histogram or density plot
│  ├─ Compare groups → Box plot, violin plot
│  └─ Two variables → Scatter plot
│
├─ COMPOSITION
│  ├─ Parts of whole → Stacked bar (NOT pie unless ≤3 slices)
│  ├─ Over time → Stacked area
│  └─ Hierarchical → Treemap or sunburst
│
├─ RELATIONSHIP
│  ├─ Two variables → Scatter plot
│  ├─ Three variables → Bubble chart (size = 3rd var)
│  └─ Network/flow → Force-directed, Sankey, chord
│
└─ GEOGRAPHIC
   ├─ Regional values → Choropleth
   ├─ Point locations → Dot map
   └─ Flows between places → Flow map
```

### 3. Library Selection

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Quick static chart | **Chart.js** or **Plotly** | Fast setup, good defaults |
| Interactive dashboard | **Plotly** | Built-in interactions, responsive |
| Custom/novel visualization | **D3.js** | Full control, bindable to any DOM |
| Statistical/scientific | **Vega-Lite** | Declarative grammar, stats built-in |
| Large datasets (>10k points) | **D3 + Canvas** or **deck.gl** | WebGL performance |
| React project | **Recharts** or **Nivo** | Component-based, D3 under hood |

## Color Guidelines

### Palette Types
- **Sequential**: Light→dark for continuous values (use: heatmaps, choropleths)
- **Diverging**: Two hues meeting at neutral midpoint (use: pos/neg, above/below average)
- **Categorical**: Distinct hues for unordered groups (max 7-8 colors)

### Accessibility Requirements
- Minimum contrast ratio: 3:1 against background
- Never rely on color alone—add patterns, labels, or shapes
- Avoid: red/green as only differentiator
- Test with: Coblis simulator or Stark plugin
- Safe palettes: ColorBrewer2.org, Viridis, Cividis

### Semantic Colors
```
Positive/growth: Green (#22c55e) or Blue (#3b82f6)
Negative/decline: Red (#ef4444)
Neutral/baseline: Gray (#6b7280)
Warning/attention: Amber (#f59e0b)
```

## Accessibility Checklist

- [ ] Color contrast ≥3:1
- [ ] Not color-only encoding (add texture/shape/label)
- [ ] SVG has `role="img"` and `aria-label`
- [ ] Include `<title>` and `<desc>` in SVG
- [ ] Keyboard navigable (tabindex on interactive elements)
- [ ] Provide data table alternative for screen readers
- [ ] Font size ≥12px for labels
- [ ] Test at 200% zoom

## Annotation Strategy

Guide the viewer's eye:
1. **Title**: State the insight, not just the metric ("Sales grew 40% in Q3" > "Q3 Sales")
2. **Subtitle**: Context, time range, data source
3. **Callouts**: Annotate outliers, inflection points, key events
4. **Direct labels**: Label data points when possible (avoid legend lookup)

## Reference Files

For implementation details, see:
- `reference/d3-patterns.md` — D3.js code patterns and examples
- `reference/statistical-viz.md` — Box plots, error bars, confidence intervals
- `reference/dashboards.md` — Multi-chart layouts, linked views
- `reference/export.md` — SVG/PNG export, print preparation

## Quick Start Templates

### Static Bar Chart (Chart.js)
```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: categories,
    datasets: [{ data: values, backgroundColor: '#3b82f6' }]
  },
  options: {
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});
```

### Interactive Line (Plotly)
```javascript
Plotly.newPlot('chart', [{
  x: dates,
  y: values,
  type: 'scatter',
  mode: 'lines+markers'
}], {
  title: 'Metric Over Time',
  xaxis: { title: 'Date' },
  yaxis: { title: 'Value' }
});
```

### Custom SVG (D3.js)
See `reference/d3-patterns.md` for full patterns.

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Pie charts with >3 slices | Hard to compare angles | Use horizontal bar |
| Dual Y-axes | Misleading correlations | Two separate charts |
| 3D charts | Distorts perception | Use 2D always |
| Truncated Y-axis | Exaggerates differences | Start at zero (or clearly label) |
| Rainbow color scales | No perceptual ordering | Use sequential palette |
| Legend far from data | Forces eye movement | Direct label instead |
| Too many gridlines | Visual noise | Minimal or none |

## Common Tasks

### "Visualize this CSV"
1. Read first 5 rows → identify column types
2. Determine question: comparison? distribution? trend?
3. Select chart type from framework above
4. Choose library based on interactivity needs
5. Apply color palette, check accessibility
6. Add title stating the insight

### "Make this chart better"
1. Remove chartjunk (3D, gradients, excessive gridlines)
2. Direct label instead of legend
3. Sort bars by value (not alphabetically)
4. Add meaningful title (insight, not just label)
5. Check color accessibility
6. Reduce to essential elements only

### "Build a dashboard"
1. Identify 3-5 key metrics (no more)
2. Use consistent color encoding across charts
3. Largest/most important chart gets most space
4. Add filtering controls if interactive
5. Link charts for cross-filtering if possible
6. See `reference/dashboards.md`
