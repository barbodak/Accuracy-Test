<script lang="ts">
    import {
        retreiveQuizAnswer,
        retreiveAccount,
    } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import { toJalaali } from "jalaali-js";

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
        const unanswered = 90 - calculatedCorrect - calculatedCorrect;

        const totalAttempts = calculatedCorrect + calculatedWrong;
        const accuracy =
            totalAttempts > 0 ? (calculatedCorrect / totalAttempts) * 100 : 0;

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
            totalAttempts > 0 ? (data.correct / totalAttempts) * 100 : 0;
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
                {#if picResult && picStats}
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
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f1f5f9"
                                        stroke-width="8"
                                        fill="transparent"
                                    />
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke={picStats.strokeColor}
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray={circumference}
                                        stroke-dashoffset={circumference -
                                            (Number(picStats.accuracy) / 100) *
                                                circumference}
                                        class="transition-all duration-1000 ease-out"
                                    />
                                </svg>
                                <span
                                    class="absolute text-lg font-black text-slate-700"
                                    >{Math.round(
                                        Number(picStats.accuracy),
                                    )}%</span
                                >
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
                {#if textResult && textStats}
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
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke="#f1f5f9"
                                        stroke-width="8"
                                        fill="transparent"
                                    />
                                    <circle
                                        cx="48"
                                        cy="48"
                                        r={radius}
                                        stroke={textStats.strokeColor}
                                        stroke-width="8"
                                        fill="transparent"
                                        stroke-dasharray={circumference}
                                        stroke-dashoffset={circumference -
                                            (Number(textStats.accuracy) / 100) *
                                                circumference}
                                        class="transition-all duration-1000 ease-out"
                                    />
                                </svg>
                                <span
                                    class="absolute text-lg font-black text-slate-700"
                                    >{Math.round(
                                        Number(textStats.accuracy),
                                    )}%</span
                                >
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
