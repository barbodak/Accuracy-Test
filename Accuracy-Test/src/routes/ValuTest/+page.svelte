<script lang="ts">
    import { writable } from "svelte/store";
    import Layout from "../+layout.svelte";
    import ValCard from "../../components/ValCard.svelte";
    import Page from "../+page.svelte";
    let answers = Array(20)
        .fill(-1)
        .map((x, i) => -1 * i);
    let cardWasUsed = Array(20).fill(false);
    let txt = "no touching yet";
    let hoveringOver = 90;
    let isOverlayOpen = false;

    function handleDragStart(event: DragEvent, cardIndex: number) {
        event.dataTransfer?.setData("cardName", cardIndex.toString());
    }
    function handleDrop(event: any, dropZoneIndex: number) {
        event.preventDefault();
        const cardIndex = parseInt(event.dataTransfer.getData("cardName"));
        cardWasUsed[cardIndex] = true;
        if (answers[dropZoneIndex] < 0) {
            // Remove the item from one basket.
            // Splice returns an array of the deleted elements, just one in this case.
            answers.map((x, i) => {
                if (x === cardIndex) {
                    answers[i] = -1 * i;
                }
            });
            answers[dropZoneIndex] = cardIndex;
        } else {
            // swaping
            let tmp = answers[dropZoneIndex];
            answers[dropZoneIndex] = -100;
            answers.forEach((x, i) => {
                if (x === cardIndex) {
                    answers[i] = tmp;
                }
            });
            answers[dropZoneIndex] = cardIndex;
        }
        hoveringOver = 100;
    }

    import { tweened } from "svelte/motion";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Overlay from "../../components/Overlay.svelte";
    import Question from "../../components/Question.svelte";
    let number = 30;
    let cnt = 0;

    onMount(async () => {
        const quiz = await retreiveQuiz({ quiz_type: "ValuTest" });
        if (quiz.quiz_info == "not_started") {
            console.log("not started");
            goto("/");
        }
        answers = quiz.answers.map((x: any) => x - 1);
        answers = answers.slice(0, 20);
        answers.forEach((x: any, i: any) => {
            if (x >= 0) {
                cardWasUsed[x] = true;
            }
        });
    });
    let submit_promise: Promise<void>;
    function handleSubmit() {
        // just because you feel it doesn't mean it's there
        // tupac
        let ans = answers.map((x) => x + 1);
        submit_promise = submitAnswer({
            answers: ans,
            quiz_type: "ValuTest",
        });
    }

    // Force UI update if needed (though this should generally not be necessary)
</script>

<header class="fixed top-0 w-full bg-blue-900 text-white z-10">
    <nav class="container mx-auto px-6 py-3">
        <div class="flex justify-between items-center">
            <div class="text-lg font-semibold">Values Test</div>
            <div class="space-x-4 lg:order-2">
                <!-- Swapped order for large screens -->
                <button
                    class="px-4 py-2 bg-red-700 hover:bg-red-800 rounded-lg focus:outline-none"
                    on:click={() => {
                        handleSubmit();
                        isOverlayOpen = true;
                    }}
                >
                    End Test
                </button>
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
                    <div class="mx-5 my-7">
                        <ValCard
                            id={index}
                            on:dragstart={(event) =>
                                handleDragStart(event, index)}
                        />
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
                {#each answers as answer, index (answer)}
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
                        {#if answers[index] < 0}{:else}
                            <ValCard
                                id={answers[index]}
                                on:dragstart={(event) =>
                                    handleDragStart(event, answers[index])}
                                on:click={() => {
                                    cardWasUsed[answers[index]] = false;
                                    answers[index] = -1 * index;
                                }}
                            />
                        {/if}
                    </div>
                {/each}
            </div>
        </div>
    </div>
</body>

{#if isOverlayOpen}
    <Overlay canBeExited={false} isTransparent={true}>
        <p>
            are you sure you want to end this test? your answers are
            automatically saved and you can edit your answers until the time
            ends
        </p>
        <button
            class="bg-red-600 hover:bg-red-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
            on:click={() => {
                goto("/TestEnded");
            }}
            >End Test
        </button>
        <button
            class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
            on:click={() => {
                isOverlayOpen = false;
            }}
        >
            Continue Test</button
        >
    </Overlay>
{/if}
