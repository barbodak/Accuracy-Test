<script lang="ts">
    import { fly } from "svelte/transition";
    export let current: number;
    export let total: number;
</script>

<div class="progress-glass-pill">
    {#key current}
        <span class="animated-number" in:fly={{ y: -10, duration: 300 }}>
            {current}
        </span>
    {/key}
    <span class="divider">از</span>
    <span class="total-number">{total}</span>
</div>

<style>
    .progress-glass-pill {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px);
        padding: 0.6rem 1.8rem;
        border-radius: 50px;
        border: 2px solid rgba(255, 255, 255, 0.7);
        font-size: 1.3rem;
        font-weight: 800;
        color: #2d3748;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .animated-number {
        color: #c53030; /* The dark red from your original screenshot */
        display: inline-block;
    }
    .divider,
    .total-number {
        color: #4a5568;
    }
</style>
