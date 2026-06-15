<script>
    import { fly, fade } from "svelte/transition";
    import { belbinQuestions } from "$lib/belbin-data";
    import { goto } from "$app/navigation";
    import Overlay from "../../components/Overlay.svelte";
    import { submitAnswer } from "$lib/utils/api/quiz-apis";
    import { onMount, tick } from "svelte";

    let currentQuestionIndex = 0;
    let userAnswers = new Array(56).fill(0);

    let slideDirection = 1;
    let showNextConfirm = false;
    let showSubmitConfirm = false;

    // Scroll detection logic
    let scrollContainer;
    let showScrollIndicator = true;

    function checkScroll() {
        if (!scrollContainer) return;
        const { scrollTop, scrollHeight, clientHeight } = scrollContainer;
        if (
            scrollHeight <= clientHeight ||
            Math.ceil(scrollTop + clientHeight) >= scrollHeight - 10
        ) {
            showScrollIndicator = false;
        } else {
            showScrollIndicator = true;
        }
    }

    onMount(() => {
        checkScroll();
        window.addEventListener("resize", checkScroll);
        return () => window.removeEventListener("resize", checkScroll);
    });

    $: currentQuestionIndex, tick().then(checkScroll);

    const themes = [
        {
            primary: "bg-indigo-600",
            light: "bg-indigo-50",
            text: "text-indigo-800",
            border: "border-indigo-200",
            blob: "bg-indigo-400",
        },
        {
            primary: "bg-rose-600",
            light: "bg-rose-50",
            text: "text-rose-800",
            border: "border-rose-200",
            blob: "bg-rose-400",
        },
        {
            primary: "bg-emerald-600",
            light: "bg-emerald-50",
            text: "text-emerald-800",
            border: "border-emerald-200",
            blob: "bg-emerald-400",
        },
        {
            primary: "bg-amber-600",
            light: "bg-amber-50",
            text: "text-amber-800",
            border: "border-amber-200",
            blob: "bg-amber-400",
        },
        {
            primary: "bg-sky-600",
            light: "bg-sky-50",
            text: "text-sky-800",
            border: "border-sky-200",
            blob: "bg-sky-400",
        },
        {
            primary: "bg-violet-600",
            light: "bg-violet-50",
            text: "text-violet-800",
            border: "border-violet-200",
            blob: "bg-violet-400",
        },
        {
            primary: "bg-fuchsia-600",
            light: "bg-fuchsia-50",
            text: "text-fuchsia-800",
            border: "border-fuchsia-200",
            blob: "bg-fuchsia-400",
        },
    ];

    $: startIndex = currentQuestionIndex * 8;
    $: currentAnswersSlice = userAnswers.slice(startIndex, startIndex + 8);
    $: totalAllocated = currentAnswersSlice.reduce((sum, val) => sum + val, 0);
    $: remainingPoints = 10 - totalAllocated;
    $: isNextDisabled = remainingPoints !== 0;

    $: currentTheme = themes[currentQuestionIndex];

    function incrementScore(globalIndex) {
        if (remainingPoints > 0) userAnswers[globalIndex] += 1;
    }

    function decrementScore(globalIndex) {
        if (userAnswers[globalIndex] > 0) userAnswers[globalIndex] -= 1;
    }

    function handleNextClick() {
        if (totalAllocated === 10) showNextConfirm = true;
    }

    function confirmNextQuestion() {
        showNextConfirm = false;
        if (currentQuestionIndex < 6) {
            slideDirection = 1;
            currentQuestionIndex += 1;
        }
    }

    function prevQuestion() {
        if (currentQuestionIndex > 0) {
            slideDirection = -1;
            currentQuestionIndex -= 1;
        }
    }

    function handleSubmitClick() {
        if (totalAllocated === 10) showSubmitConfirm = true;
    }

    async function confirmSubmitQuiz() {
        showSubmitConfirm = false;
        try {
            await submitAnswer({
                quiz_type: "BelbinTest",
                answers: userAnswers,
            });
            goto("/");
        } catch (error) {
            console.error("Failed to submit answers:", error);
        }
    }
</script>

<svelte:head>
    <title>پرسشنامه بلبین</title>
</svelte:head>

<div
    dir="rtl"
    class="min-h-screen h-screen w-full bg-slate-50 flex flex-col items-center justify-center p-2 sm:p-4 md:p-6 font-vazir relative overflow-hidden selection:bg-indigo-100 selection:text-indigo-900"
>
    <!-- Dynamic Gradient Blobs matching the image -->
    <div
        class="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] rounded-full {currentTheme.blob} opacity-20 blur-[120px] transition-colors duration-1000 pointer-events-none"
    ></div>
    <div
        class="absolute bottom-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full {currentTheme.blob} opacity-15 blur-[100px] transition-colors duration-1000 pointer-events-none"
    ></div>

    <div
        class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03] pointer-events-none mix-blend-overlay"
    ></div>

    <div
        class="w-full max-w-4xl bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl flex flex-col max-h-[98vh] sm:max-h-[95vh] h-full border border-white/50 relative overflow-hidden z-10"
    >
        <div
            class="{currentTheme.primary} text-white p-4 sm:p-6 transition-colors duration-500 relative overflow-hidden shrink-0 shadow-md z-10"
        >
            <div
                class="absolute inset-0 bg-white opacity-10 mix-blend-overlay"
            ></div>

            <div
                class="flex flex-col md:flex-row justify-between items-center gap-4 relative z-10"
            >
                <div class="flex items-center gap-3 w-full md:w-auto">
                    <div
                        class="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-xl font-bold shadow-inner shrink-0"
                    >
                        {currentQuestionIndex + 1}
                    </div>
                    <h2
                        class="text-base sm:text-lg md:text-xl font-bold leading-tight flex-1"
                    >
                        {belbinQuestions[currentQuestionIndex].question}
                    </h2>
                </div>

                <div
                    class="flex items-center gap-3 w-full md:w-auto bg-white/10 p-2 rounded-2xl backdrop-blur-md border border-white/20"
                >
                    <div class="flex flex-col items-center px-4 py-1">
                        <span
                            class="text-xs font-medium opacity-80 uppercase tracking-wider mb-1"
                            >امتیاز باقیمانده</span
                        >
                        <div class="flex items-baseline gap-1">
                            <span
                                class="text-2xl font-black {remainingPoints ===
                                0
                                    ? 'text-green-300 drop-shadow-md'
                                    : 'text-white'} transition-colors duration-300"
                            >
                                {remainingPoints}
                            </span>
                            <span class="text-sm opacity-70">از 10</span>
                        </div>
                    </div>
                    <div class="w-px h-10 bg-white/20 mx-1"></div>
                    <div class="flex flex-col items-center px-4 py-1">
                        <span
                            class="text-xs font-medium opacity-80 uppercase tracking-wider mb-1"
                            >اختصاص یافته</span
                        >
                        <span class="text-2xl font-black">{totalAllocated}</span
                        >
                    </div>
                </div>
            </div>

            <div
                class="w-full bg-black/20 rounded-full h-1.5 mt-5 overflow-hidden"
            >
                <div
                    class="bg-white h-1.5 rounded-full transition-all duration-500 ease-out"
                    style="width: {((currentQuestionIndex + 1) / 7) * 100}%"
                ></div>
            </div>
        </div>

        <div
            class="flex-1 relative overflow-hidden flex flex-col bg-slate-50/30"
        >
            {#if showScrollIndicator}
                <div
                    transition:fade={{ duration: 200 }}
                    class="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-slate-100 to-transparent z-10 pointer-events-none"
                ></div>
                <div
                    transition:fade={{ duration: 200 }}
                    class="absolute bottom-4 left-1/2 -translate-x-1/2 bg-slate-800 text-white px-5 py-2.5 rounded-full shadow-lg flex items-center gap-2 pointer-events-none animate-bounce z-20"
                >
                    <span class="text-sm font-bold tracking-wide"
                        >بیشتر اسکرول کنید</span
                    >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2.5"
                            d="M19 14l-7 7m0 0l-7-7m7 7V3"
                        />
                    </svg>
                </div>
            {/if}

            <div
                bind:this={scrollContainer}
                on:scroll={checkScroll}
                class="flex-1 overflow-y-scroll px-2 sm:px-4 pb-8 pt-4 relative custom-scrollbar w-full"
            >
                {#key currentQuestionIndex}
                    <div
                        in:fly={{
                            x: slideDirection * 40,
                            duration: 400,
                            delay: 100,
                        }}
                        out:fly={{ x: -slideDirection * 40, duration: 300 }}
                        class="w-full h-full space-y-3"
                    >
                        {#each belbinQuestions[currentQuestionIndex].answers as answer, i}
                            {@const globalIndex = startIndex + i}
                            {@const score = userAnswers[globalIndex]}
                            {@const isSelected = score > 0}

                            <div
                                class="group relative bg-white/90 rounded-2xl p-3 sm:p-4 border-2 transition-all duration-300 hover:shadow-lg flex flex-col sm:flex-row items-center gap-4 {isSelected
                                    ? `${currentTheme.border} ${currentTheme.light} shadow-md`
                                    : 'border-slate-100 hover:border-slate-300'}"
                            >
                                <div
                                    class="flex-1 w-full text-slate-700 text-sm sm:text-base md:text-lg leading-relaxed font-medium"
                                >
                                    {answer.text}
                                </div>

                                <div
                                    class="flex items-center gap-3 shrink-0 bg-slate-100 p-1.5 rounded-xl shadow-inner w-full sm:w-auto justify-between sm:justify-start"
                                >
                                    <button
                                        class="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl transition-all duration-200 active:scale-95 {score >
                                        0
                                            ? 'bg-white text-slate-700 shadow-sm hover:bg-slate-50'
                                            : 'text-slate-400 opacity-50 cursor-not-allowed'}"
                                        on:click={() =>
                                            decrementScore(globalIndex)}
                                        disabled={score === 0}
                                    >
                                        -
                                    </button>
                                    <div
                                        class="w-8 text-center font-black text-xl {isSelected
                                            ? currentTheme.text
                                            : 'text-slate-600'} select-none"
                                    >
                                        {score}
                                    </div>
                                    <button
                                        class="w-10 h-10 rounded-lg flex items-center justify-center font-bold text-xl transition-all duration-200 active:scale-95 {remainingPoints >
                                        0
                                            ? `${currentTheme.primary} text-white shadow-md hover:brightness-110`
                                            : 'bg-slate-200 text-slate-400 cursor-not-allowed'}"
                                        on:click={() =>
                                            incrementScore(globalIndex)}
                                        disabled={remainingPoints === 0}
                                    >
                                        +
                                    </button>
                                </div>
                            </div>
                        {/each}
                    </div>
                {/key}
            </div>
        </div>

        <div
            class="bg-amber-50/80 backdrop-blur-sm border-t border-amber-200 px-4 py-3 sm:px-6 shrink-0 z-10 flex items-start gap-3 shadow-inner"
        >
            <div class="text-amber-500 mt-0.5 shrink-0">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                </svg>
            </div>
            <p
                class="text-amber-900 text-xs sm:text-sm font-medium leading-relaxed text-justify"
            >
                شما برای امتیازدهی به گزینه‌های این صفحه <strong
                    class="font-bold">۱۰ امتیاز</strong
                > بودجه دارید. که شکل توزیع آن بین گزینه‌ها با شماست. اما جمع امتیازات
                باید ۱۰ باشد. نه بیشتر نه کمتر. گزینه‌هایی که امتیاز بیشتری دریافت
                می‌کنند اولویت‌های بالاتر شما هستند و گزینه‌هایی که امتیاز نمی‌گیرند
                درباره شما صادق نخواهند بود.
            </p>
        </div>

        <div
            class="p-4 sm:p-6 bg-white/90 backdrop-blur-sm border-t border-slate-100 flex flex-col sm:flex-row justify-between items-center gap-4 shrink-0 shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.05)] z-10"
        >
            <button
                class="w-full sm:w-auto px-6 py-3 rounded-xl font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed disabled:active:scale-100"
                on:click={prevQuestion}
                disabled={currentQuestionIndex === 0}
            >
                سوال قبلی
            </button>

            <div class="text-sm font-medium text-slate-500 hidden md:block">
                سوال {currentQuestionIndex + 1} از 7
            </div>

            {#if currentQuestionIndex < 6}
                <button
                    class="w-full sm:w-auto px-8 py-3 rounded-xl font-bold text-white transition-all duration-300 shadow-lg active:scale-95 flex items-center justify-center gap-2 {isNextDisabled
                        ? 'bg-slate-300 cursor-not-allowed shadow-none'
                        : `${currentTheme.primary} hover:brightness-110 hover:-translate-y-0.5`}"
                    on:click={handleNextClick}
                    disabled={isNextDisabled}
                >
                    <span>سوال بعدی</span>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 rtl:rotate-180"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </button>
            {:else}
                <button
                    class="w-full sm:w-auto px-8 py-3 rounded-xl font-bold text-white transition-all duration-300 shadow-lg shadow-emerald-500/30 active:scale-95 flex items-center justify-center gap-2 {isNextDisabled
                        ? 'bg-slate-300 cursor-not-allowed shadow-none'
                        : 'bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 hover:-translate-y-0.5'}"
                    on:click={handleSubmitClick}
                    disabled={isNextDisabled}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clip-rule="evenodd"
                        />
                    </svg>
                    <span>ثبت نهایی</span>
                </button>
            {/if}
        </div>
    </div>
</div>

<!-- MISSING NEXT CONFIRM OVERLAY ADDED -->
{#if showNextConfirm}
    <Overlay
        canBeExited={true}
        isTransparent={true}
        isTransparentMain={true}
        on:close={() => (showNextConfirm = false)}
    >
        <div
            class="bg-white p-6 md:p-8 rounded-3xl shadow-2xl max-w-sm w-[90%] text-center border-t-4 {currentTheme.border.replace(
                'border-',
                'border-',
            )}"
        >
            <div
                class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 {currentTheme.light} {currentTheme.text}"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-8 w-8"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M5 13l4 4L19 7"
                    />
                </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-2">
                تایید امتیازات
            </h3>
            <p class="text-slate-600 mb-8 font-medium">
                امتیاز شما با موفقیت برای این بخش توزیع شد. درصورت نیاز توانایی
                بازگشت و تغییر امتیازات را پیش از پایان پرسشنامه خواهید داشت. به
                سوال بعدی برویم؟
            </p>
            <div class="flex gap-3 justify-center">
                <button
                    class="px-6 py-2.5 rounded-xl text-slate-600 bg-slate-100 hover:bg-slate-200 font-bold transition-colors"
                    on:click={() => (showNextConfirm = false)}>بازنگری</button
                >
                <button
                    class="px-6 py-2.5 rounded-xl text-white font-bold transition-colors shadow-md {currentTheme.primary} hover:brightness-110"
                    on:click={confirmNextQuestion}>بله، ادامه</button
                >
            </div>
        </div>
    </Overlay>
{/if}

{#if showSubmitConfirm}
    <Overlay
        canBeExited={true}
        isTransparent={true}
        isTransparentMain={true}
        on:close={() => (showSubmitConfirm = false)}
    >
        <div
            class="bg-white p-6 md:p-8 rounded-3xl shadow-2xl max-w-sm w-[90%] text-center border-t-4 border-emerald-500"
        >
            <div
                class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-8 w-8"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-2">
                ثبت نهایی پرسشنامه
            </h3>
            <p class="text-slate-600 mb-8 font-medium">
                پاسخ‌ها ثبت شده و قابل تغییر نخواهند بود. مطمئن هستید؟
            </p>
            <div class="flex gap-3 justify-center">
                <button
                    class="px-6 py-2.5 rounded-xl text-slate-600 bg-slate-100 hover:bg-slate-200 font-bold transition-colors"
                    on:click={() => (showSubmitConfirm = false)}>انصراف</button
                >
                <button
                    class="px-6 py-2.5 rounded-xl text-white bg-emerald-600 hover:bg-emerald-700 font-bold transition-colors shadow-md"
                    on:click={confirmSubmitQuiz}>بله، ثبت کن</button
                >
            </div>
        </div>
    </Overlay>
{/if}

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 10px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: #e2e8f0;
        border-radius: 10px;
        border: 2px solid #f8fafc;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background-color: #94a3b8;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background-color: #64748b;
    }
    .custom-scrollbar {
        scrollbar-width: auto;
        scrollbar-color: #94a3b8 #e2e8f0;
    }
</style>
