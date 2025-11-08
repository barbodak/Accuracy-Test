<script lang="ts">
    import ValCardComponent from "$lib/../components/ValCard.svelte";
    import Overlay from "$lib/../components/Overlay.svelte";
    import ImportanceArrow from "$lib/../components/Arrow.svelte";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    // --- State Management ---
    let answers = Array(20)
        .fill(0)
        .map((_, i) => -(i + 1));
    let cardWasUsed = Array(20).fill(false);
    let cardOrder = shuffle(Array.from({ length: 20 }, (_, i) => i));

    let hoveringOver = -1;
    let isOverlayOpen = false;
    let submit_promise: Promise<void>;

    // State for the new interaction model
    let selectedCardIndex: number | null = null;
    let selectedCardOriginalSlot: number | null = null;

    $: usedCardsCnt = cardWasUsed.reduce(
        (acc: number, curr: boolean) => (curr ? acc + 1 : acc),
        0,
    );

    // --- Lifecycle ---
    onMount(async () => {
        const quiz = await retreiveQuiz({ quiz_type: "ValuTest" });
        if (quiz.quiz_time == "not_started") {
            console.log("Quiz has not started, redirecting.");
            goto("/");
        }
        if (quiz.answers && quiz.answers.length > 0) {
            quiz.answers.forEach((q: number, i: number) => {
                if (i < 20 && q > 0) {
                    const cardId = q - 1;
                    answers[i] = cardId;
                    cardWasUsed[cardId] = true;
                }
            });
        }
    });

    function shuffle(array: any[]) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    function hasFilledEverything() {
        return cardWasUsed.every((x) => x === true);
    }

    function handleDragStart(event: DragEvent, cardIndex: number) {
        event.dataTransfer?.setData("cardIndex", cardIndex.toString());
        selectedCardIndex = null;
        selectedCardOriginalSlot = null;
    }

    function handleDrop(event: DragEvent, dropZoneIndex: number) {
        event.preventDefault();
        const cardIndex = parseInt(
            event.dataTransfer?.getData("cardIndex") || "-1",
        );
        if (cardIndex >= 0) {
            // A simplified placement logic for drag-and-drop
            const cardToDisplace = answers[dropZoneIndex];
            const originalSlot = answers.indexOf(cardIndex);

            answers[dropZoneIndex] = cardIndex;
            cardWasUsed[cardIndex] = true;

            if (originalSlot !== -1) {
                answers[originalSlot] = cardToDisplace;
            } else if (cardToDisplace >= 0) {
                cardWasUsed[cardToDisplace] = false;
            }
        }
        hoveringOver = -1;
    }

    function handleCardSelectInTray(cardIndex: number) {
        if (selectedCardIndex === cardIndex) {
            selectedCardIndex = null;
            selectedCardOriginalSlot = null;
        } else {
            selectedCardIndex = cardIndex;
            selectedCardOriginalSlot = null;
        }
    }

    function handleSlotClick(slotIndex: number) {
        // Case 1: A card is selected (from tray or grid)
        if (selectedCardIndex !== null) {
            const cardToDisplace = answers[slotIndex];

            answers[slotIndex] = selectedCardIndex;
            cardWasUsed[selectedCardIndex] = true;

            // If the selected card came from the grid, perform a swap
            if (selectedCardOriginalSlot !== null) {
                console.log(
                    selectedCardOriginalSlot,
                    cardToDisplace,
                    slotIndex,
                    answers[slotIndex],
                    answers,
                );
                answers[selectedCardOriginalSlot] = cardToDisplace;
                // if (cardToDisplace < 0) {
                //     // If swapping into an empty slot, ensure the original card is used
                //     const originalCard = cardData[selectedCardIndex];
                cardWasUsed[selectedCardIndex] = true;
                // }
            }
            // If the selected card came from the tray and displaced another card
            else if (cardToDisplace >= 0) {
                cardWasUsed[cardToDisplace] = false;
            }

            // Clear selection
            selectedCardIndex = null;
            selectedCardOriginalSlot = null;
            console.log("stuff");
        }
        // Case 2: No card is selected, so we are picking one up from the grid
        else {
            const cardInSlot = answers[slotIndex];
            if (cardInSlot >= 0) {
                selectedCardIndex = cardInSlot;
                selectedCardOriginalSlot = slotIndex;
            }
        }
    }

    function handleRemoveFromGrid(slotIndex: number) {
        const cardIdToRemove = answers[slotIndex];
        if (slotIndex == selectedCardOriginalSlot) {
            selectedCardIndex = null;
            selectedCardOriginalSlot = null;
        }
        if (cardIdToRemove >= 0) {
            cardWasUsed[cardIdToRemove] = false;
            answers[slotIndex] = -(slotIndex + 1); // Reset slot to empty
        }
    }

    function handleSubmit() {
        isOverlayOpen = true;
        if (hasFilledEverything()) {
            let ans = answers.map((x) => Math.max(x + 1, 0));
            submit_promise = submitAnswer({
                answers: ans,
                quiz_type: "ValuTest",
            });
        }
    }
</script>

<div
    class="bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 h-screen font-sans flex flex-col overflow-hidden"
>
    <!-- Header -->

    <!-- Main Layout -->
    <div class="flex flex-1 min-h-0">
        <!-- Main Content Grid -->
        <main class="flex-1 flex flex-col p-4 sm:p-6 min-w-0">
            <div class="mb-4">
                <ImportanceArrow />
            </div>

            <div class="grid grid-cols-5 gap-2 sm:gap-4 mb-2 px-2">
                <div
                    class="text-center font-bold text-slate-600 dark:text-slate-300"
                >
                    ستون ۱
                </div>
                <div
                    class="text-center font-bold text-slate-600 dark:text-slate-300"
                >
                    ستون ۲
                </div>
                <div
                    class="text-center font-bold text-slate-600 dark:text-slate-300"
                >
                    ستون ۳
                </div>
                <div
                    class="text-center font-bold text-slate-600 dark:text-slate-300"
                >
                    ستون ۴
                </div>
                <div
                    class="text-center font-bold text-slate-600 dark:text-slate-300"
                >
                    ستون ۵
                </div>
            </div>

            <!-- Responsive Card Grid -->
            <div class="flex-1 grid grid-cols-5 grid-rows-4 gap-2 sm:gap-4">
                {#each answers as answer, index}
                    <div
                        class="rounded-lg transition-all duration-200 flex items-center justify-center"
                        class:border-dashed={answer < 0}
                        class:border-2={answer < 0}
                        class:border-slate-300={hoveringOver !== index &&
                            answer < 0}
                        class:dark:border-slate-600={hoveringOver !== index &&
                            answer < 0}
                        class:border-indigo-500={hoveringOver === index}
                        class:ring-4={selectedCardOriginalSlot === index}
                        class:ring-indigo-400={selectedCardOriginalSlot ===
                            index}
                        class:cursor-pointer={true}
                        class:hover:border-indigo-400={selectedCardIndex !==
                            null && answer < 0}
                        on:dragenter|preventDefault={() =>
                            (hoveringOver = index)}
                        on:dragleave|preventDefault={() => (hoveringOver = -1)}
                        on:drop|preventDefault={(event) =>
                            handleDrop(event, index)}
                        on:dragover|preventDefault
                        on:click={() => handleSlotClick(index)}
                        role="button"
                        tabindex="0"
                    >
                        {#if selectedCardIndex !== null && answer < 0}
                            <div class="text-slate-300 dark:text-slate-600">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="48"
                                    height="48"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    ><line x1="12" y1="5" x2="12" y2="19"
                                    ></line><line x1="5" y1="12" x2="19" y2="12"
                                    ></line></svg
                                >
                            </div>
                        {/if}

                        {#if answer >= 0}
                            <div
                                class="w-full h-full cursor-grab active:cursor-grabbing group card-container"
                                draggable="true"
                                on:dragstart={(event) =>
                                    handleDragStart(event, answer)}
                            >
                                <ValCardComponent
                                    id={answer}
                                    haveClose={true}
                                    on:remove={() =>
                                        handleRemoveFromGrid(index)}
                                />
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>
        </main>

        <!-- Sidebar Card Tray -->
        <aside
            class="w-1/5 bg-slate-200 dark:bg-slate-800 border-l-2 border-slate-300 dark:border-slate-700 flex flex-col p-3"
        >
            <header class="w-full bg-white dark:bg-slate-800 z-20 shadow-md">
                <nav class="container mx-auto px-4 sm:px-6 py-3">
                    <div class="flex justify-between items-center">
                        <div class="text-xl font-semibold">WIL پرسشنامه</div>
                        <button
                            class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white font-bold focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors"
                            on:click={handleSubmit}
                        >
                            پایان آزمون
                        </button>
                    </div>
                </nav>
            </header>
            <div
                class="flex-1 grid grid-cols-1 overflow-y-auto space-y-3 px-1 py-1"
            >
                {#each cardOrder as card}
                    {#if !cardWasUsed[card]}
                        <div
                            class="rounded-lg transition-all duration-200 cursor-pointer card-container
                           h-36"
                            class:ring-4={selectedCardIndex === card &&
                                selectedCardOriginalSlot === null}
                            class:ring-offset-2={selectedCardIndex === card &&
                                selectedCardOriginalSlot === null}
                            class:ring-indigo-500={selectedCardIndex === card &&
                                selectedCardOriginalSlot === null}
                            class:dark:ring-offset-slate-800={selectedCardIndex ===
                                card && selectedCardOriginalSlot === null}
                            class:opacity-60={selectedCardIndex !== null &&
                                selectedCardIndex !== card}
                            draggable="true"
                            on:dragstart={(event) =>
                                handleDragStart(event, card)}
                            on:click={() => handleCardSelectInTray(card)}
                            role="button"
                            tabindex="0"
                        >
                            <ValCardComponent id={card} haveClose={false} />
                        </div>
                    {/if}
                {/each}

                <!-- <h2 class="text-lg font-bold mb-3 text-center"> -->
                <!--     {#if usedCardsCnt < 20} -->
                <!--         کارت‌های باقی‌مانده -->
                <!--     {:else} -->
                <!--         تمام کارت‌ها استفاده شده -->
                <!--     {/if} -->
                <!-- </h2> -->
            </div>
        </aside>
    </div>

    <!-- Overlay Modal -->
    {#if isOverlayOpen}
        <Overlay
            canBeExited={false}
            isTransparent={true}
            on:close={() => (isOverlayOpen = false)}
        >
            {#if hasFilledEverything()}
                <h3 class="text-xl font-bold mb-4">پایان آزمون</h3>
                <p>آیا مطمئن هستید که می‌خواهید آزمون را تمام کنید؟</p>
                <div class="flex gap-4 mt-6">
                    <button
                        class="flex-1 px-4 py-2 bg-slate-600 hover:bg-slate-700 rounded-lg text-white font-bold transition-colors"
                        on:click={() => (isOverlayOpen = false)}
                    >
                        ادامه آزمون
                    </button>
                    <button
                        class="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-white font-bold transition-colors"
                        on:click={() => goto("/ValuTest/result")}
                    >
                        بله، تمام کن
                    </button>
                </div>
            {:else}
                <h3 class="text-xl font-bold mb-4">خطا</h3>
                <p>لطفا پیش از اتمام آزمون تمامی خانه‌ها را پر کنید.</p>
                <div class="flex gap-4 mt-6">
                    <button
                        class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-bold transition-colors"
                        on:click={() => (isOverlayOpen = false)}
                    >
                        متوجه شدم
                    </button>
                </div>
            {/if}
        </Overlay>
    {/if}
</div>

<style>
    .card-container {
        container-type: inline-size;
        container-name: val-card; /* Optional, but very good practice */
    }
</style>
