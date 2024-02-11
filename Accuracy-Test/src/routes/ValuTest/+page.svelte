<script lang="ts">
    import ValCard from "../../components/ValCard.svelte";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Overlay from "../../components/Overlay.svelte";

    function shuffle(array: Array<any>) {
        let currentIndex = array.length,
            randomIndex;

        // While there remain elements to shuffle.
        while (currentIndex > 0) {
            // Pick a remaining element.
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;

            // And swap it with the current element.
            [array[currentIndex], array[randomIndex]] = [
                array[randomIndex],
                array[currentIndex],
            ];
        }

        return array;
    }

    let answers = Array(20)
        .fill(-1)
        .map((x, i) => -1 * (i + 1));
    let cardWasUsed = Array(20).fill(false);
    let hoveringOver = 90;
    let isOverlayOpen = false;
    let cardOrder = shuffle(
        Array(20)
            .fill(0)
            .map((x, i) => i)
    );

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
                    answers[i] = -1 * (i + 1);
                }
            });
            answers[dropZoneIndex] = cardIndex;
        } else {
            // swaping
            let wasDroped = false;
            let tmp = answers[dropZoneIndex];
            answers[dropZoneIndex] = -100;
            answers.forEach((x, i) => {
                if (x === cardIndex) {
                    answers[i] = tmp;
                    wasDroped = true;
                }
            });
            answers[dropZoneIndex] = cardIndex;
            if (wasDroped === false && tmp !== cardIndex)
                cardWasUsed[tmp] = false;
        }
        hoveringOver = 100;
    }
    function hasFilledEverything() {
        return cardWasUsed.every((x) => x === true);
    }

    onMount(async () => {
        const quiz = await retreiveQuiz({ quiz_type: "ValuTest" });
        if (quiz.quiz_info == "not_started") {
            console.log("not started");
            goto("/");
        }
        {
            let i = 0;
            for (let q of quiz.answers) {
                if (i < 20 && q > 0) answers[i] = q - 1;
                i++;
            }
        }
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
        let ans = answers.map((x) => Math.max(x + 1, 0));
        submit_promise = submitAnswer({
            answers: ans,
            quiz_type: "ValuTest",
        });
    }

    // Force UI update if needed (though this should generally not be necessary)
</script>

<header class="fixed top-0 w-full bg-blue-950 text-white z-5">
    <nav class="container mx-auto px-6 py-3">
        <div class="flex justify-between items-center">
            <div class="text-lg font-semibold">W.I.L. آزمون</div>
            <div class="space-x-4 lg:order-2">
                <!-- Swapped order for large screens -->
                <button
                    class="px-4 py-2 bg-red-700 hover:bg-red-800 rounded-lg focus:outline-none"
                    on:click={() => {
                        handleSubmit();
                        isOverlayOpen = true;
                    }}
                >
                    پایان آزمون
                </button>
            </div>
        </div>
    </nav>
</header>

<body>
    <div class="flex mt-16">
        <!-- mt-16 to push down content below the fixed header -->

        <!-- Blue Sidebar -->
        <div class="w-1/5 h-screen fixed right-0 bg-black overflow-auto z-0">
            {#each cardOrder as card}
                {#if cardWasUsed[card] === false}
                    <div class="mx-5 my-7">
                        <ValCard
                            id={card}
                            on:dragstart={(event) =>
                                handleDragStart(event, card)}
                        />
                    </div>
                {/if}
            {/each}
            <!-- Sidebar content goes here -->
        </div>

        <div class="w-4/5 h-screen pl-1/5">
            <br />
            <img
                class="pb-5 px-10"
                src="/images/quiz/importance_label.png"
                alt="importance_label"
            />
            <div class="grid grid-cols-5 grid-rows-1 gap-x-9 px-5">
                {#each Array(5) as a, index}
                    <div
                        class="border-2 border-solid rounded-md text-center place-items-center border-black bg-black text-white"
                    >
                        ستون {index == 0
                            ? "اول"
                            : index == 1
                            ? "دوم"
                            : index == 2
                            ? "سوم"
                            : index == 3
                            ? "چهارم"
                            : "پنجم"}
                    </div>
                {/each}
            </div>
            <div class="grid grid-cols-5 grid-rows-4 gap-x-9 gap-y-6 h-5/6 p-5">
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
                        role="button"
                        tabindex="0"
                    >
                        {#if answers[index] < 0}
                            <div />
                        {:else}
                            <ValCard
                                id={answers[index]}
                                on:dragstart={(event) =>
                                    handleDragStart(event, answers[index])}
                                on:click={() => {
                                    cardWasUsed[answers[index]] = false;
                                    answers[index] = -1 * (index + 1);
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
        {#if hasFilledEverything()}
            <p>آیا مطمئن هستید که می‌خواهید آزمون را تمام کنید؟</p>
            <button
                class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
                on:click={() => {
                    isOverlayOpen = false;
                }}
            >
                ادامه آزمون
            </button>
            <button
                class="bg-red-600 hover:bg-red-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
                on:click={() => {
                    goto("/TestEnded");
                }}
                >پایان آزمون
            </button>
        {:else}
            <p>لطفا پیش از اتمام آزمون تمامی خانه‌ها را پر کنید</p>
            <button
                class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
                on:click={() => {
                    isOverlayOpen = false;
                }}
            >
                ادامه آزمون
            </button>
        {/if}
    </Overlay>
{/if}
