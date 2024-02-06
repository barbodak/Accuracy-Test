<script lang="ts">
    import { writable } from "svelte/store";
    import Layout from "../+layout.svelte";
    import ValCard from "../../components/ValCard.svelte";
    import Page from "../+page.svelte";
    let answers = Array(20).fill(-1);
    let cardWasUsed = Array(20).fill(false);
    let txt = "no touching yet";
    let hoveringOver = 90;

    export let direction: "left" | "right" = "right";

    function handleDragStart(event: DragEvent, cardIndex: number) {
        event.dataTransfer?.setData("cardName", cardIndex.toString());
    }
    function handleDrop(event: any, dropZoneIndex: number) {
        event.preventDefault();
        if (answers[dropZoneIndex] === -1) {
            const cardIndex = parseInt(event.dataTransfer.getData("cardName"));
            txt = cardIndex.toString();
            // Remove the item from one basket.
            // Splice returns an array of the deleted elements, just one in this case.
            cardWasUsed[cardIndex] = true;
            answers[dropZoneIndex] = 0;
            answers[dropZoneIndex] = cardIndex;
            hoveringOver = 100;
        }
    }

    import { tweened } from "svelte/motion";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    let number = 30;
    let cnt = 0;
    let timer: any;
    let ti = 0;

    onMount(async () => {
        const quiz = await retreiveQuiz({ quiz_type: "ValuTest" });
        answers = quiz.answers.map((x: any) => x - 1);
        answers = answers.slice(0, 20);
        answers.forEach((x: any, i: any) => {
            if (x !== -1) {
                cardWasUsed[x] = true;
            }
        });
        let now = new Date();
        let qdate = new Date(quiz.quiz_info);
        let delta = now.valueOf() - qdate.valueOf();
        ti = Math.floor(delta / 1000);
        timer = tweened(5 * 60 - ti);
        console.log(timer);
        console.log("f");
    });
    setInterval(() => {
        if ($timer > -2) $timer--;
    }, 1000);

    let submit_promise: Promise<void>;
    function handleSubmit() {
        // just because you feel it doesn't mean it's there
        // tupac
        let ans = answers.map((x) => x + 1);
        console.log(ans);
        submit_promise = submitAnswer({
            answers: ans,
            quiz_type: "ValuTest",
        });
    }
    $: minutes = Math.floor($timer / 60);
    $: seconds = Math.floor($timer - minutes * 60);
    $: {
        if (seconds == 0) handleSubmit();
    }
    $: {
        if (seconds == 0 && minutes == 0) {
            handleSubmit();
            console.log("submitting");
        }
    }
    $: {
        if (seconds < 0 || minutes < 0) {
            goto("/TestEnded");
        }
    }
</script>

<header class="fixed top-0 w-full bg-blue-900 text-white z-10">
    <nav class="container mx-auto px-6 py-3">
        <div class="flex justify-between items-center">
            <div class="text-lg font-semibold">Values Test</div>
            <div class="space-x-4 lg:order-2">
                <!-- Swapped order for large screens -->
                <button
                    class="px-4 py-2 bg-red-700 hover:bg-red-800 rounded-lg focus:outline-none"
                    on:click={handleSubmit}
                >
                    End Test
                </button>
            </div>
            <div class="space-x-4 lg:flex lg:w-auto lg:order-1">
                <!-- Swapped order for large screens -->
                <p
                    class="text-white p-3 rounded-3xl border-white border-2 text-lg"
                >
                    {minutes + " : " + seconds}
                </p>
            </div>
        </div>
    </nav>
</header>

<body>
    <div class="flex mt-16">
        <!-- mt-16 to push down content below the fixed header -->

        <!-- Blue Sidebar -->
        <div class="w-1/5 h-screen fixed right-0 bg-blue-950 overflow-auto z-0">
            {#each cardWasUsed as card, index}
                {#if card === false}
                    <div
                        class="mx-5 my-7"
                        draggable={true}
                        on:dragstart={(event) => handleDragStart(event, index)}
                    >
                        <ValCard id={index} />
                    </div>
                {/if}
            {/each}
            <!-- Sidebar content goes here -->
        </div>

        <!-- Orange Main Content -->
        <div class="w-4/5 h-screen pl-1/5">
            <br />
            <div
                class="grid grid-cols-5 grid-rows-4 gap-x-5 gap-y-6 h-screen p-5"
            >
                {#each answers as answer, index}
                    <div
                        class={"border-2 border-solid rounded-md text-center place-items-center " +
                            (hoveringOver === index
                                ? "border-orange-600"
                                : "border-black")}
                        on:dragenter={() => (hoveringOver = index)}
                        on:dragleave={() => (hoveringOver = 100)}
                        on:drop={(event) => handleDrop(event, index)}
                        on:dragover={(ev) => {
                            ev.preventDefault();
                        }}
                    >
                        {#if answers[index] === -1}{:else}
                            <div
                                class="h-full w-full flex justify-center items-center"
                            >
                                <ValCard
                                    id={answers[index]}
                                    on:click={() => {
                                        cardWasUsed[answers[index]] = false;
                                        answers[index] = -1;
                                    }}
                                />
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>
        </div>
    </div>
</body>
