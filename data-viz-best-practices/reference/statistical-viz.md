# Statistical Visualization Reference

## Box Plot

Shows distribution: median, quartiles, outliers.

```javascript
function boxPlot(container, data, { groupKey, valueKey }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  // Group data
  const groups = d3.group(data, d => d[groupKey]);
  const summaries = Array.from(groups, ([key, values]) => {
    const sorted = values.map(d => d[valueKey]).sort(d3.ascending);
    const q1 = d3.quantile(sorted, 0.25);
    const median = d3.quantile(sorted, 0.5);
    const q3 = d3.quantile(sorted, 0.75);
    const iqr = q3 - q1;
    const min = Math.max(d3.min(sorted), q1 - 1.5 * iqr);
    const max = Math.min(d3.max(sorted), q3 + 1.5 * iqr);
    const outliers = sorted.filter(v => v < min || v > max);
    return { key, q1, median, q3, min, max, outliers };
  });

  const x = d3.scaleBand()
    .domain(summaries.map(d => d.key))
    .range([0, innerWidth])
    .padding(0.3);

  const y = d3.scaleLinear()
    .domain([
      d3.min(summaries, d => Math.min(d.min, ...d.outliers)),
      d3.max(summaries, d => Math.max(d.max, ...d.outliers))
    ]).nice()
    .range([innerHeight, 0]);

  // Axes
  g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x));
  g.append('g').call(d3.axisLeft(y));

  const boxWidth = x.bandwidth();

  // Draw each box
  summaries.forEach(d => {
    const cx = x(d.key) + boxWidth / 2;

    // Vertical line (whiskers)
    g.append('line')
      .attr('x1', cx).attr('x2', cx)
      .attr('y1', y(d.min)).attr('y2', y(d.max))
      .attr('stroke', '#333');

    // Box (IQR)
    g.append('rect')
      .attr('x', x(d.key))
      .attr('y', y(d.q3))
      .attr('width', boxWidth)
      .attr('height', y(d.q1) - y(d.q3))
      .attr('fill', '#3b82f6')
      .attr('stroke', '#1e40af');

    // Median line
    g.append('line')
      .attr('x1', x(d.key)).attr('x2', x(d.key) + boxWidth)
      .attr('y1', y(d.median)).attr('y2', y(d.median))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);

    // Whisker caps
    [d.min, d.max].forEach(val => {
      g.append('line')
        .attr('x1', cx - boxWidth / 4).attr('x2', cx + boxWidth / 4)
        .attr('y1', y(val)).attr('y2', y(val))
        .attr('stroke', '#333');
    });

    // Outliers
    d.outliers.forEach(val => {
      g.append('circle')
        .attr('cx', cx)
        .attr('cy', y(val))
        .attr('r', 3)
        .attr('fill', 'none')
        .attr('stroke', '#333');
    });
  });
}
```

## Error Bars

Show uncertainty around point estimates.

```javascript
function errorBars(container, data, { xKey, yKey, errorKey }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  const x = d3.scaleBand()
    .domain(data.map(d => d[xKey]))
    .range([0, innerWidth])
    .padding(0.4);

  const yMax = d3.max(data, d => d[yKey] + d[errorKey]);
  const y = d3.scaleLinear()
    .domain([0, yMax]).nice()
    .range([innerHeight, 0]);

  g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x));
  g.append('g').call(d3.axisLeft(y));

  // Bars
  g.selectAll('.bar')
    .data(data)
    .join('rect')
    .attr('x', d => x(d[xKey]))
    .attr('y', d => y(d[yKey]))
    .attr('width', x.bandwidth())
    .attr('height', d => innerHeight - y(d[yKey]))
    .attr('fill', '#3b82f6');

  // Error bars
  data.forEach(d => {
    const cx = x(d[xKey]) + x.bandwidth() / 2;
    const capWidth = x.bandwidth() / 4;

    // Vertical line
    g.append('line')
      .attr('x1', cx).attr('x2', cx)
      .attr('y1', y(d[yKey] - d[errorKey]))
      .attr('y2', y(d[yKey] + d[errorKey]))
      .attr('stroke', '#1f2937')
      .attr('stroke-width', 1.5);

    // Caps
    [d[yKey] - d[errorKey], d[yKey] + d[errorKey]].forEach(val => {
      g.append('line')
        .attr('x1', cx - capWidth).attr('x2', cx + capWidth)
        .attr('y1', y(val)).attr('y2', y(val))
        .attr('stroke', '#1f2937')
        .attr('stroke-width', 1.5);
    });
  });
}
```

## Confidence Interval Band

Show uncertainty around a trend line.

```javascript
function confidenceBand(container, data, { xKey, yKey, lowerKey, upperKey }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d[xKey]))
    .range([0, innerWidth]);

  const y = d3.scaleLinear()
    .domain([
      d3.min(data, d => d[lowerKey]),
      d3.max(data, d => d[upperKey])
    ]).nice()
    .range([innerHeight, 0]);

  // Confidence band (area)
  const area = d3.area()
    .x(d => x(d[xKey]))
    .y0(d => y(d[lowerKey]))
    .y1(d => y(d[upperKey]))
    .curve(d3.curveMonotoneX);

  g.append('path')
    .datum(data)
    .attr('fill', '#3b82f6')
    .attr('fill-opacity', 0.2)
    .attr('d', area);

  // Center line
  const line = d3.line()
    .x(d => x(d[xKey]))
    .y(d => y(d[yKey]))
    .curve(d3.curveMonotoneX);

  g.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', '#3b82f6')
    .attr('stroke-width', 2)
    .attr('d', line);

  g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x));
  g.append('g').call(d3.axisLeft(y));
}
```

## Histogram

Show distribution of continuous variable.

```javascript
function histogram(container, values, { bins = 20, color = '#3b82f6' } = {}) {
  const { g, innerWidth, innerHeight } = createChart(container, values);

  const x = d3.scaleLinear()
    .domain(d3.extent(values)).nice()
    .range([0, innerWidth]);

  const binGenerator = d3.bin()
    .domain(x.domain())
    .thresholds(x.ticks(bins));

  const binnedData = binGenerator(values);

  const y = d3.scaleLinear()
    .domain([0, d3.max(binnedData, d => d.length)]).nice()
    .range([innerHeight, 0]);

  g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x));
  g.append('g').call(d3.axisLeft(y));

  g.selectAll('.bar')
    .data(binnedData)
    .join('rect')
    .attr('x', d => x(d.x0) + 1)
    .attr('y', d => y(d.length))
    .attr('width', d => Math.max(0, x(d.x1) - x(d.x0) - 2))
    .attr('height', d => innerHeight - y(d.length))
    .attr('fill', color);
}
```

## Violin Plot (with D3)

Combines box plot with density estimation.

```javascript
function violinPlot(container, data, { groupKey, valueKey }) {
  const { g, innerWidth, innerHeight } = createChart(container, data);

  const groups = d3.group(data, d => d[groupKey]);
  const groupNames = Array.from(groups.keys());

  const x = d3.scaleBand()
    .domain(groupNames)
    .range([0, innerWidth])
    .padding(0.1);

  const allValues = data.map(d => d[valueKey]);
  const y = d3.scaleLinear()
    .domain(d3.extent(allValues)).nice()
    .range([innerHeight, 0]);

  g.append('g').attr('transform', `translate(0,${innerHeight})`).call(d3.axisBottom(x));
  g.append('g').call(d3.axisLeft(y));

  groups.forEach((values, key) => {
    const nums = values.map(d => d[valueKey]);

    // Kernel density estimation
    const kde = kernelDensityEstimator(kernelEpanechnikov(7), y.ticks(50));
    const density = kde(nums);

    const maxDensity = d3.max(density, d => d[1]);
    const violinWidth = d3.scaleLinear()
      .domain([0, maxDensity])
      .range([0, x.bandwidth() / 2]);

    const area = d3.area()
      .x0(d => x(key) + x.bandwidth() / 2 - violinWidth(d[1]))
      .x1(d => x(key) + x.bandwidth() / 2 + violinWidth(d[1]))
      .y(d => y(d[0]))
      .curve(d3.curveCatmullRom);

    g.append('path')
      .datum(density)
      .attr('fill', '#3b82f6')
      .attr('fill-opacity', 0.7)
      .attr('stroke', '#1e40af')
      .attr('d', area);
  });
}

// KDE helpers
function kernelDensityEstimator(kernel, X) {
  return V => X.map(x => [x, d3.mean(V, v => kernel(x - v))]);
}

function kernelEpanechnikov(k) {
  return v => Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
}
```

## When to Use Each

| Visualization | Use When |
|---------------|----------|
| **Box plot** | Compare distributions across groups; show median, spread, outliers |
| **Violin plot** | Show full distribution shape; compare multiple groups |
| **Histogram** | Show distribution of single continuous variable |
| **Error bars** | Show uncertainty/variability around point estimates |
| **Confidence band** | Show uncertainty around a trend or regression line |
| **Density plot** | Smooth alternative to histogram |
