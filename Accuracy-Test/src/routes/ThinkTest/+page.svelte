<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import QuizLayout from "../../components/QuizLayout.svelte";
    import { fly, fade, crossfade } from "svelte/transition";
    import { cubicOut } from "svelte/easing";
    import QuestionCard from "../../components/QuestionCard.svelte";
    import FlipClock from "../../components/FlipClock.svelte";
    import { createQuizTimer } from "$lib/timer";
    import { quizData } from "$lib/think-data";
    import ProgressBar from "../../components/ProgressBar.svelte"; // adjust path
    import { submitAnswer } from "$lib/utils/api/quiz-apis";

    let partIndex = 0;
    let groupIndex = 0;
    let subIndex = 0;
    let baseHue = 110;

    // Update the hue on mount to a random value
    onMount(() => {
        baseHue = Math.floor(Math.random() * 360);
    });

    // Reactively calculate the dynamic hue based on your current global question index
    $: hue = (baseHue + currentGlobalQuestionIndex * 35) % 360;

    let quizState: "part-title" | "main-text" | "answering" = "part-title";

    // Answers mapped by Question ID (string) -> Score (number)
    let answers: Record<string, number> = {};
    let isSubmitting = false;
    let diraction = 1;
    let isTransitioning = false;

    const TOTAL_SECONDS = 45 * 60;
    const { timer, start, destroy } = createQuizTimer(
        new Date(),
        TOTAL_SECONDS,
    );

    const [send, receive] = crossfade({
        duration: 500,
        easing: cubicOut,
        fallback(node, params) {
            return fade(node, { duration: 300 });
        },
    });

    onMount(() => start());
    onDestroy(() => destroy());

    // Reactive declarations for current data
    $: currentPart = quizData[partIndex];
    $: currentGroup = currentPart.groups[groupIndex];
    $: currentSubQuestion = currentGroup.subQuestions[subIndex];

    // Look up answer using the string ID
    $: currentAnswer = answers[currentSubQuestion?.id];

    $: isLastQuestion =
        partIndex === quizData.length - 1 &&
        groupIndex === currentPart.groups.length - 1 &&
        subIndex === currentGroup.subQuestions.length - 1 &&
        quizState === "answering";

    // Dynamically calculate the global index for the ProgressBar's little arrow pointer
    $: currentGlobalQuestionIndex = (() => {
        let index = 0;
        for (let pIdx = 0; pIdx < quizData.length; pIdx++) {
            const part = quizData[pIdx];
            for (let gIdx = 0; gIdx < part.groups.length; gIdx++) {
                const group = part.groups[gIdx];
                for (let sIdx = 0; sIdx < group.subQuestions.length; sIdx++) {
                    if (
                        pIdx === partIndex &&
                        gIdx === groupIndex &&
                        sIdx === subIndex
                    ) {
                        return index;
                    }
                    index++;
                }
            }
        }
        return index;
    })();

    function handleSelect(score: number) {
        if (isTransitioning) return;
        answers[currentSubQuestion.id] = score;
        answers = { ...answers };
    }

    function nextQuestion() {
        diraction = 1;
        if (quizState === "part-title") {
            quizState = "main-text";
        } else if (quizState === "main-text") {
            quizState = "answering";
        } else {
            // IF skipping (no answer selected), set the answer for this ID to 0
            if (currentAnswer === undefined) {
                answers[currentSubQuestion.id] = 0;
                answers = { ...answers }; // Trigger reactivity
            }

            if (subIndex < currentGroup.subQuestions.length - 1) {
                subIndex += 1;
            } else if (groupIndex < currentPart.groups.length - 1) {
                groupIndex += 1;
                subIndex = 0;
                quizState = "main-text";
            } else if (partIndex < quizData.length - 1) {
                partIndex += 1;
                groupIndex = 0;
                subIndex = 0;
                quizState = "part-title";
            }
        }
    }

    function prevQuestion() {
        diraction = -1;
        if (quizState === "answering") {
            if (subIndex > 0) {
                subIndex -= 1;
            } else {
                quizState = "main-text";
            }
        } else if (quizState === "main-text") {
            if (groupIndex > 0) {
                groupIndex -= 1;
                subIndex =
                    currentPart.groups[groupIndex].subQuestions.length - 1;
                quizState = "answering";
            } else {
                quizState = "part-title";
            }
        } else if (quizState === "part-title") {
            if (partIndex > 0) {
                partIndex -= 1;
                groupIndex = quizData[partIndex].groups.length - 1;
                subIndex =
                    quizData[partIndex].groups[groupIndex].subQuestions.length -
                    1;
                quizState = "answering";
            }
        }
    }

    async function finishQuiz() {
        isSubmitting = true;

        // 1. Flatten the answers into a simple array based on global question order
        let formattedAnswers = [];
        for (const part of quizData) {
            for (const group of part.groups) {
                for (const subQ of group.subQuestions) {
                    const val = answers[subQ.id];
                    formattedAnswers.push(val === undefined ? 0 : val);
                }
            }
        }

        // 2. Ensure the array is exactly 80 items long (pad with 0s or slice)
        while (formattedAnswers.length < 80) {
            formattedAnswers.push(0);
        }
        formattedAnswers = formattedAnswers.slice(0, 80);

        try {
            await submitAnswer({
                quiz_type: "ThinkTest",
                answers: formattedAnswers, // Submitting the array of length 80
            });
            alert("آزمون با موفقیت ثبت شد!");
        } catch (error) {
            console.error("Submission failed:", error);
            alert("خطایی در ثبت آزمون رخ داد.");
        } finally {
            isSubmitting = false;
        }
    }

    const partHue = (baseHue + currentGlobalQuestionIndex * 75) % 360;

    // You can make it a solid color, or a gradient! Let's do a soft gradient string.
    // We use 65% lightness so it stands out against your 90% lightness background.
    const colorStyle = `linear-gradient(135deg, hsl(${partHue}, 80%, 70%), hsl(${(partHue + 20) % 360}, 80%, 60%))`;

    const partColors = [
        "bg-blue-500",
        "bg-purple-500",
        "bg-green-500",
        "bg-orange-500",
        "bg-red-500",
    ];

    $: progressBarQuestions = (() => {
        let globalIndex = 0;
        const arr = [];

        for (let pIdx = 0; pIdx < quizData.length; pIdx++) {
            const part = quizData[pIdx];
            let isStartOfPart = true;

            // 1. Calculate the dynamic HSL color for this entire part
            // Make sure 'baseHue' exists in your component (e.g., let baseHue = 210;)
            const segmentHue = (baseHue + pIdx * 35) % 360;
            const dynamicColor = `hsl(${segmentHue}, 80%, 60%)`;

            for (const group of part.groups) {
                for (const subQ of group.subQuestions) {
                    // 2. Declare state and DEFAULT it to "unanswered"
                    let state: "unanswered" | "answered" | "skipped" =
                        "unanswered";

                    const ans = answers[subQ.id];

                    // 3. Override state if we have an answer or skip
                    if (ans !== undefined && ans !== 0) {
                        state = "answered";
                    } else if (ans === 0) {
                        state = "skipped";
                    }

                    arr.push({
                        index: globalIndex,
                        state: state,
                        color: dynamicColor, // <--- Assign the generated HSL string
                        isPartStart: isStartOfPart,
                    });

                    isStartOfPart = false;
                    globalIndex++;
                }
            }
        }
        return arr;
    })();
</script>

<div dir="rtl">
    <QuizLayout {hue}>
        <div class="flex flex-col items-center gap-4 mb-8">
            <FlipClock timeInSeconds={$timer} />

            <!-- Timer Progress Bar -->
            <!-- ... FlipClock component ... -->
            <ProgressBar
                questions={progressBarQuestions}
                currentIndex={currentGlobalQuestionIndex}
            />

            <!-- گرید اصلی برای هندل کردن عنوان بخش در مقابل سوالات -->
            <div class="grid w-full place-items-center">
                <!-- STATE 1: PART TITLE -->
                {#if quizState === "part-title"}
                    <div
                        class="col-start-1 row-start-1 w-full bg-white p-12 rounded-2xl shadow-sm border border-slate-200 text-center flex flex-col items-center justify-center min-h-[300px]"
                        in:fly={{
                            x: -300 * diraction,
                            duration: 400,
                            delay: 400,
                        }}
                        out:fly={{ x: 300 * diraction, duration: 400 }}
                    >
                        <span
                            class="text-sm font-bold text-blue-600 bg-blue-50 px-4 py-1.5 rounded-full mb-4"
                        >
                            بخش {currentPart.partNumber}
                        </span>
                        <h1
                            class="text-3xl md:text-4xl font-extrabold text-slate-800 mb-6 leading-tight"
                        >
                            {currentPart.title}
                        </h1>
                    </div>

                    <!-- STATES 2 & 3: MAIN TEXT AND ANSWERING -->
                {:else}
                    <!-- OUTER KEY: هندل کردن انیمیشن سوایپ هنگام تغییر گروه -->
                    {#key currentGroup?.mainText}
                        <div
                            class="col-start-1 row-start-1 w-full grid place-items-center"
                            in:fly={{
                                x: -300 * diraction,
                                duration: 400,
                                delay: 400,
                            }}
                            out:fly={{ x: 300 * diraction, duration: 400 }}
                        >
                            {#if quizState === "main-text"}
                                <!-- Parent div: Fade برای جلوگیری از اسنپ شدن و روی هم افتادن المنت‌ها -->
                                <div
                                    class="col-start-1 row-start-1 w-full"
                                    in:fade={{ duration: 400, delay: 200 }}
                                    out:fade={{ duration: 400 }}
                                >
                                    <div
                                        class="w-full bg-white p-8 rounded-2xl shadow-sm border border-slate-200 min-h-[300px] flex items-center"
                                        in:receive={{ key: "morph-text" }}
                                        out:send={{ key: "morph-text" }}
                                    >
                                        <h2
                                            class="text-xl font-bold text-slate-800 leading-loose text-justify w-full"
                                        >
                                            {currentGroup.mainText}
                                        </h2>
                                    </div>
                                </div>
                            {:else if quizState === "answering"}
                                <!-- Parent div: Fade برای مدیریت نرم‌تر گرید حین ترانزیشن -->
                                <div
                                    class="col-start-1 row-start-1 w-full flex flex-col items-center gap-6"
                                    in:fade={{ duration: 400, delay: 200 }}
                                    out:fade={{ duration: 400 }}
                                >
                                    <!-- کارت کوچک متن که از کارت بزرگ ساخته/تبدیل (مورف) می‌شود -->
                                    <div
                                        class="w-full bg-slate-50 p-6 rounded-xl border border-slate-200 shadow-sm"
                                        in:receive={{ key: "morph-text" }}
                                        out:send={{ key: "morph-text" }}
                                    >
                                        <p
                                            class="text-lg font-semibold text-slate-700 leading-relaxed text-justify"
                                        >
                                            {currentGroup.mainText}
                                        </p>
                                    </div>

                                    <!-- بخش کارت سوال -->
                                    <div class="grid w-full place-items-center">
                                        {#key currentSubQuestion.id}
                                            <div
                                                class="col-start-1 row-start-1 w-full"
                                                in:fly={{
                                                    x: -200 * diraction,
                                                    duration: 400,
                                                    delay: 300,
                                                }}
                                                out:fly={{
                                                    x: 200 * diraction,
                                                    duration: 300,
                                                }}
                                            >
                                                <QuestionCard
                                                    question={currentSubQuestion.text}
                                                    choices={currentSubQuestion.choices}
                                                    selectedScore={currentAnswer}
                                                    onSelect={handleSelect}
                                                    onPrev={prevQuestion}
                                                    onNext={nextQuestion}
                                                    animDiraction={diraction}
                                                    canAdvance={currentAnswer !==
                                                        undefined}
                                                />
                                            </div>
                                        {/key}
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/key}
                {/if}
            </div>

            <!-- GLOBAL BOTTOM NAVIGATION -->
            <!-- GLOBAL BOTTOM NAVIGATION -->
            <div class="flex justify-between items-center w-full mt-8">
                <button
                    class="flex items-center gap-2 px-6 py-3 rounded-full text-base font-semibold text-slate-700 bg-white border border-slate-200 shadow-sm transition-all duration-200 hover:bg-slate-50 hover:-translate-y-0.5 hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-sm"
                    on:click={prevQuestion}
                    disabled={isSubmitting ||
                        (quizState === "part-title" && partIndex === 0)}
                >
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                    قبلی
                </button>

                {#if isLastQuestion}
                    <button
                        class="flex items-center gap-2 px-8 py-3 rounded-full text-base font-semibold text-white bg-slate-900 shadow-md transition-all duration-200 hover:bg-black hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-md"
                        on:click={finishQuiz}
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? "در حال ثبت..." : "پایان آزمون"}
                    </button>
                {:else}
                    <button
                        class="flex items-center gap-2 px-6 py-3 rounded-full text-base font-semibold text-slate-700 bg-white border border-slate-200 shadow-sm transition-all duration-200 hover:bg-slate-50 hover:-translate-y-0.5 hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-sm"
                        on:click={nextQuestion}
                        disabled={isSubmitting}
                    >
                        {quizState === "answering" &&
                        currentAnswer === undefined
                            ? "رد کن"
                            : "بعدی"}
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <polyline points="15 18 9 12 15 6"></polyline>
                        </svg>
                    </button>
                {/if}
            </div>
        </div></QuizLayout
    >
</div>
