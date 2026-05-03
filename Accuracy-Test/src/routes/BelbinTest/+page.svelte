<script lang="ts">
    import { fly } from "svelte/transition";
    import { belbinQuestions } from "$lib/belbin-data";
    import Overlay from "$lib/../components/Overlay.svelte";
    import { submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";

    let currentQuestionIndex = 0;

    // آرایه ۵۶ تایی از اعداد صحیح برای ذخیره پاسخ‌ها (۷ سوال * ۸ گزینه)
    let userAnswers: number[] = new Array(56).fill(0);

    let slideDirection = -1;

    let showNextConfirm = false;
    let showSubmitConfirm = false;

    const themes = [
        {
            main: "bg-blue-50",
            box: "bg-blue-600 text-white",
            border: "border-blue-200",
        },
        {
            main: "bg-teal-50",
            box: "bg-teal-600 text-white",
            border: "border-teal-200",
        },
        {
            main: "bg-violet-50",
            box: "bg-violet-600 text-white",
            border: "border-violet-200",
        },
        {
            main: "bg-rose-50",
            box: "bg-rose-600 text-white",
            border: "border-rose-200",
        },
        {
            main: "bg-amber-50",
            box: "bg-amber-500 text-white",
            border: "border-amber-200",
        },
        {
            main: "bg-fuchsia-50",
            box: "bg-fuchsia-600 text-white",
            border: "border-fuchsia-200",
        },
        {
            main: "bg-cyan-50",
            box: "bg-cyan-600 text-white",
            border: "border-cyan-200",
        },
    ];

    $: startIndex = currentQuestionIndex * 8;
    $: currentAnswersSlice = userAnswers.slice(startIndex, startIndex + 8);
    $: totalAllocated = currentAnswersSlice.reduce((sum, val) => sum + val, 0);
    $: remainingPoints = 10 - totalAllocated;
    $: isNextDisabled = remainingPoints !== 0;
    $: currentTheme = themes[currentQuestionIndex];

    function incrementScore(globalIndex: number) {
        if (remainingPoints > 0) {
            userAnswers[globalIndex] += 1;
            userAnswers = [...userAnswers];
        }
    }

    function decrementScore(globalIndex: number) {
        if (userAnswers[globalIndex] > 0) {
            userAnswers[globalIndex] -= 1;
            userAnswers = [...userAnswers];
        }
    }

    function handleNextClick() {
        showNextConfirm = true;
    }

    function confirmNextQuestion() {
        showNextConfirm = false;
        if (
            !isNextDisabled &&
            currentQuestionIndex < belbinQuestions.length - 1
        ) {
            slideDirection = -1;
            currentQuestionIndex += 1;
        }
    }

    function prevQuestion() {
        if (currentQuestionIndex > 0) {
            slideDirection = 1;
            currentQuestionIndex -= 1;
        }
    }

    function handleSubmitClick() {
        showSubmitConfirm = true;
    }

    async function confirmSubmitQuiz() {
        showSubmitConfirm = false;

        // خروجی نهایی شامل همان آرایه 56 تایی ثابت از امتیازات است
        const payload = {
            quiz_type: "BelbinTest",
            answers: userAnswers,
        };
        await submitAnswer(payload);

        console.log("Submitting Belbin Test:", payload);
        // alert("آزمون با موفقیت ثبت شد.");
        goto("/");
    }
</script>

<div
    class="h-screen w-full transition-colors duration-700 {currentTheme.main} flex flex-col items-center justify-center p-2 md:p-4"
    dir="rtl"
>
    <div
        class="w-full max-w-4xl bg-white rounded-2xl shadow-xl border {currentTheme.border} p-4 md:p-5 flex flex-col max-h-[98vh] h-full transition-colors duration-700 relative overflow-hidden"
    >
        <div class="flex flex-row gap-3 mb-4 shrink-0">
            <div
                class="flex-1 {currentTheme.box} rounded-xl p-4 md:px-6 shadow-md flex flex-col justify-center transition-colors duration-500"
            >
                <span class="text-xs opacity-80 mb-1 font-medium tracking-wide"
                    >سوال {currentQuestionIndex + 1} از {belbinQuestions.length}</span
                >
                {#if belbinQuestions[currentQuestionIndex]}
                    <h1 class="text-xl md:text-2xl font-bold leading-relaxed">
                        {belbinQuestions[currentQuestionIndex].question}
                    </h1>
                {/if}
            </div>

            <div class="flex flex-col gap-2 shrink-0 w-28 md:w-36">
                <div
                    class="flex-1 border-2 transition-all duration-300 rounded-xl flex flex-col items-center justify-center shadow-sm
					{remainingPoints === 0
                        ? 'border-green-500 bg-green-50'
                        : 'border-gray-200 bg-gray-50'}"
                >
                    <span
                        class="text-[11px] font-bold uppercase {remainingPoints ===
                        0
                            ? 'text-green-700'
                            : 'text-gray-500'} mb-0.5">باقیمانده</span
                    >
                    <div class="flex items-center justify-center">
                        {#if remainingPoints === 0}
                            <svg
                                class="w-6 h-6 text-green-600"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                                ><path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2.5"
                                    d="M5 13l4 4L19 7"
                                ></path></svg
                            >
                        {:else}
                            <span class="text-xl font-black text-gray-800"
                                >{remainingPoints}</span
                            >
                        {/if}
                    </div>
                </div>

                <div
                    class="flex-1 bg-white border border-gray-100 rounded-xl flex flex-col items-center justify-center shadow-sm"
                >
                    <span class="text-[11px] font-bold text-gray-400 mb-0.5"
                        >ثبت شده</span
                    >
                    <span
                        class="text-lg font-black {totalAllocated === 10
                            ? 'text-green-600'
                            : 'text-gray-700'}"
                    >
                        {totalAllocated}
                        <span class="text-[10px] font-normal text-gray-400"
                            >/ ۱۰</span
                        >
                    </span>
                </div>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto px-1 pb-2 relative">
            {#if belbinQuestions[currentQuestionIndex]}
                {#key currentQuestionIndex}
                    <div
                        in:fly={{
                            x: slideDirection * 100,
                            duration: 400,
                            delay: 100,
                        }}
                        out:fly={{ x: slideDirection * -100, duration: 400 }}
                    >
                        <div class="flex flex-col gap-2">
                            {#each belbinQuestions[currentQuestionIndex].answers as answer, aIndex}
                                {@const globalIndex =
                                    currentQuestionIndex * 8 + aIndex}
                                {@const currentScore = userAnswers[globalIndex]}
                                <div
                                    class="flex items-center justify-between py-2 px-3 md:px-4 rounded-xl transition-all duration-200 border relative
									{currentScore > 0
                                        ? 'bg-slate-50 border-slate-300 shadow-sm z-10'
                                        : 'bg-white border-gray-100 hover:border-gray-300'}"
                                >
                                    <span
                                        class="text-lg
                                        text-gray-800 ml-3 leading-snug flex-1 hover:text-black text-justify"
                                    >
                                        {answer.text}
                                    </span>

                                    <div
                                        class="flex items-center gap-0.5 shrink-0 bg-white rounded-lg border border-gray-200 p-0.5 shadow-sm"
                                        dir="ltr"
                                    >
                                        <button
                                            class="w-8 h-8 rounded-md flex items-center justify-center text-xl font-bold transition-colors
												{currentScore === 0
                                                ? 'text-gray-200 cursor-not-allowed'
                                                : 'text-rose-500 hover:bg-rose-50'}"
                                            on:click={() =>
                                                decrementScore(globalIndex)}
                                            disabled={currentScore === 0}
                                            >-</button
                                        >
                                        <span
                                            class="w-6 text-center text-lg font-black {currentScore >
                                            0
                                                ? 'text-slate-800'
                                                : 'text-gray-400'}"
                                            >{currentScore}</span
                                        >
                                        <button
                                            class="w-8 h-8 rounded-md flex items-center justify-center text-xl font-bold transition-colors
												{remainingPoints === 0
                                                ? 'text-gray-200 cursor-not-allowed'
                                                : 'text-emerald-500 hover:bg-emerald-50'}"
                                            on:click={() =>
                                                incrementScore(globalIndex)}
                                            disabled={remainingPoints === 0}
                                            >+</button
                                        >
                                    </div>
                                </div>
                            {/each}
                        </div>
                    </div>
                {/key}
            {/if}
        </div>

        <div
            class="mt-4 pt-3 border-t border-gray-100 flex flex-col md:flex-row gap-4 items-center justify-between shrink-0"
        >
            <p
                class="text-xs md:text-sm text-amber-900 font-medium text-justify flex-1 leading-relaxed bg-amber-100 p-2 md:p-3 rounded-lg border border-amber-300 shadow-sm"
            >
                شما برای امتیازدهی به گزینه‌های این صفحه ۱۰ امتیاز بودجه دارید.
                که شکل توزیع آن بین گزینه‌ها با شماست. اما جمع امتیازات باید ۱۰
                باشد. نه بیشتر نه کمتر. گزینه‌هایی که امتیاز بیشتری دریافت
                می‌کنند اولویت‌های بالاتر شما هستنتد و گزینه‌هایی که امتیاز
                نمی‌گیرند درباره شما صادق نخواهند بود
            </p>

            <div class="flex gap-2 w-full md:w-auto shrink-0 justify-between">
                <button
                    class="px-5 py-2 rounded-xl text-sm font-bold transition-all duration-200 flex-1 md:flex-none
						{currentQuestionIndex === 0
                        ? 'text-gray-300 bg-gray-50 cursor-not-allowed'
                        : 'text-gray-600 bg-white border border-gray-200 hover:bg-gray-50 shadow-sm'}"
                    on:click={prevQuestion}
                    disabled={currentQuestionIndex === 0}
                >
                    مرحله قبل
                </button>

                {#if currentQuestionIndex === belbinQuestions.length - 1}
                    <button
                        class="px-6 py-2 rounded-xl text-sm font-bold text-white transition-all duration-300 shadow-md flex-1 md:flex-none
							{isNextDisabled
                            ? 'bg-gray-300 cursor-not-allowed shadow-none'
                            : 'bg-emerald-600 hover:bg-emerald-700 hover:-translate-y-0.5 shadow-emerald-200'}"
                        on:click={handleSubmitClick}
                        disabled={isNextDisabled}
                    >
                        پایان و ثبت
                    </button>
                {:else}
                    <button
                        class="px-6 py-2 rounded-xl text-sm font-bold text-white transition-all duration-300 shadow-md flex-1 md:flex-none
							{isNextDisabled
                            ? 'bg-gray-300 cursor-not-allowed shadow-none'
                            : 'bg-blue-600 hover:bg-blue-700 hover:-translate-y-0.5 shadow-blue-200'}"
                        on:click={handleNextClick}
                        disabled={isNextDisabled}
                    >
                        مرحله بعد
                    </button>
                {/if}
            </div>
        </div>
    </div>

    {#if showNextConfirm}
        <Overlay
            canBeExited={true}
            isTransparent={true}
            on:click={() => (showNextConfirm = false)}
        >
            <div
                class="text-center w-full px-4 py-2"
                dir="rtl"
                on:click|stopPropagation
            >
                <h3 class="text-lg font-bold text-white mb-3">
                    آیا از پاسخ‌های خود مطمئن هستید؟
                </h3>
                <p class="text-sm text-slate-300 mb-6 leading-relaxed">
                    پیش از پایان آزمون، همچنان امکان بازگشت به این مرحله و
                    ویرایش پاسخ‌ها وجود دارد.
                </p>
                <div class="flex justify-center gap-3">
                    <button
                        class="px-5 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg text-white font-medium transition-colors"
                        on:click={() => (showNextConfirm = false)}
                        >انصراف</button
                    >
                    <button
                        class="px-5 py-2 bg-blue-500 hover:bg-blue-400 rounded-lg text-white font-bold transition-colors"
                        on:click={confirmNextQuestion}>تایید و ادامه</button
                    >
                </div>
            </div>
        </Overlay>
    {/if}

    {#if showSubmitConfirm}
        <Overlay
            canBeExited={true}
            isTransparent={true}
            on:click={() => (showSubmitConfirm = false)}
        >
            <div
                class="text-center w-full px-4 py-2"
                dir="rtl"
                on:click|stopPropagation
            >
                <div
                    class="w-14 h-14 bg-rose-500/20 text-rose-400 rounded-full flex items-center justify-center mx-auto mb-4"
                >
                    <svg
                        class="w-8 h-8"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        ><path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        ></path></svg
                    >
                </div>
                <h3 class="text-xl font-bold text-white mb-2">
                    ثبت نهایی آزمون
                </h3>
                <p
                    class="text-sm text-rose-200 mb-6 leading-relaxed bg-rose-900/30 p-3 rounded-lg border border-rose-800"
                >
                    آیا از پایان آزمون اطمینان دارید؟ <strong
                        >پس از ثبت، امکان بازگشت و تغییر پاسخ‌ها وجود نخواهد
                        داشت.</strong
                    >
                </p>
                <div class="flex justify-center gap-3">
                    <button
                        class="px-5 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg text-white font-medium transition-colors"
                        on:click={() => (showSubmitConfirm = false)}
                        >بررسی مجدد</button
                    >
                    <button
                        class="px-5 py-2 bg-rose-600 hover:bg-rose-500 rounded-lg text-white font-bold transition-colors shadow-lg shadow-rose-900/50"
                        on:click={confirmSubmitQuiz}>بله، ثبت نهایی</button
                    >
                </div>
            </div>
        </Overlay>
    {/if}
</div>
