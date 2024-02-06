<div class="arrow" />

<!-- Arrow.svelte -->
<style>
    .arrow {
        position: relative;
        height: 4px; /* Thickness of the arrow line */
        background-color: black;
    }

    .arrow::before,
    .arrow::after {
        content: "";
        position: absolute;
        top: 50%;
        border-style: solid;
        border-color: black;
        border-width: 8px 8px 0 8px; /* Size of the arrowheads */
        transform: translateY(-50%);
    }

    .arrow::before {
        left: 0; /* Arrow point on the left */
        transform: translateY(-50%) rotate(225deg);
    }

    .arrow::after {
        right: 0; /* Arrow point on the right */
        transform: translateY(-50%) rotate(45deg);
    }
</style>

