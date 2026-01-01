<script lang="ts">
    import { goto } from "$app/navigation";
    import { fly } from "svelte/transition";
    import { startQuiz } from "$lib/utils/api/quiz-apis";

    let isLoading = false;
    let promise: Promise<void>;

    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "AcuTest_text",
        });
        await promise;
        window.location.href = "/AcuTest/Text";
    };

    let currentStep = 1;
    const totalSteps = 6;

    const tutorialSteps = [
        {
            title: "به بخش اول آزمون دقت خوش آمدید",
            description:
                "این آزمون برای سنجش سرعت و دقت شما در تطبیق اطلاعات طراحی شده است. شما باید بررسی کنید که آیا اطلاعات نمایش داده شده در دو ستون چپ و راست با هم مطابقت دارند یا خیر.\nبرای پاسخگویی مناسب باید تمرکز بالایی داشته باشید.",
        },
        {
            title: "نحوه انجام آزمون",
            description:
                "در هر مرحله، دو عبارت در سمت راست و چپ به شما نمایش داده می‌شود. وظیفه شما مقایسه دقیق و سریع آن‌هاست. شما باید تصمیم بگیرید که آیا این دو عبارت دقیقاً یکسان هستند یا خیر.",
        },
        {
            title: "حالت یکسان",
            description:
                "اگر دو عبارت نمایش داده شده **کاملاً یکسان** بودند (حتی از نظر بزرگی و کوچکی حروف و علائم‌نگارشی)، باید دکمه سبز رنگ با علامت (✓) را انتخاب کنید.",
        },
        {
            title: "حالت متفاوت",
            description:
                "اگر **کوچکترین تفاوتی** بین دو عبارت وجود داشت (مثل یک غلط املایی، جابجایی حروف یا تفاوت در آن‌ها)، باید دکمه قرمز رنگ با علامت (✗) را انتخاب کنید.",
        },
        {
            title: "مدت زمان و شرایط",
            description:
                "مدت زمان کلی این آزمون **۶ دقیقه** است. تعداد سوالات زیاد است، بنابراین باید سعی کنید تعادلی بین سرعت و دقت خود برقرار کنید.",
        },
        {
            title: "آماده‌اید؟",
            description:
                "زمان شما بلافاصله پس از فشردن دکمه «شروع آزمون» آغاز خواهد شد. لطفاً مطمئن شوید که در محیطی آرام هستید و تمرکز کافی دارید.",
        },
    ];

    function nextStep() {
        if (currentStep < totalSteps) {
            currentStep++;
            direction = 1;
        }
    }

    function prevStep() {
        if (currentStep > 1) {
            currentStep--;
            direction = -1;
        }
    }

    // Animation helpers
    let animate = false;
    let direction = 1; // 1 for next, -1 for prev
    $: {
        animate = false;
        // Trigger reflow to restart animation when step changes
        setTimeout(() => (animate = true), 50);
    }
</script>

<svelte:head>
    <title>راهنمای بخش اول آزمون دقت (AcuTest)</title>
</svelte:head>

<div
    class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-slate-900 font-['Vazirmatn']"
    dir="rtl"
>
    <div
        class="w-full max-w-2xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 sm:p-10 transition-all duration-300 overflow-y-auto border border-slate-200 dark:border-slate-700"
    >
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-slate-800 dark:text-white">
                راهنمای بخش اول آزمون دقت
            </h2>
            <span class="text-sm font-medium text-slate-500 dark:text-slate-400"
                >مرحله {currentStep} از {totalSteps}</span
            >
        </div>

        <!-- Progress Bar -->
        <div
            class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2.5 mb-8"
        >
            <div
                class="bg-indigo-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                style="width: {(currentStep / totalSteps) * 100}%"
            />
        </div>

        <!-- Content Area -->
        <div class="relative min-h-[350px] sm:min-h-[380px] overflow-hidden">
            {#key currentStep}
                <div
                    class="absolute w-full"
                    in:fly={{
                        x: direction === 1 ? 300 : -300,
                        duration: 300,
                        delay: 300,
                    }}
                    out:fly={{ x: direction === 1 ? -300 : 300, duration: 300 }}
                >
                    <h3
                        class="text-xl sm:text-2xl font-semibold text-slate-700 dark:text-slate-100 mb-4"
                    >
                        {tutorialSteps[currentStep - 1].title}
                    </h3>
                    <p
                        class="text-base text-slate-600 dark:text-slate-300 mb-6 leading-relaxed whitespace-pre-line text-justify"
                    >
                        {tutorialSteps[currentStep - 1].description}
                    </p>

                    <!-- Visual Simulations -->
                    <div
                        class="h-48 w-full bg-slate-50 dark:bg-slate-700/30 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-center overflow-hidden relative"
                    >
                        <!-- Step 1: Icon -->
                        {#if currentStep === 1}
                            <div
                                class="flex items-center justify-center text-indigo-500 dark:text-indigo-400"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="w-24 h-24 opacity-80"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    stroke-width="1.5"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                    />
                                </svg>
                            </div>
                        {/if}

                        <!-- Step 2: Static Example -->
                        {#if currentStep === 2}
                            <div
                                class="flex w-full items-center justify-between gap-2 px-4 opacity-70"
                            >
                                <div
                                    class="bg-white dark:bg-slate-600 p-3 rounded shadow-sm flex-1 text-center font-mono text-slate-600 dark:text-slate-200"
                                >
                                    david's block
                                </div>
                                <div class="flex gap-2">
                                    <div
                                        class="w-10 h-10 rounded border-2 border-slate-300 flex items-center justify-center text-slate-300"
                                    >
                                        ✗
                                    </div>
                                    <div
                                        class="w-10 h-10 rounded border-2 border-slate-300 flex items-center justify-center text-slate-300"
                                    >
                                        ✓
                                    </div>
                                </div>
                                <div
                                    class="bg-white dark:bg-slate-600 p-3 rounded shadow-sm flex-1 text-center font-mono text-slate-600 dark:text-slate-200"
                                >
                                    davids block
                                </div>
                            </div>
                        {/if}

                        <!-- Step 3: Animation (SAME) -->
                        {#if currentStep === 3 && animate}
                            <div
                                class="relative w-full max-w-md flex flex-col items-center"
                            >
                                <div class="pointer-check" />
                                <div
                                    class="flex w-full items-center justify-between gap-2 sm:gap-4 px-2"
                                >
                                    <!-- Right Text -->
                                    <div
                                        class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 p-3 rounded-lg shadow-sm flex-1 text-center font-mono text-lg font-bold text-slate-700 dark:text-slate-200"
                                    >
                                        Mr.sfaiee
                                    </div>

                                    <!-- Buttons -->
                                    <div class="flex gap-3">
                                        <!-- Correct Button (Target) -->
                                        <!-- Wrong Button -->
                                        <div
                                            class="w-12 h-12 rounded-lg border-2 border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-300 flex items-center justify-center text-2xl"
                                        >
                                            ✗
                                        </div>
                                        <div
                                            class="w-12 h-12 rounded-lg border-2 flex items-center justify-center text-2xl font-bold transition-colors duration-300 btn-check-animate"
                                        >
                                            ✓
                                        </div>
                                    </div>

                                    <!-- Left Text -->
                                    <div
                                        class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 p-3 rounded-lg shadow-sm flex-1 text-center font-mono text-lg font-bold text-slate-700 dark:text-slate-200"
                                    >
                                        Mr.sfaiee
                                    </div>
                                </div>
                                <div
                                    class="mt-4 text-xs font-bold text-green-600 bg-green-100 px-3 py-1 rounded-full animate-pulse"
                                >
                                    کاملاً یکسان
                                </div>
                            </div>
                        {/if}

                        <!-- Step 4: Animation (DIFFERENT) -->
                        {#if currentStep === 4 && animate}
                            <div
                                class="relative w-full max-w-md flex flex-col items-center"
                            >
                                <div class="pointer-cross" />
                                <div
                                    class="flex w-full items-center justify-between gap-2 sm:gap-4 px-2"
                                >
                                    <!-- Right Text -->
                                    <div
                                        class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 p-3 rounded-lg shadow-sm flex-1 text-center font-mono text-lg font-bold text-slate-700 dark:text-slate-200"
                                    >
                                        Wilson
                                    </div>

                                    <!-- Buttons -->
                                    <div class="flex gap-3">
                                        <!-- Correct Button -->
                                        <!-- Wrong Button (Target) -->
                                        <div
                                            class="w-12 h-12 rounded-lg border-2 flex items-center justify-center text-2xl font-bold transition-colors duration-300 btn-cross-animate"
                                        >
                                            ✗
                                        </div>
                                        <div
                                            class="w-12 h-12 rounded-lg border-2 border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-300 flex items-center justify-center text-2xl"
                                        >
                                            ✓
                                        </div>
                                    </div>

                                    <!-- Left Text (Different) -->
                                    <div
                                        class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 p-3 rounded-lg shadow-sm flex-1 text-center font-mono text-lg font-bold text-slate-700 dark:text-slate-200 relative overflow-hidden"
                                    >
                                        Wilison
                                        <!-- Highlight diff -->
                                        <span
                                            class="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-1 bg-red-400 opacity-50"
                                        ></span>
                                    </div>
                                </div>
                                <div
                                    class="mt-4 text-xs font-bold text-red-600 bg-red-100 px-3 py-1 rounded-full animate-pulse"
                                >
                                    متفاوت (غلط املایی)
                                </div>
                            </div>
                        {/if}

                        <!-- Step 5: Time -->
                        {#if currentStep === 5}
                            <div
                                class="flex flex-col items-center justify-center"
                            >
                                <div
                                    class="w-20 h-20 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center mb-3 animate-bounce"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="w-10 h-10 text-indigo-600 dark:text-indigo-300"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                        />
                                    </svg>
                                </div>
                                <span
                                    class="text-3xl font-bold text-indigo-700 dark:text-indigo-300"
                                    >۶ دقیقه</span
                                >
                                <span
                                    class="text-sm text-slate-500 mt-2 dark:text-slate-400"
                                    >زمان کل آزمون</span
                                >
                            </div>
                        {/if}

                        <!-- Step 6: Ready -->
                        {#if currentStep === 6}
                            <div
                                class="flex items-center justify-center text-indigo-600 dark:text-indigo-400"
                            >
                                <div class="relative">
                                    <span
                                        class="absolute inset-0 rounded-full bg-indigo-400 opacity-20 animate-ping"
                                    ></span>
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="80"
                                        height="80"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="1.5"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path
                                            d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"
                                        />
                                    </svg>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            {/key}
        </div>

        <!-- Footer / Navigation -->
        <div
            class="flex justify-between items-center pt-8 mt-8 border-t border-slate-200 dark:border-slate-700"
        >
            <button
                on:click={prevStep}
                class="py-2 px-5 rounded-lg font-semibold text-slate-700 dark:text-slate-200 bg-slate-200 dark:bg-slate-600 hover:bg-slate-300 dark:hover:bg-slate-500 transition-all
               disabled:opacity-0 disabled:pointer-events-none"
                disabled={currentStep === 1}
            >
                قبلی
            </button>

            {#if currentStep === totalSteps}
                <button
                    on:click={startQuizHandler}
                    disabled={isLoading}
                    class="py-2 px-6 rounded-lg font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-all disabled:bg-indigo-400 flex items-center gap-2 shadow-lg hover:shadow-indigo-500/30"
                >
                    {#if isLoading}
                        <div
                            class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
                        ></div>
                        <span>درحال آماده‌سازی...</span>
                    {:else}
                        شروع آزمون
                    {/if}
                </button>
            {:else}
                <button
                    on:click={nextStep}
                    class="py-2 px-5 rounded-lg font-semibold text-white bg-indigo-600 hover:bg-indigo-700 transition-all shadow-md hover:shadow-indigo-500/20"
                >
                    بعدی
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    /* Import Font */
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap");

    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }

    /* Common Pointer Style */
    .pointer-check,
    .pointer-cross {
        width: 28px;
        height: 28px;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'><path fill='white' stroke='black' stroke-width='1.5' d='M2.5,2.5l23,10l-10,3l-3,10Z'/></svg>");
        background-size: contain;
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 20;
        opacity: 0;
    }

    /* --- Animations for Match Case (Green) --- */
    .pointer-check {
        animation: click-green-btn 2.5s ease-in-out infinite;
    }

    .btn-check-animate {
        animation: green-btn-state 2.5s ease-in-out infinite;
    }

    @keyframes click-red-btn {
        0% {
            opacity: 0;
            transform: translate(-50%, 50px) scale(1);
        }
        20% {
            opacity: 1;
            /* Move near green button (center + slight right offset if needed) */
            transform: translate(15px, -15px) scale(1);
        }
        40% {
            /* Click */
            transform: translate(15px, -15px) scale(0.8);
        }
        50% {
            /* Release */
            transform: translate(15px, -15px) scale(1);
        }
        80% {
            opacity: 1;
        }
        90%,
        100% {
            opacity: 0;
        }
    }

    @keyframes green-btn-state {
        0%,
        35% {
            /* Default state */
            background-color: #f8fafc; /* slate-50 */
            border-color: #e2e8f0; /* slate-200 */
            color: #cbd5e1; /* slate-300 */
        }
        36% {
            /* Clicked state starts */
            background-color: #dcfce7; /* green-100 */
            border-color: #22c55e; /* green-500 */
            color: #15803d; /* green-700 */
            transform: scale(0.95);
        }
        45% {
            transform: scale(1);
        }
        100% {
            /* Stay green */
            background-color: #dcfce7;
            border-color: #22c55e;
            color: #15803d;
        }
    }

    /* --- Animations for Mismatch Case (Red) --- */
    .pointer-cross {
        animation: click-red-btn 2.5s ease-in-out infinite;
    }

    .btn-cross-animate {
        animation: red-btn-state 2.5s ease-in-out infinite;
    }

    @keyframes click-green-btn {
        0% {
            opacity: 0;
            transform: translate(-50%, 50px) scale(1);
        }
        20% {
            opacity: 1;
            /* Move near red button (center - slight left offset if needed) */
            transform: translate(-45px, -15px) scale(1);
        }
        40% {
            /* Click */
            transform: translate(-45px, -15px) scale(0.8);
        }
        50% {
            /* Release */
            transform: translate(-45px, -15px) scale(1);
        }
        80% {
            opacity: 1;
        }
        90%,
        100% {
            opacity: 0;
        }
    }

    @keyframes red-btn-state {
        0%,
        35% {
            /* Default state */
            background-color: #f8fafc;
            border-color: #e2e8f0;
            color: #cbd5e1;
        }
        36% {
            /* Clicked state starts */
            background-color: #fee2e2; /* red-100 */
            border-color: #ef4444; /* red-500 */
            color: #b91c1c; /* red-700 */
            transform: scale(0.95);
        }
        45% {
            transform: scale(1);
        }
        100% {
            /* Stay red */
            background-color: #fee2e2;
            border-color: #ef4444;
            color: #b91c1c;
        }
    }
</style>
