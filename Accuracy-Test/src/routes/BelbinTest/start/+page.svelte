<script>
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    import { fade, fly } from "svelte/transition";
    import { onMount } from "svelte";

    let currentStep = 1;
    let direction = 1;
    let totalSteps = 6;
    let promise = null;

    // متغیرهای انیمیشن مرحله 4
    let demoScore = 4;
    let clickAnimation = false;
    let step4Interval;

    const tutorialSteps = [
        {
            title: "به پرسشنامه بلبین خوش آمدید",
            description:
                "شما در حال ورود به راهنمای پرسشنامه بلبین هستید. این پرسشنامه به شما کمک می‌کند تا نقش‌ها و رفتارهای تیمی خود را بهتر بشناسید.",
        },
        {
            title: "ساختار پرسشنامه",
            description:
                "این پرسشنامه شامل ۷ بخش است. در هر بخش، ۸ جمله (گزینه) به شما نمایش داده می‌شود که باید آن‌ها را ارزیابی کنید.",
        },
        {
            title: "تخصیص امتیاز",
            description:
                "شما برای امتیازدهی به گزینه‌های هر صفحه ۱۰ امتیاز بودجه دارید که شکل توزیع آن بین گزینه‌ها با شماست. اما جمع امتیازات باید دقیقاً ۱۰ باشد، نه بیشتر نه کمتر. گزینه‌هایی که امتیاز بیشتری دریافت می‌کنند اولویت‌های بالاتر شما هستند و گزینه‌هایی که امتیاز نمی‌گیرند درباره شما صادق نخواهند بود.",
        },
        {
            title: "نحوه امتیازدهی",
            description:
                "برای تغییر امتیاز هر گزینه، به سادگی می‌توانید از دکمه‌های (+) و (-) که در کنار امتیاز هر گزینه قرار گرفته‌اند استفاده کنید.",
        },
        {
            title: "پیمایش و مطالعه دقیق",
            description:
                "لطفاً حتماً در هر مرحله صفحه را به پایین اسکرول (پیمایش) کنید و تمام گزینه‌ها را با دقت بخوانید تا هیچ گزینه‌ای از دید شما پنهان نماند.",
        },
        {
            title: "آماده‌اید؟",
            description:
                "آیا برای شروع آماده‌اید؟ لطفاً آرامش خود را حفظ کنید و با زمان کافی و دقت پرسشنامه را تکمیل کنید. هیچ پاسخ درست یا غلطی در اینجا وجود ندارد.",
        },
    ];

    $: if (currentStep === 4) {
        demoScore = 4;
        clickAnimation = false;
        if (step4Interval) clearInterval(step4Interval);

        step4Interval = setInterval(() => {
            // Faster click simulation
            clickAnimation = true;
            setTimeout(() => {
                demoScore = 3;
                clickAnimation = false;
            }, 150); // Faster push

            // Return to initial state faster
            setTimeout(() => {
                demoScore = 4;
            }, 1000);
        }, 1500); // Shorter loop cycle
    } else {
        if (step4Interval) clearInterval(step4Interval);
    }

    function nextStep() {
        if (currentStep < totalSteps) {
            direction = 1;
            currentStep++;
        }
    }

    function prevStep() {
        if (currentStep > 1) {
            direction = -1;
            currentStep--;
        }
    }

    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "BelbinTest",
        });
        await promise;
        window.location.href = "/BelbinTest";
    };
</script>

<div
    dir="rtl"
    class="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 flex items-center justify-center p-4 sm:p-8"
>
    <div
        class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col h-[650px]"
    >
        <!-- هدر و نوار پیشرفت -->
        <div class="p-6 border-b border-slate-100 dark:border-slate-700">
            <div class="flex justify-between items-center mb-5">
                <!-- متن هدر بزرگ‌تر شده است -->
                <h1
                    class="text-3xl sm:text-4xl font-extrabold text-slate-800 dark:text-white"
                >
                    راهنمای پرسشنامه
                </h1>
                <span
                    class="text-sm sm:text-base font-medium text-slate-500 dark:text-slate-400"
                    >مرحله {currentStep} از {totalSteps}</span
                >
            </div>
            <div
                class="w-full h-2.5 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden"
            >
                <div
                    class="h-full bg-blue-500 transition-all duration-500 ease-out"
                    style="width: {(currentStep / totalSteps) * 100}%"
                ></div>
            </div>
        </div>

        <!-- محتوای اصلی -->
        <div class="flex-1 relative overflow-hidden bg-white dark:bg-slate-800">
            {#key currentStep}
                <div
                    class="absolute inset-0 p-6 flex flex-col"
                    in:fly={{
                        x: direction === 1 ? -300 : 300,
                        duration: 400,
                        delay: 100,
                    }}
                    out:fly={{ x: direction === 1 ? 300 : -300, duration: 400 }}
                >
                    <div class="mb-8 text-center min-h-[100px]">
                        <h2
                            class="text-2xl font-bold mb-4 text-blue-600 dark:text-blue-400"
                        >
                            {tutorialSteps[currentStep - 1].title}
                        </h2>
                        <p
                            class="text-slate-600 dark:text-slate-300 leading-relaxed text-base sm:text-lg max-w-2xl mx-auto"
                        >
                            {tutorialSteps[currentStep - 1].description}
                        </p>
                    </div>

                    <div
                        class="flex-1 relative bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-slate-100 dark:border-slate-700 p-6 flex items-center justify-center overflow-hidden"
                    >
                        {#if currentStep === 1}
                            <div
                                class="flex flex-col items-center justify-center h-full space-y-4"
                            >
                                <div
                                    class="w-36 h-36 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center shadow-lg transform transition-transform hover:scale-105"
                                >
                                    <span
                                        class="text-4xl font-bold text-blue-600 dark:text-blue-300"
                                        >Belbin</span
                                    >
                                </div>
                            </div>

                            <!-- مرحله 2: لیست زیر هم -->
                        {:else if currentStep === 2}
                            <div
                                class="flex flex-col items-center justify-center h-full space-y-3"
                            >
                                <div
                                    class="w-64 bg-white dark:bg-slate-700 p-4 rounded-2xl shadow-xl flex flex-col gap-3 border border-slate-200 dark:border-slate-600"
                                >
                                    <div
                                        class="h-6 w-full bg-slate-300 dark:bg-slate-500 rounded mb-1"
                                    ></div>
                                    <!-- Question placeholder -->
                                    <div class="flex flex-col gap-2 w-full">
                                        <!-- Changed Array(8) to Array(5) -->
                                        {#each Array(5) as _}
                                            <div
                                                class="h-3 w-full bg-blue-200 dark:bg-blue-800 rounded"
                                            ></div>
                                        {/each}
                                    </div>
                                </div>
                                <span
                                    class="text-sm font-medium text-slate-500 dark:text-slate-400"
                                    >۷ بخش - هر بخش ۸ گزینه</span
                                >
                            </div>
                        {:else if currentStep === 3}
                            <div
                                class="flex flex-col items-center justify-center h-full space-y-8"
                            >
                                <div
                                    class="text-center bg-white dark:bg-slate-700 px-8 py-4 rounded-2xl shadow-md border border-slate-100 dark:border-slate-600"
                                >
                                    <p class="text-lg mb-2 font-medium">
                                        بودجه باقیمانده
                                    </p>
                                    <div
                                        class="text-5xl font-bold text-green-500"
                                    >
                                        ۱۰ / ۱۰
                                    </div>
                                </div>
                                <div class="flex gap-4">
                                    <div
                                        class="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-xl flex items-center justify-center font-bold text-2xl text-blue-700 dark:text-blue-300 shadow-sm border border-blue-200 dark:border-blue-800"
                                    >
                                        ۵
                                    </div>
                                    <div
                                        class="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-xl flex items-center justify-center font-bold text-2xl text-blue-700 dark:text-blue-300 shadow-sm border border-blue-200 dark:border-blue-800"
                                    >
                                        ۳
                                    </div>
                                    <div
                                        class="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-xl flex items-center justify-center font-bold text-2xl text-blue-700 dark:text-blue-300 shadow-sm border border-blue-200 dark:border-blue-800"
                                    >
                                        ۲
                                    </div>
                                </div>
                            </div>

                            <!-- مرحله 4: انیمیشن کلیک، تغییر عدد و بازگشت -->
                        {:else if currentStep === 4}
                            <div
                                class="flex flex-col items-center justify-center h-full space-y-4"
                            >
                                <div
                                    class="flex items-center gap-6 bg-white dark:bg-slate-700 p-6 rounded-3xl shadow-xl border border-slate-200 dark:border-slate-600"
                                >
                                    <div class="relative">
                                        <div
                                            class="w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400 flex items-center justify-center text-4xl font-bold transition-transform duration-150 {clickAnimation
                                                ? 'scale-75 bg-red-300 dark:bg-red-800'
                                                : ''}"
                                        >
                                            -
                                        </div>
                                        <!-- Clicking hand icon -->
                                        <div
                                            class="absolute -bottom-6 -right-2 text-3xl transition-transform duration-150 z-20 {clickAnimation
                                                ? 'scale-90 translate-y-0'
                                                : 'translate-y-4'}"
                                        >
                                            👆
                                        </div>
                                    </div>
                                    <span
                                        class="text-5xl font-bold w-12 text-center transition-all duration-150"
                                        >{demoScore}</span
                                    >
                                    <div
                                        class="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400 flex items-center justify-center text-4xl font-bold"
                                    >
                                        +
                                    </div>
                                </div>
                            </div>
                            <!-- مرحله 5: انیمیشن واضح اسکرول -->
                        {:else if currentStep === 5}
                            <div
                                class="flex items-center justify-center h-full w-full"
                            >
                                <div
                                    class="w-64 h-72 bg-white dark:bg-slate-700 border-4 border-slate-200 dark:border-slate-600 rounded-3xl overflow-hidden relative shadow-inner"
                                >
                                    <!-- نوار اسکرول متحرک -->
                                    <div
                                        class="absolute top-0 right-1.5 w-2 h-16 bg-blue-500 rounded-full z-10 scroll-thumb"
                                    ></div>
                                    <!-- محتوایی که اسکرول می‌شود -->
                                    <div
                                        class="p-4 space-y-4 w-full scroll-content"
                                    >
                                        {#each Array(10) as _, i}
                                            <div
                                                class="h-8 w-full {i % 2 === 0
                                                    ? 'bg-slate-100 dark:bg-slate-600'
                                                    : 'bg-slate-200 dark:bg-slate-500'} rounded-lg"
                                            ></div>
                                        {/each}
                                    </div>
                                </div>
                            </div>
                        {:else if currentStep === 6}
                            <div
                                class="flex flex-col items-center justify-center h-full space-y-6"
                            >
                                <div
                                    class="w-32 h-32 bg-green-100 dark:bg-green-900/50 rounded-full flex items-center justify-center shadow-xl transform hover:scale-110 transition duration-300 border-[6px] border-white dark:border-slate-800"
                                >
                                    <svg
                                        class="w-16 h-16 text-green-600 dark:text-green-400"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="3"
                                            d="M5 13l4 4L19 7"
                                        ></path>
                                    </svg>
                                </div>
                                <p
                                    class="text-2xl font-bold text-slate-700 dark:text-slate-300"
                                >
                                    موفق باشید!
                                </p>
                            </div>
                        {/if}
                    </div>
                </div>
            {/key}
        </div>

        <!-- دکمه‌های ناوبری -->
        <div
            class="p-6 border-t border-slate-100 dark:border-slate-700 flex justify-between items-center bg-slate-50 dark:bg-slate-800/90 z-10"
        >
            <button
                class="px-8 py-3 rounded-xl font-bold transition-all duration-200 {currentStep ===
                1
                    ? 'bg-slate-200 text-slate-400 cursor-not-allowed dark:bg-slate-700/50 dark:text-slate-500'
                    : 'bg-white text-slate-700 border border-slate-200 shadow-sm hover:bg-slate-100 dark:bg-slate-700 dark:text-slate-200 dark:border-slate-600 dark:hover:bg-slate-600'}"
                on:click={prevStep}
                disabled={currentStep === 1}
            >
                قبلی
            </button>

            {#if currentStep < totalSteps}
                <button
                    class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold transition-all duration-200 shadow-lg shadow-blue-500/30 flex items-center gap-2"
                    on:click={nextStep}
                >
                    بعدی
                </button>
            {:else}
                <button
                    class="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl font-bold transition-all duration-200 shadow-lg shadow-green-500/30 disabled:opacity-70 disabled:cursor-wait flex items-center gap-2"
                    on:click={startQuizHandler}
                    disabled={!!promise}
                >
                    {#if promise}
                        <svg
                            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                class="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                stroke-width="4"
                            ></circle>
                            <path
                                class="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            ></path>
                        </svg>
                        درحال بارگذاری...
                    {:else}
                        شروع پرسشنامه
                    {/if}
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    :global(body) {
        font-family:
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }

    .scroll-thumb {
        animation: scroll-down 3s infinite ease-in-out;
    }

    .scroll-content {
        animation: scroll-content 3s infinite ease-in-out;
    }

    @keyframes scroll-down {
        0%,
        15% {
            top: 6px;
        }
        85%,
        100% {
            top: calc(100% - 70px);
        }
    }

    @keyframes scroll-content {
        0%,
        15% {
            transform: translateY(0);
        }
        85%,
        100% {
            transform: translateY(-50%);
        }
    }
</style>
