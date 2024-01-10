<h1>Hello World</h1>
<svg width="3000" height="1000">

    <defs>
        <marker id="arrow" markerWidth="13" markerHeight="13" refy="6" orient="auto">
            <path d="M2,2 L2,11 L10,6 L2,2" style="fill:red;" />
        </marker>
    </defs>

    <path d="M30,150 L100,50"
          style="stroke:red; stroke-width: 1.25px; fill: none;
                 marker-end: url(#arrow);"
    />

</svg>
