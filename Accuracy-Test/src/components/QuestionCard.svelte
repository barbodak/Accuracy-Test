<script lang="ts">
    import { fly } from "svelte/transition";
    export let question;
    export let animDiraction: number;
    export let choices; // Array of { score: number, text: string } passed from parent
    export let selectedScore: number | undefined;
    export let onSelect: (score: number) => void;
    export let onPrev: () => void;
    export let onNext: () => void;
    export let canAdvance: boolean;
    console.log(question);

    function handleKeydown(event: KeyboardEvent) {
        const key = event.key;

        const matchedChoice = choices.find((c) => c.score.toString() === key);

        if (matchedChoice) {
            onSelect(matchedChoice.score);
        } else if (key === "ArrowLeft" || key === "Enter") {
            if (canAdvance) onNext();
        } else if (key === "ArrowRight") {
            onPrev();
        }
    }
    const circleColors = [
        "#fecdd3",
        "#fce7f3",
        "#f1f5f9",
        "#dcfce7",
        "#bbf7d0",
    ];
</script>

<svelte:window on:keydown={handleKeydown} />

<div
    class="bg-white/95 backdrop-blur-md px-8 py-10 rounded-[24px] text-center shadow-[0_20px_40px_rgba(0,0,0,0.08)]"
    in:fly={{ x: -300 * animDiraction, duration: 300, delay: 300 }}
    out:fly={{ x: 300 * animDiraction, duration: 300 }}
>
    <h2 class="text-[1.4rem] text-slate-900 mb-10 font-bold">{question}</h2>

    <div
        class="flex flex-col sm:flex-row-reverse sm:flex-nowrap justify-center items-center gap-4 sm:gap-6 w-full"
    >
        {#each choices as choice}
            <!-- 
          flex-row (mobile): items sit side-by-side
          sm:flex-col (desktop): items stack vertically 
        -->
            <button
                class="group flex flex-row sm:flex-col items-center gap-4 sm:gap-3 w-full sm:w-20 cursor-pointer shrink-0"
                on:click={() => onSelect(choice.score)}
            >
                <!-- Circular Button -->
                <div
                    class="w-[50px] h-[50px] sm:w-[60px] sm:h-[60px] rounded-full border-4 flex items-center justify-center transition-all duration-200 ease-in-out group-hover:scale-[1.15] group-hover:shadow-[0_8px_15px_rgba(0,0,0,0.15)] shrink-0"
                    class:border-slate-700={selectedScore === choice.score}
                    class:scale-[1.15]={selectedScore === choice.score}
                    class:shadow-[0_6px_15px_rgba(0,0,0,0.2)]={selectedScore ===
                        choice.score}
                    class:border-white={selectedScore !== choice.score}
                    class:shadow-md={selectedScore !== choice.score}
                    style="background-color: {circleColors[choice.score - 1] ||
                        '#f1f5f9'};"
                >
                    <div class="text-[0.9rem] text-slate-700 font-semibold">
                        {#if selectedScore === choice.score}✔{/if}
                    </div>
                </div>

                <span
                    class="text-[0.9rem] text-slate-700 font-semibold transition-all duration-200 ease-in-out group-hover:text-slate-900 group-hover:scale-110 sm:group-hover:translate-y-0.5 text-left sm:text-center leading-tight flex-1"
                    class:!text-slate-900={selectedScore === choice.score}
                    class:!font-extrabold={selectedScore === choice.score}
                >
                    {choice.text}
                </span>
            </button>
        {/each}
    </div>
</div>
