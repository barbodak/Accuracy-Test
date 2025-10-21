<script lang="ts">
    export let selected: "S" | "D" | "0" = "0";
    export let number: number;
    export let text1: string;
    export let text2: string;

    const selection = (option: "S" | "D") => {
        selected = selected === option ? "0" : option;
    };
</script>

<div
    class="select-none bg-white rounded-lg overflow-hidden p-4 sm:p-6 transition-shadow hover:shadow-lg"
>
    <div class="flex w-full items-center justify-between gap-3 sm:gap-4">
        <div class="flex h-24 flex-1 items-center justify-end p-3">
            <p class="font-mono text-right text-lg text-slate-700">{text1}</p>
        </div>

        <div class="flex flex-row gap-3">
            <button
                on:click={() => selection("S")}
                class="flex h-12 w-12 items-center justify-center rounded-md border-2 text-2xl font-semibold transition-all duration-200 focus:outline-none focus-visible:ring-4 focus-visible:ring-offset-2 focus-visible:ring-green-300"
                class:border-green-500={selected === "S"}
                class:text-green-700={selected === "S"}
                class:bg-green-100={selected === "S"}
                class:border-slate-300={selected !== "S"}
                class:text-slate-500={selected !== "S"}
                class:hover:border-green-400={selected !== "S"}
                class:hover:bg-green-50={selected !== "S"}
                aria-label="Mark as Same"
            >
                ✓
            </button>

            <button
                on:click={() => selection("D")}
                class="flex h-12 w-12 items-center justify-center rounded-md border-2 text-2xl font-semibold transition-all duration-200 focus:outline-none focus-visible:ring-4 focus-visible:ring-offset-2 focus-visible:ring-red-300"
                class:border-red-500={selected === "D"}
                class:text-red-700={selected === "D"}
                class:bg-red-100={selected === "D"}
                class:border-slate-300={selected !== "D"}
                class:text-slate-500={selected !== "D"}
                class:hover:border-red-400={selected !== "D"}
                class:hover:bg-red-50={selected !== "D"}
                aria-label="Mark as Different"
            >
                ✗
            </button>
        </div>

        <div class="flex h-24 flex-1 items-center justify-start p-3">
            <p class="font-mono text-left text-lg text-slate-700">{text2}</p>
        </div>
    </div>
</div>
