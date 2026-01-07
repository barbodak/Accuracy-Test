<script lang="ts">
    import {
        retreiveQuizAnswer,
        retreiveAccount,
    } from "$lib/utils/api/quiz-apis";
    import { onMount, onDestroy } from "svelte";
    import { fly } from "svelte/transition";
    import { toJalaali } from "jalaali-js";
    import { invalidateAll } from "$app/navigation"; // To refresh data without full reload

    // --- Types ---
    type TextQuizResult = {
        correct: number;
        wrong: number;
        unanswered?: number; // Added optional field
        no_no: number;
        no_yes: number;
        yes_no: number;
        yes_yes: number;
    };

    type PicQuizResult = {
        correct: number;
        wrong: number;
        unanswered?: number; // Added optional field
    };

    export let data;

    const ACU_TEST_PIC_TIMELIMIT_SECONDS = 60 * 5 + 11; // 311 seconds
    const ACU_TEST_TEXT_TIMELIMIT_SECONDS = 60 * 6 + 11; // 371 seconds

    // State for timers
    let textQuizRemaining = 0;
    let picQuizRemaining = 0;
    let timerInterval: number;

    // Helper to format seconds into MM:SS
    function formatTime(seconds: number) {
        if (seconds <= 0) return "00:00";
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, "0")}`;
    }

    function calculateTimeRemaining(
        startTimeStr: number,
        limitSeconds: number,
    ) {
        if (!startTimeStr) return 0;
        const startTime = new Date(startTimeStr).getTime();
        const endTime = startTime + limitSeconds * 1000;
        const now = Date.now();
        const diff = Math.floor((endTime - now) / 1000);
        return diff > 0 ? diff : 0;
    }

    function updateTimers() {
        // 1. Logic for Text Quiz (Check your specific variable name for the text quiz result)
        // Assuming variable is something like data.acu_text_result based on context
        if (data.acu_text_result?.quiz_time === "not_ended") {
            textQuizRemaining = calculateTimeRemaining(
                data.acu_text_result.start_time,
                ACU_TEST_TEXT_TIMELIMIT_SECONDS,
            );

            // Refresh if timer just hit 0
            if (textQuizRemaining === 0) {
                handleTimerEnd();
            }
        }

        // 2. Logic for Picture Quiz
        // Assuming variable is something like data.acu_pic_result
        if (data.acu_pic_result?.quiz_time === "not_ended") {
            picQuizRemaining = calculateTimeRemaining(
                data.acu_pic_result.start_time,
                ACU_TEST_PIC_TIMELIMIT_SECONDS,
            );

            // Refresh if timer just hit 0
            if (picQuizRemaining === 0) {
                handleTimerEnd();
            }
        }
    }

    function handleTimerEnd() {
        clearInterval(timerInterval);
        // Reloads the page to fetch new results
        location.reload();
        // Alternatively use invalidateAll() for a smoother SvelteKit reload:
        // invalidateAll();
    }

    // --- State ---
    let first_name: string = "";
    let last_name: string = "";
    let age: number | null = null;
    let jalaliDate: string = "";

    let textResult: TextQuizResult | null = null;
    let picResult: PicQuizResult | null = null;
    let loading = true;
    let errorMsg: string | null = null;

    // --- Stats Logic ---
    $: textStats = textResult ? calculateTextStats(textResult) : null;
    $: picStats = picResult ? calculatePicStats(picResult) : null;

    function calculateTextStats(data: TextQuizResult) {
        const calculatedCorrect = data.no_no + data.yes_yes;
        const calculatedWrong = data.no_yes + data.yes_no;
        // Check if API returns unanswered, otherwise default to 0
        const unanswered = 90 - calculatedCorrect - calculatedWrong;

        const totalAttempts = calculatedCorrect + calculatedWrong;
        const accuracy =
            totalAttempts > 0
                ? ((calculatedCorrect - calculatedWrong * (1 / 3)) / 90) * 100
                : 0;

        const totalActualNo = data.no_no + data.no_yes;
        const falsePositiveRate =
            totalActualNo > 0 ? (data.no_yes / totalActualNo) * 100 : 0; // Impulsivity

        const totalActualYes = data.yes_yes + data.yes_no;
        const falseNegativeRate =
            totalActualYes > 0 ? (data.yes_no / totalActualYes) * 100 : 0; // Inattention

        return {
            correctCount: calculatedCorrect,
            wrongCount: calculatedWrong,
            unansweredCount: unanswered,
            accuracy: accuracy.toFixed(1),
            fpRate: falsePositiveRate.toFixed(1),
            fnRate: falseNegativeRate.toFixed(1),
            gradeColor:
                accuracy > 80
                    ? "text-emerald-600"
                    : accuracy > 50
                      ? "text-amber-600"
                      : "text-rose-600",
            strokeColor:
                accuracy > 80
                    ? "#059669"
                    : accuracy > 50
                      ? "#d97706"
                      : "#e11d48", // Emerald / Amber / Rose
        };
    }

    function calculatePicStats(data: PicQuizResult) {
        const totalAttempts = data.correct + data.wrong;
        const accuracy =
            totalAttempts > 0
                ? ((data.correct - data.wrong * (1 / 3)) / 42) * 100
                : 0;
        const unanswered = 42 - totalAttempts;

        return {
            correctCount: data.correct,
            wrongCount: data.wrong,
            unansweredCount: unanswered,
            accuracy: accuracy.toFixed(1),
            gradeColor:
                accuracy > 80
                    ? "text-emerald-600"
                    : accuracy > 60
                      ? "text-amber-600"
                      : "text-rose-600",
            strokeColor:
                accuracy > 80
                    ? "#059669"
                    : accuracy > 60
                      ? "#d97706"
                      : "#e11d48",
        };
    }

    onMount(async () => {
        const d = new Date();
        const j = toJalaali(d);
        jalaliDate = `${j.jy}/${j.jm}/${j.jd}`;

        try {
            const account = await retreiveAccount();
            if (account) {
                first_name = account.first_name || "";
                last_name = account.last_name || "";
                age = account.age;
            }

            const res1: any = await retreiveQuizAnswer({
                quiz_type: "AcuTest_text",
            });
            const res2: any = await retreiveQuizAnswer({
                quiz_type: "AcuTest_pic",
            });
            data = { acu_text_result: res1, acu_pic_result: res2 };
            console.log(data);

            if (res1 && res1.no_no !== undefined) {
                textResult = res1;
                picResult = res2;
            } else {
                textResult = res2;
                picResult = res1;
            }
        } catch (error: any) {
            console.error("Error:", error);
            errorMsg = error.message || "خطا در دریافت اطلاعات";
        } finally {
            loading = false;
        }
    });

    // Helper for circle SVG
    const radius = 35;
    const circumference = 2 * Math.PI * radius;
    onMount(() => {
        updateTimers(); // Run immediately
        timerInterval = setInterval(updateTimers, 1000); // Run every second
    });

    onDestroy(() => {
        if (timerInterval) clearInterval(timerInterval);
    });
</script>

<svelte:head>
    <title>گزارش عملکرد | AcuTest</title>
</svelte:head>

<div
    class="min-h-screen bg-[#F5F3FF] font-['Vazirmatn'] text-slate-800 py-10 px-4 sm:px-6"
    dir="rtl"
>
    {#if loading}
        <!-- Loading -->
        <div class="flex flex-col items-center justify-center min-h-[50vh]">
            <div
                class="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"
            ></div>
            <p class="mt-4 text-purple-700 font-medium">
                در حال تحلیل نتایج...
            </p>
        </div>
    {:else if errorMsg}
        <!-- Error -->
        <div
            class="max-w-md mx-auto bg-white rounded-xl shadow-sm border border-rose-100 p-8 text-center"
        >
            <h3 class="text-lg font-bold text-rose-700 mb-2">
                خطا در بارگذاری
            </h3>
            <p class="text-slate-500 text-sm">{errorMsg}</p>
        </div>
    {:else}
        <!-- Content -->
        <div
            class="max-w-5xl mx-auto space-y-8"
            in:fly={{ y: 20, duration: 600 }}
        >
            <!-- Header -->
            <div class="text-center space-y-2 mb-8">
                <h1
                    class="text-3xl sm:text-4xl font-black text-purple-900 tracking-tight"
                >
                    گزارش جامع ارزیابی
                </h1>
                <p class="text-slate-500 font-medium">
                    تحلیل دقت و تمرکز شناختی
                </p>

                <div class="flex flex-wrap justify-center gap-3 mt-4 pt-4">
                    {#if first_name || last_name}
                        <div
                            class="bg-white px-4 py-1.5 rounded-full shadow-sm border border-purple-100 text-sm text-purple-900 font-semibold"
                        >
                            {first_name}
                            {last_name}
                        </div>
                    {/if}
                    <div
                        class="bg-white px-4 py-1.5 rounded-full shadow-sm border border-purple-100 text-sm text-purple-900 font-semibold"
                    >
                        {jalaliDate}
                    </div>
                    {#if age}
                        <div
                            class="bg-white px-4 py-1.5 rounded-full shadow-sm border border-purple-100 text-sm text-purple-900 font-semibold"
                        >
                            <span class="text-purple-400 font-normal">سن:</span>
                            {age}
                        </div>
                    {/if}
                </div>
            </div>

            <!-- CARD GRID -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 1. Picture Test Card -->
                {#if data.acu_pic_result?.quiz_time === "not_ended"}
                    <div
                        class="bg-white rounded-3xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between"
                    >
                        <div
                            class="flex flex-col items-center justify-center p-6 text-center"
                        >
                            <p class="text-lg font-bold text-gray-600 mb-2">
                                نتایج آزمون شما درحال آماده شدن است
                            </p>
                            <div
                                class="text-4xl font-mono font-bold text-primary"
                            >
                                {formatTime(picQuizRemaining)}
                            </div>
                            <p class="text-sm text-gray-400 mt-2">
                                لطفا شکیبا باشید...
                            </p>
                        </div>
                    </div>
                {:else if picResult && picStats}
                    {@const pTotal =
                        Number(picStats.correctCount) +
                        Number(picStats.wrongCount) +
                        Number(picStats.unansweredCount)}
                    {@const pCorrectLen =
                        (Number(picStats.correctCount) / pTotal) *
                        circumference}
                    {@const pWrongLen =
                        (Number(picStats.wrongCount) / pTotal) * circumference}
                    {@const pUnansweredLen =
                        (Number(picStats.unansweredCount) / pTotal) *
                        circumference}

                    <div
                        class="bg-white rounded-3xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between"
                    >
                        <div class="flex justify-between items-start mb-6">
                            <div>
                                <h2 class="text-lg font-bold text-slate-800">
                                    آزمون الگوهای تصویری
                                </h2>
                                <p class="text-xs text-slate-400 mt-1">
                                    تطبیق اشکال بصری
                                </p>
                            </div>

                            <!-- Circle Progress -->
                            <div
                                class="relative flex items-center justify-center"
                            >
                                <svg class="transform -rotate-90 w-24 h-24">
                                    <!-- Background Circle (Just in case) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f1f5f9"
                                        stroke-width="8"
                                        fill="transparent"
                                    />

                                    <!-- 1. CORRECT SEGMENT (Green) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#10b981"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{pCorrectLen} {circumference}"
                                        stroke-dashoffset="0"
                                        class="transition-all duration-1000 ease-out"
                                    />

                                    <!-- 2. WRONG SEGMENT (Red) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f43f5e"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{pWrongLen} {circumference}"
                                        stroke-dashoffset={-pCorrectLen}
                                        class="transition-all duration-1000 ease-out"
                                    />

                                    <!-- 3. UNANSWERED SEGMENT (Gray) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#cbd5e1"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{pUnansweredLen} {circumference}"
                                        stroke-dashoffset={-(
                                            pCorrectLen + pWrongLen
                                        )}
                                        class="transition-all duration-1000 ease-out"
                                    />
                                </svg>
                                <!-- Percentage Text in Middle -->
                                <span
                                    class="absolute text-lg font-black text-slate-700"
                                >
                                    {Math.round(Number(picStats.accuracy))}%
                                </span>
                            </div>
                        </div>

                        <!-- 3-Column Stats -->
                        <div class="grid grid-cols-3 gap-2 mt-auto">
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-emerald-600"
                                    >{picStats.correctCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-500 font-medium"
                                    >صحیح</span
                                >
                            </div>
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-rose-500"
                                    >{picStats.wrongCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-500 font-medium"
                                    >غلط</span
                                >
                            </div>
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-slate-500"
                                    >{picStats.unansweredCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-400 font-medium"
                                    >بی‌پاسخ</span
                                >
                            </div>
                        </div>
                    </div>
                {/if}

                <!-- 2. Text Test Card -->
                {#if data.acu_text_result?.quiz_time === "not_ended"}
                    <div
                        class="bg-white rounded-3xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between"
                    >
                        <div
                            class="flex flex-col items-center justify-center p-6 text-center"
                        >
                            <p class="text-lg font-bold text-gray-600 mb-2">
                                نتایج آزمون شما درحال آماده شدن است
                            </p>
                            <div
                                class="text-4xl font-mono font-bold text-primary"
                            >
                                {formatTime(textQuizRemaining)}
                            </div>
                            <p class="text-sm text-gray-400 mt-2">
                                لطفا شکیبا باشید...
                            </p>
                        </div>
                    </div>
                {:else if textResult && textStats}
                    {@const tTotal =
                        Number(textStats.correctCount) +
                        Number(textStats.wrongCount) +
                        Number(textStats.unansweredCount)}
                    {@const tCorrectLen =
                        (Number(textStats.correctCount) / tTotal) *
                        circumference}
                    {@const tWrongLen =
                        (Number(textStats.wrongCount) / tTotal) * circumference}
                    {@const tUnansweredLen =
                        (Number(textStats.unansweredCount) / tTotal) *
                        circumference}

                    <div
                        class="bg-white rounded-3xl p-6 shadow-sm border border-slate-200 flex flex-col justify-between"
                    >
                        <div class="flex justify-between items-start mb-6">
                            <div>
                                <h2 class="text-lg font-bold text-slate-800">
                                    آزمون تایید متنی
                                </h2>
                                <p class="text-xs text-slate-400 mt-1">
                                    شناسایی خطاهای شناختی
                                </p>
                            </div>

                            <!-- Circle Progress -->
                            <div
                                class="relative flex items-center justify-center"
                            >
                                <svg class="transform -rotate-90 w-24 h-24">
                                    <!-- Background Circle -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f1f5f9"
                                        stroke-width="8"
                                        fill="transparent"
                                    />

                                    <!-- 1. CORRECT SEGMENT (Green) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#10b981"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{tCorrectLen} {circumference}"
                                        stroke-dashoffset="0"
                                        class="transition-all duration-1000 ease-out"
                                    />

                                    <!-- 2. WRONG SEGMENT (Red) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f43f5e"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{tWrongLen} {circumference}"
                                        stroke-dashoffset={-tCorrectLen}
                                        class="transition-all duration-1000 ease-out"
                                    />

                                    <!-- 3. UNANSWERED SEGMENT (Gray) -->
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#cbd5e1"
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray="{tUnansweredLen} {circumference}"
                                        stroke-dashoffset={-(
                                            tCorrectLen + tWrongLen
                                        )}
                                        class="transition-all duration-1000 ease-out"
                                    />
                                </svg>
                                <span
                                    class="absolute text-lg font-black text-slate-700"
                                >
                                    {Math.round(Number(textStats.accuracy))}%
                                </span>
                            </div>
                        </div>
                        <!-- 3-Column Stats -->
                        <div class="grid grid-cols-3 gap-2 mt-auto">
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-emerald-600"
                                    >{textStats.correctCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-500 font-medium"
                                    >صحیح</span
                                >
                            </div>
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-rose-500"
                                    >{textStats.wrongCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-500 font-medium"
                                    >غلط</span
                                >
                            </div>
                            <div
                                class="bg-slate-50 rounded-2xl p-3 text-center border border-slate-100"
                            >
                                <span
                                    class="block text-xl font-bold text-slate-500"
                                    >{textStats.unansweredCount}</span
                                >
                                <span
                                    class="text-[10px] text-slate-400 font-medium"
                                    >بی‌پاسخ</span
                                >
                            </div>
                        </div>
                    </div>
                {/if}
            </div>

            <!-- DETAILED ANALYSIS (2x2 Matrix Layout) -->
            {#if textResult && textStats}
                <div
                    class="bg-white rounded-3xl p-8 shadow-sm border border-slate-200"
                >
                    <div
                        class="flex items-center gap-3 mb-8 border-b border-slate-100 pb-4"
                    >
                        <div class="w-2 h-8 bg-purple-600 rounded-full"></div>
                        <h3 class="text-xl font-bold text-slate-800">
                            تحلیل ماتریس پاسخ‌دهی
                        </h3>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-5 gap-8">
                        <!-- LEFT SIDE: 2x2 Matrix -->
                        <div class="lg:col-span-3">
                            <div class="grid grid-cols-2 gap-4 h-full">
                                <!-- Top Left: Yes/Yes (Green) -->
                                <div
                                    class="flex flex-col p-5 bg-emerald-50/50 rounded-2xl border border-emerald-100"
                                >
                                    <span
                                        class="text-xs font-bold text-emerald-800/60 mb-2"
                                        >تطابق صحیح (Hit)</span
                                    >
                                    <div class="mt-auto">
                                        <span
                                            class="text-3xl font-black text-emerald-700"
                                            >{textResult.yes_yes}</span
                                        >
                                        <span
                                            class="text-xs text-emerald-600 mr-1"
                                            >مورد</span
                                        >
                                    </div>
                                </div>

                                <!-- Top Right: No/Yes (Amber - False Alarm) -->
                                <div
                                    class="flex flex-col p-5 bg-amber-50/50 rounded-2xl border border-amber-100"
                                >
                                    <span
                                        class="text-xs font-bold text-amber-800/60 mb-2"
                                        >تشخیص غلط (Impulsivity)</span
                                    >
                                    <div class="mt-auto">
                                        <span
                                            class="text-3xl font-black text-amber-600"
                                            >{textResult.no_yes}</span
                                        >
                                        <span
                                            class="text-xs text-amber-600 mr-1"
                                            >مورد</span
                                        >
                                    </div>
                                </div>

                                <!-- Bottom Left: Yes/No (Rose - Miss) -->
                                <div
                                    class="flex flex-col p-5 bg-rose-50/50 rounded-2xl border border-rose-100"
                                >
                                    <span
                                        class="text-xs font-bold text-rose-800/60 mb-2"
                                        >عدم تشخیص (Inattention)</span
                                    >
                                    <div class="mt-auto">
                                        <span
                                            class="text-3xl font-black text-rose-600"
                                            >{textResult.yes_no}</span
                                        >
                                        <span class="text-xs text-rose-600 mr-1"
                                            >مورد</span
                                        >
                                    </div>
                                </div>

                                <!-- Bottom Right: No/No (Green) -->
                                <div
                                    class="flex flex-col p-5 bg-emerald-50/50 rounded-2xl border border-emerald-100"
                                >
                                    <span
                                        class="text-xs font-bold text-emerald-800/60 mb-2"
                                        >رد صحیح (Rejection)</span
                                    >
                                    <div class="mt-auto">
                                        <span
                                            class="text-3xl font-black text-emerald-700"
                                            >{textResult.no_no}</span
                                        >
                                        <span
                                            class="text-xs text-emerald-600 mr-1"
                                            >مورد</span
                                        >
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- RIGHT SIDE: Bias Bars -->
                        <div
                            class="lg:col-span-2 flex flex-col justify-center gap-6 py-2"
                        >
                            <!-- Impulsivity Card -->
                            <div
                                class="p-4 rounded-2xl bg-slate-50 border border-slate-100"
                            >
                                <div
                                    class="flex justify-between items-center mb-2"
                                >
                                    <span
                                        class="text-sm font-bold text-slate-700"
                                        >تکانشگری</span
                                    >
                                    <span
                                        class="text-xs px-2 py-0.5 rounded bg-white text-slate-500 font-mono shadow-sm"
                                        >{textStats.fpRate}%</span
                                    >
                                </div>
                                <div
                                    class="h-2 w-full bg-slate-200 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="h-full rounded-full {Number(
                                            textStats.fpRate,
                                        ) > 15
                                            ? 'bg-amber-500'
                                            : 'bg-purple-400'}"
                                        style="width: {textStats.fpRate}%"
                                    ></div>
                                </div>
                                <p
                                    class="text-xs text-slate-400 mt-2 leading-relaxed"
                                >
                                    تمایل به پاسخ مثبت عجولانه در زمانی که پاسخ
                                    صحیح "خیر" است.
                                </p>
                            </div>

                            <!-- Inattention Card -->
                            <div
                                class="p-4 rounded-2xl bg-slate-50 border border-slate-100"
                            >
                                <div
                                    class="flex justify-between items-center mb-2"
                                >
                                    <span
                                        class="text-sm font-bold text-slate-700"
                                        >بی‌توجهی</span
                                    >
                                    <span
                                        class="text-xs px-2 py-0.5 rounded bg-white text-slate-500 font-mono shadow-sm"
                                        >{textStats.fnRate}%</span
                                    >
                                </div>
                                <div
                                    class="h-2 w-full bg-slate-200 rounded-full overflow-hidden"
                                >
                                    <div
                                        class="h-full rounded-full {Number(
                                            textStats.fnRate,
                                        ) > 15
                                            ? 'bg-rose-500'
                                            : 'bg-purple-400'}"
                                        style="width: {textStats.fnRate}%"
                                    ></div>
                                </div>
                                <p
                                    class="text-xs text-slate-400 mt-2 leading-relaxed"
                                >
                                    از قلم انداختن پاسخ‌های صحیح در زمانی که
                                    باید "بله" را انتخاب کنید.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap");
    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }
</style>
