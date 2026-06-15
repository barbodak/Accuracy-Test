<script lang="ts">
    import { fly } from "svelte/transition";

    export let timeInSeconds: number = 0;

    $: minutes = Math.floor(timeInSeconds / 60).toString().padStart(2, "0");
    $: seconds = Math.floor(timeInSeconds % 60).toString().padStart(2, "0");
    $: formattedTime = `${minutes}:${seconds}`;
</script>

<div 
    class="inline-flex items-center gap-3 bg-white px-5 py-2 rounded-full border border-slate-100 shadow-[0_2px_10px_rgba(0,0,0,0.03)]" 
    dir="ltr"
>
    <!-- Digits Container -->
    <div class="flex items-center text-lg font-bold font-mono text-slate-800">
        {#each formattedTime.split('') as char, i}
            {#if char === ':'}
                <!-- Subtle colon -->
                <span class="text-slate-300 mx-0.5 pb-0.5">:</span>
            {:else}
                <!-- 
                  Invisible bounding box for each digit. 
                  This creates the "window" for the slide animation without adding harsh shapes. 
                -->
                <div class="relative flex h-7 w-3.5 items-center justify-center overflow-hidden">
                    {#key char}
                        <span 
                            class="absolute" 
                            in:fly={{ y: -15, duration: 300 }} 
                            out:fly={{ y: 15, duration: 300 }}
                        >
                            {char}
                        </span>
                    {/key}
                </div>
            {/if}
        {/each}
    </div>

    <!-- Clock Icon (Smaller and softer color to match the new size) -->
    <svg
        class="text-slate-400"
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
    >
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
</div>

