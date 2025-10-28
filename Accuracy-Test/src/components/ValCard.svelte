<script lang="ts">
    import { cardData } from "$lib/card-data";
    import { createEventDispatcher } from "svelte";

    export let id: number;
    $: card = cardData[id];

    const dispatch = createEventDispatcher();
</script>

<div
    class="w-full h-full flex flex-col bg-white rounded-lg shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-200 overflow-hidden border border-slate-200 select-none relative group"
>
    <button
        on:click|stopPropagation={() => dispatch("remove")}
        class="remove-button"
        aria-label="Remove card"
    >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
            ><line x1="18" y1="6" x2="6" y2="18"></line><line
                x1="6"
                y1="6"
                x2="18"
                y2="18"
            ></line></svg
        >
    </button>

    <div class="card-letter-section bg-slate-50">
        <span
            class="card-letter text-slate-700"
            style="text-shadow: 1px 1px 3px rgba(0,0,0,0.1);"
        >
            {card.letter}
        </span>
    </div>

    <div class="h-px bg-slate-200"></div>

    <div class="card-content">
        <p class="card-prompt text-slate-500">
            {card.prompt}
        </p>
        <p class="card-text font-semibold text-slate-800">
            {card.text}
        </p>
    </div>
</div>

<style>
    /* 'cqi' stands for "container query inline-size".
      1cqi = 1% of the container's width.
      This makes all our spacing and fonts perfectly fluid!
    */

    .card-letter-section {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        /* Replaces pt-2 pb-1 */
        padding-top: 2cqi;
        padding-bottom: 1cqi;
    }

    .card-letter {
        font-weight: 700;
        /* Replaces text-4xl sm:text-5xl */
        font-size: 10cqi;
        line-height: 1;
    }

    .card-content {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        /* Replaces p-4 */
        padding: 4cqi;
    }

    .card-prompt {
        /* Replaces text-xs sm:text-sm mb-3 */
        font-size: 4cqi;
        line-height: 1.3;
        margin-bottom: 2cqi;
    }

    .card-text {
        /* Replaces text-sm sm:text-base */
        font-size: 6cqi;
        line-height: 1.4;
    }

    .remove-button {
        position: absolute;
        /* Replaces top-1 right-1 */
        top: 2cqi;
        right: 2cqi;
        z-index: 10;
        /* Replaces w-6 h-6 */
        width: 5cqi;
        height: 5cqi;

        background-color: #ef4444; /* red-500 */
        color: white;
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;

        opacity: 0;
        transition: all 0.2s;
    }

    /* Recreates the group-hover:opacity-100 */
    .group:hover .remove-button {
        opacity: 1;
    }

    .remove-button:hover {
        background-color: #dc2626; /* red-600 */
    }

    .remove-button svg {
        /* Scale the SVG icon relative to the button */
        width: 60%;
        height: 60%;
    }

    /* --- THIS IS THE RESPONSIVE MAGIC ---
      If the container named 'val-card' is ever less than 100px wide,
      these styles will automatically apply.
    */
    @container val-card (max-width: 100px) {
        .card-prompt {
            /* On very small cards, hide the prompt text */
            display: none;
        }

        .card-letter {
            /* Make the letter a bit smaller */
            font-size: 14cqi;
        }

        .card-text {
            /* Make the main text a bit smaller */
            font-size: 3.5cqi;
        }

        .card-content {
            /* Reduce padding to give text more space */
            padding: 2.5cqi;
        }
    }
</style>
