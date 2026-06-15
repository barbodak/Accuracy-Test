<script>
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    import { onMount, onDestroy } from "svelte";
    import { fade, fly } from "svelte/transition";

    let currentStep = 1;
    let direction = 1;
    let promise = null;

    // متغیرهای انیمیشن هکزاکو (مرحله ۲)
    let step2Interval;
    let step3Interval;
    let demoChoice = -1; // گزینه‌ای که انتخاب می‌شود
    let cursorPosition = -1; // موقعیت موس برای انیمیشن
    let cursorScale = 1;
    let cursorOpacity = 0;
    
    // رنگ‌ها و لیبل‌های اصلی هکزاکو
    const btnColors = [
        "bg-red-200",
        "bg-red-100",
        "bg-slate-100",
        "bg-green-100",
        "bg-green-200",
    ];
    const hexacoLabels = [
        "کاملاً مخالفم",
        "مخالفم",
        "نظری ندارم",
        "موافقم",
        "کاملاً موافقم"
    ];

    let navAnimation = false;

    const tutorialSteps = [
        {
            title: "ساختار پرسشنامه",
            description:
                "این پرسشنامه شامل ۱۰۰ سوال است.\nبرای پاسخگویی به این سوالات هیچ محدودیت زمانی وجود ندارد، بنابراین با دقت و در کمال آرامش به سوالات پاسخ دهید.",
        },
        {
            title: "نحوه پاسخگویی",
            description:
                "برای هر سوال ۵ گزینه در نظر گرفته شده است.\nگزینه‌ای که بیشترین تطابق را با ویژگی‌های شما دارد انتخاب کنید.",
        },
        {
            title: "ویرایش پاسخ‌ها",
            description:
                "در صورت نیاز می‌توانید با استفاده از دکمه «قبلی» به سوالات پیشین بازگردید و پاسخ‌های خود را تغییر دهید.",
        },
        {
            title: "آماده‌اید؟",
            description:
                "شما با موفقیت راهنمای پرسشنامه هکزاکو را مطالعه کردید.\nبرای شروع ارزیابی روی دکمه زیر کلیک کنید.",
        },
    ];

    const totalSteps = tutorialSteps.length;

    // مدیریت انیمیشن‌های هر مرحله
    $: if (currentStep === 2) {
        // ریست اولیه
        demoChoice = -1;
        cursorOpacity = 0;
        cursorScale = 1;
        
        if (step2Interval) clearInterval(step2Interval);
        
        step2Interval = setInterval(() => {
            // ۱. شروع سیکل و مخفی کردن موس
            demoChoice = -1;
            cursorOpacity = 0;
            cursorScale = 1;

            // ۲. موس ظاهر می‌شود و به سمت گزینه "موافقم" (ایندکس 3) می‌رود
            setTimeout(() => {
                cursorPosition = 3; 
                cursorOpacity = 1;
            }, 500);

            // ۳. شبیه‌سازی کلیک کردن موس (کوچک شدن)
            setTimeout(() => {
                cursorScale = 0.8;
            }, 1300);

            // ۴. رها کردن کلیک و ثبت انتخاب (تیک خوردن گزینه)
            setTimeout(() => {
                cursorScale = 1;
                demoChoice = 3;
            }, 1500);

            // ۵. محو شدن موس بعد از نمایش انتخاب
            setTimeout(() => {
                cursorOpacity = 0;
            }, 2500);

        }, 3200); // تکرار کل این پروسه هر ۳.۲ ثانیه
    } else {
        if (step2Interval) clearInterval(step2Interval);
    }

    $: if (currentStep === 3) {
        if (step3Interval) clearInterval(step3Interval);
        step3Interval = setInterval(() => {
            navAnimation = true;
            setTimeout(() => {
                navAnimation = false;
            }, 300);
        }, 2000);
    } else {
        if (step3Interval) clearInterval(step3Interval);
    }

    onDestroy(() => {
        if (step2Interval) clearInterval(step2Interval);
        if (step3Interval) clearInterval(step3Interval);
    });

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
            quiz_type: "HexacoTest",
        });
        await promise;
        window.location.href = "/HexacoTest";
    };

</script>

<svelte:head>
    <title>راهنمای پرسشنامه</title>
</svelte:head>

<div
    dir="rtl"
    class="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 flex items-center justify-center p-4 sm:p-8 font-sans"
>
    <div
        class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-3xl shadow-2xl overflow-hidden flex flex-col h-[650px]"
    >
        <!-- هدر و نوار پیشرفت -->
        <div class="p-6 border-b border-slate-100 dark:border-slate-700">
            <div class="flex justify-between items-center mb-5">
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
                    <!-- عنوان و توضیحات داینامیک -->
                    <div class="mb-8 text-center min-h-[100px]">
                        <h2
                            class="text-2xl font-bold mb-4 text-blue-600 dark:text-blue-400"
                        >
                            {tutorialSteps[currentStep - 1].title}
                        </h2>
                        <p
                            class="text-slate-600 dark:text-slate-300 leading-relaxed text-base sm:text-lg max-w-2xl mx-auto whitespace-pre-line"
                        >
                            {tutorialSteps[currentStep - 1].description}
                        </p>
                    </div>

                    <!-- بخش محتوای انیمیشن‌ها -->
                    <div
                        class="flex-1 relative bg-slate-50 dark:bg-slate-900/50 rounded-2xl border border-slate-100 dark:border-slate-700 p-6 flex items-center justify-center overflow-hidden"
                    >
                        {#if currentStep === 1}
                            <!-- محتوای مرحله 1 -->
                            <div class="flex flex-col items-center justify-center space-y-6">
                                <div class="w-32 h-32 rounded-full bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center shadow-inner">
                                    <span class="text-5xl font-extrabold text-blue-600 dark:text-blue-400">۱۰۰</span>
                                </div>
                                <div class="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/30 px-4 py-2 rounded-full">
                                    <span class="text-xl">⏳</span>
                                    <span class="font-medium">بدون محدودیت زمانی</span>
                                </div>
                            </div>

                        {:else if currentStep === 2}
                            <!-- دکمه‌های دایره‌ای هکزاکو -->
                            <div class="w-full max-w-2xl bg-white dark:bg-slate-700 p-8 rounded-2xl shadow-lg border border-slate-200 dark:border-slate-600 relative overflow-hidden">
                                <!-- خط جایگزین متن سوال -->
                                <div class="h-4 w-2/3 bg-slate-200 dark:bg-slate-600 rounded mb-10 mx-auto"></div>
                                
                                <div class="flex flex-row flex-wrap justify-center gap-4 sm:gap-6 relative">
                                    {#each hexacoLabels as label, i}
                                        <div class="flex flex-col items-center gap-3 w-20 sm:w-24 transition-transform duration-200">
                                            <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-full border-4 border-white shadow-md flex items-center justify-center text-xl text-slate-800 transition-all duration-300 {btnColors[i]} {demoChoice === i ? 'scale-110 shadow-lg border-blue-500 !text-blue-600' : ''}">
                                                {#if demoChoice === i}
                                                    <span in:fade={{ duration: 150 }}>✔</span>
                                                {/if}
                                            </div>
                                            <span class="text-xs sm:text-sm font-semibold text-slate-600 dark:text-slate-300 text-center leading-tight">{label}</span>
                                        </div>
                                    {/each}

                                    <!-- موس حرفه‌ای SVG (انیمیشن) -->
                                    <div class="absolute z-20 pointer-events-none transition-all duration-700 ease-in-out"
                                         style="
                                            opacity: {cursorOpacity};
                                            transform: scale({cursorScale});
                                            right: {cursorPosition === -1 ? '40%' : `${6 + cursorPosition * 20}%`};
                                            top: {cursorPosition === -1 ? '100%' : '35%'};
                                         ">
                                        <svg width="32" height="32" viewBox="0 0 24 24" fill="white" stroke="#1e293b" stroke-width="1.5" class="drop-shadow-xl translate-x-2 translate-y-2">
                                            <path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>

                        {:else if currentStep === 3}
                            <!-- محتوای مرحله 3 -->
                            <div class="w-full max-w-sm bg-white dark:bg-slate-700 p-6 rounded-2xl shadow-lg border border-slate-200 dark:border-slate-600 flex justify-between items-center relative">
                                <button class="px-6 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-600 text-slate-700 dark:text-slate-200 font-medium transition-transform {navAnimation ? 'bg-slate-200 dark:bg-slate-500 scale-95' : ''}">
                                    قبلی
                                </button>
                                <button class="px-6 py-2.5 rounded-xl bg-blue-600 text-white font-medium opacity-50">
                                    بعدی
                                </button>
                                <!-- انیمیشن دست برای دکمه قبلی -->
                                <div class="absolute bottom-1 right-12 text-3xl z-20 transition-transform duration-300 {navAnimation ? 'translate-y-0 scale-90' : 'translate-y-4 scale-100'}">
                                    👆
                                </div>
                            </div>

                        {:else if currentStep === 4}
                            <!-- محتوای مرحله 4 -->
                            <div class="flex flex-col items-center justify-center h-full space-y-6">
                                <div class="w-32 h-32 bg-green-100 dark:bg-green-900/50 rounded-full flex items-center justify-center shadow-xl transform hover:scale-110 transition duration-300 border-[6px] border-white dark:border-slate-800">
                                    <svg class="w-16 h-16 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
                                    </svg>
                                </div>
                                <p class="text-2xl font-bold text-slate-700 dark:text-slate-300">
                                    موفق باشید!
                                </p>
                            </div>
                        {/if}
                    </div>
                </div>
            {/key}
        </div>

        <!-- دکمه‌های ناوبری پایینی -->
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

