<script lang="ts">
    import { startQuiz } from "$lib/utils/api/quiz-apis";
    import { fade, fly } from "svelte/transition";
    let promise: Promise<void>;
    const startQuizHandler = async () => {
        promise = startQuiz({
            quiz_type: "ValuTest",
        });
        await promise;
        window.location.href = "/ValuTest";
    };

    let currentStep = 1;
    const totalSteps = 8;
    // افزایش تعداد کل مراحل

    const tutorialSteps = [
        {
            title: "به آزمون ارزش‌های شغلی خوش آمدید",
            description:
                "این آزمون به شما کمک می‌کند تا مهم‌ترین اولویت‌های شغلی خود را شناسایی کنید. شما ۲۰ کارت در اختیار وجود دارد که روی هرکدام توصیفی درباره اولویت‌ها و ایده آل های شغلی نوشته شده.و یک جدول با دقیقا ۲۰ خانه خالی در ۵ ستون تعبیه شده ﺗﻮﺟﻪ داﺷﺘﻪ ﺑﺎﺷﯿﺪ که ﺑﺮای پاﺳﺦ گویی ﻣﻨﺎﺳﺐ ﺑﺎﯾﺪ آراﻣﺶ وﺗﻤﺮکز، ﺣﺪاﻗﻞ ۱۵ دﻗﯿﻪ وﻗﺖ این پرسشنامه را تکمیل کنید.",
        },
        {
            title: "اولویت‌بندی",
            description:
                "شما باید این 20 کارت را بر روی 20 خانه‌ی جدول قرار داده و چینش کارت‌ها را آنقدر تغییر دهید تا به ترکیب مطلوب خود برسید.در حالت مطلوب شما، کارت‌هایی که در ستون 5 قرار می‌دهید مهمترین اولویت‌های شغلی‌تان هستند؛ کارت‌های ستون 4 از ستون‌های 3 و 2 و 1 برای شما اهمیت بیشتری دارند؛ کارت‌های ستون 3 از ستون‌های 4 و 5 کم اهمیت‌تر ولی از ستون‌های 1 و 2 با اهمیت‌تر هستند؛ و به همین ترتیب کارت‌های ستون 2 از ستون 1 اولویت بیشتری برای شما دارند. کارت‌هایی که در ستون 1 قرار می‌دهید به نسبت بقیه‌ی کارت‌ها کمترین اولویت را برای شما دارند",
        },
        {
            title: "اولویت‌بندی",
            description:
                "بنابراین شما باید چیدمان کارت‌ها را براساس اینکه چقدر در رضایتمندی شغلی برایتان اولویت دارند در ۵ گروه دسته‌بندی کنید. در هنگام جابجا کردن کارت‌ها به این موضوع فکر کنید که داشتن شغلی با شرایط ذکر شده روی کارت چقدر برای شما مطلوبیت و اهمیت دارد. توجه داشته باشید که ۴ خانه‌ی موجود در یک ستون نسبت به یکدیگر هیچ اولویی ندارند و در هر ستون دقیقا باید ۴ کارت را قرار دهید.",
        },
        {
            title: "قرار دادن کارت‌ها",
            description:
                'در سمت راست صفحه، لیست "کارت‌های باقی‌مانده" را می‌بینید.برای قرار دادن یک کارت، ابتدا روی آن کلیک کنید تا انتخاب شود، سپس روی یک خانه خالی در جدول اصلی کلیک کنید.',
        },
        {
            title: "جابجایی کارت‌ها",
            description:
                "برای جابجایی دو کارت در جدول، روی کارت اول کلیک کنید تا انتخاب شود، سپس روی کارت دوم کلیک کنید. جای آن‌ها با هم عوض می‌شود.",
        },
        {
            title: "حذف کارت از جدول",
            description:
                "برای برگرداندن یک کارت از جدول به لیست، ماوس خود را روی آن ببرید. یک دکمه قرمز رنگ (×) ظاهر می‌شود. روی آن کلیک کنید تا کارت حذف شود.",
        },
        {
            title: " پایان آزمون", // عنوان برای مطابقت با مرحله جدید به‌روز شد
            description:
                'پس از اینکه تمام ۲۰ کارت را در جدول قرار دادید، دکمه "پایان آزمون" در گوشه بالا سمت راست صفحه کلیک کنید تا نتایج شما ذخیره شود.',
        },
        {
            title: "آماده‌اید؟", // مرحله نهایی
            description:
                'به یاد داشته باشید که برای تکمیل این پرسشنامه با آرامش و تمرکز حداقل ۱۵ دقیقه زمان‌ بگذارید.وقتی آماده بودید، روی دکمه "شروع آزمون" کلیک کنید.',
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

    // متغیر کمکی برای انیمیشن‌ا
    let animate = false;
    let direction = 1; // 1 for next, -1 for prev
    $: {
        animate = false;
        // Trigger reflow to restart animation
        setTimeout(() => (animate = true), 50);
    }
</script>

<svelte:head>
    <title>راهنمای آزمون ارزش‌ها</title>
</svelte:head>

<div
    class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-slate-900 p-4 font-['Vazirmatn']"
    dir="rtl"
>
    <div
        class="w-full max-w-2xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 sm:p-10 transition-all duration-300"
    >
        <div class="flex justify-between items-center mb-6">
            <h2
                class="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-white"
            >
                راهنمای آزمون
            </h2>
            <span class="text-sm font-medium text-slate-500 dark:text-slate-400"
                >مرحله {currentStep} از {totalSteps}</span
            >
        </div>

        <div
            class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2.5 mb-8"
        >
            <div
                class="bg-blue-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                style="width: {(currentStep / totalSteps) * 100}%"
            />
        </div>

        <div class="relative min-h-[350px] sm:min-h-[400px] overflow-hidden">
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
                        class="text-base text-slate-600 dark:text-slate-300 mb-6 leading-relaxed"
                    >
                        {tutorialSteps[currentStep - 1].description}
                    </p>

                    {#if currentStep !== 2 && currentStep !== 3}
                        <div
                            class="h-48 w-full bg-slate-100 dark:bg-slate-700/50
rounded-lg p-4 flex items-center justify-center overflow-hidden"
                        >
                            {#if currentStep === 1}
                                <div
                                    class="flex items-center justify-center text-blue-500 dark:text-blue-400"
                                >
                                    <span class="text-5xl font-bold">WIL</span>
                                </div>
                            {/if}

                            {#if currentStep === 4 && animate}
                                <div
                                    class="flex items-center justify-around w-full"
                                >
                                    <div class="flex flex-col items-center">
                                        <span
                                            class="text-sm text-slate-500 mb-2"
                                            >لیست کارت‌ها</span
                                        >
                                        <div
                                            class="mock-card mock-card-place-start"
                                        >
                                            <span class="font-bold text-2xl"
                                                >J</span
                                            >
                                        </div>
                                    </div>
                                    <div class="pointer" />

                                    <div class="flex flex-col items-center">
                                        <span
                                            class="text-sm text-slate-500 mb-2"
                                            >جدول</span
                                        >
                                        <div
                                            class="w-24 h-32 bg-slate-200 dark:bg-slate-600 border-2 border-dashed border-slate-400 rounded-lg mock-card-place-end-container"
                                        >
                                            <div
                                                class="mock-card mock-card-place-end"
                                            >
                                                <span class="font-bold text-2xl"
                                                    >J</span
                                                >
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {/if}

                            {#if currentStep === 5 && animate}
                                <div
                                    class="relative"
                                    style="width: 136px;
height: 168px;"
                                >
                                    <div
                                        class="grid grid-cols-2 gap-2
w-full h-full"
                                    >
                                        <div class="mock-grid-slot" />

                                        <div class="mock-grid-slot" />

                                        <div class="mock-grid-slot" />
                                        <div class="mock-grid-slot" />
                                    </div>

                                    <div class="pointer-swap" />

                                    <div
                                        class="mock-card grid-card mock-card-swap-1"
                                    >
                                        <span class="font-bold text-xl">A</span>
                                    </div>
                                    <div
                                        class="mock-card grid-card mock-card-swap-2"
                                    >
                                        <span class="font-bold text-xl">B</span>
                                    </div>
                                </div>
                            {/if}

                            {#if currentStep === 6 && animate}
                                <div
                                    class="flex flex-col items-center justify-center relative group"
                                >
                                    <div class="pointer-remove" />
                                    <div
                                        class="mock-card mock-card-remove relative group overflow-visible"
                                    >
                                        <span class="font-bold text-2xl">F</span
                                        >

                                        <button
                                            class="absolute -top-2 -right-2 z-10 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center
                   
                opacity-0 transition-opacity duration-300
                               focus:outline-none remove-btn-animate"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="16"
                                                height="16"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="3"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><line
                                                    x1="18"
                                                    y1="6"
                                                    x2="6"
                                                    y2="18"
                                                /><line
                                                    x1="6"
                                                    y1="6"
                                                    x2="18"
                                                    y2="18"
                                                /></svg
                                            >
                                        </button>
                                    </div>
                                </div>
                            {/if}

                            {#if currentStep === 7}
                                <div
                                    class="flex flex-col items-center justify-center text-slate-600 dark:text-slate-300"
                                >
                                    <div
                                        class="py-2 px-4 rounded-lg font-semibold text-white bg-red-600 shadow-lg mb-4"
                                    >
                                        پایان آزمون
                                    </div>

                                    <p class="text-sm text-center">
                                        بعد از قرار دادن تمامی کارت‌ها درون جدول
                                        و اطمینان از چینش آن‌ها روی این دکمه
                                        کلیک کنید.
                                    </p>
                                </div>
                            {/if}

                            {#if currentStep === 8}
                                <div
                                    class="flex items-center justify-center text-green-500 dark:text-green-400"
                                >
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
                                            d="M5 
13l4 4L19 7"
                                        />
                                    </svg>
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            {/key}
        </div>

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
                    disabled={!!promise}
                    class="py-2 px-5 rounded-lg
font-semibold text-white bg-green-600 hover:bg-green-700 transition-all disabled:bg-green-400"
                >
                    {#if promise}
                        درال بارگذاری......
                    {:else}
                        شروع آزمون
                    {/if}
                </button>
            {:else}
                <button
                    on:click={nextStep}
                    class="py-2 px-5 rounded-lg font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-all"
                >
                    بعدی
                </button>
            {/if}
        </div>
    </div>
</div>
ت ت ت ت ��

<style>
    /* ایمپورت فونت وزیرمتن */
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap");
    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }

    /* کامپوننت کارت مجازی برای انیمیشن‌ها */
    .mock-card {
        width: 6rem;
        /* 96px */
        height: 8rem;
        /* 128px */
        border-radius: 0.5rem;
        /* 8px */
        background-color: white;
        border: 1px solid #e2e8f0;
        /* slate-200 */
        box-shadow:
            0 4px 6px -1px rgb(0 0 0 / 0.1),
            0 2px 4px -2px rgb(0 0 0 / 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        user-select: none;
    }
    :global(.dark) .mock-card {
        background-color: #334155;
        /* slate-700 */
        border-color: #475569;
        /* slate-600 */
    }

    /* انیمیشن اشاره‌گر ماوس (اصلاح شد�� با مکان‌نمای استاندارد) */
    .pointer,
    .pointer-swap,
    .pointer-remove {
        width: 28px;
        height: 28px;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'><path fill='white' stroke='black' stroke-width='1.5' d='M2.5,2.5l23,10l-10,3l-3,10Z'/></svg>");
        background-size: contain;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0;
        z-index: 10;
    }

    .pointer {
        animation: click-and-move 3s ease-in-out infinite;
    }
    .pointer-swap {
        animation: click-and-swap 4s ease-in-out infinite;
    }
    .pointer-remove {
        animation: hover-and-click 3s ease-in-out infinite;
    }

    /* حذف قوانین :global(.dark) تکراری برای اشاره‌گرها */

    /* انیمیشن مرحله ۲: قرار دادن */
    .mock-card-place-start {
        animation: card-select 3s ease-in-out infinite;
    }
    .mock-card-place-end {
        transform: scale(0);
        animation: card-appear 3s ease-in-out infinite;
    }
    .mock-card-place-end-container {
        animation: grid-select 3s ease-in-out infinite;
    }

    /* انیمیشن اصلاح شده: ��کان‌نما از راست به چپ حرکت می‌کند */
    @keyframes click-and-move {
        0%,
        100% {
            opacity: 0;
            transform: translate(110px, 20px) scale(1); /* Start RIGHT */
        }
        10% {
            opacity: 1;
            transform: translate(110px, 20px) scale(1); /* Visible on RIGHT */
        }
        20% {
            transform: translate(110px, 20px) scale(0.8);
            /* Click on RIGHT */
        }
        30% {
            transform: translate(110px, 20px) scale(1);
            /* Release click */
        }
        40%,
        60% {
            opacity: 1;
            transform: translate(-130px, 20px) scale(1); /* Move to LEFT */
        }
        70% {
            transform: translate(-130px, 20px) scale(0.8);
            /* Click on LEFT */
        }
        80% {
            transform: translate(-130px, 20px) scale(1);
            /* Release click */
            opacity: 1;
        }
        90% {
            opacity: 0;
        }
    }

    /* انیمیشن اصلاح شده: کارت چپ انتخاب و سپس محو می‌شود */
    @keyframes card-select {
        0% {
            transform: scale(1);
            border-width: 1px;
            opacity: 1;
        }
        20%, /* هماهنگ با کلیک رست در click-and-move */
		30% {
            transform: scale(1.05);
            border: 2px solid #3b82f6; /* انتخاب */
            opacity: 1;
        }
        40%,
        80% {
            /* منتظر می‌ماند تا کارت راست ظاهر شود */
            transform: scale(1);
            border-width: 1px;
            opacity: 1;
        }
        90%,
        100% {
            /* محو می‌شود */
            transform: scale(1);
            border-width: 1px;
            opacity: 0;
        }
    }
    @keyframes grid-select {
        0%,
        60%,
        100% {
            border-style: dashed;
        }
        70%, /* هماهنگ با کلیک ��پ در click-and-move */
		80% {
            border-style: solid;
        }
    }
    @keyframes card-appear {
        0%,
        70% {
            /* تا بعد از کلیک چپ منتظر می‌ماند */
            transform: scale(0);
        }
        80%, /* بعد از کلیک چپ ظاهر می‌شود */
		100% {
            transform: scale(1);
        }
    }

    /* انیمیشن ��رحله ۳: جابجایی (اصلاح شده نهایی) */

    .mock-grid-slot {
        width: 4rem;
        /* w-16 */
        height: 5rem;
        /* h-20 */
        border-radius: 0.375rem;
        /* rounded-md */
        background-color: rgb(226 232 240 / 0.5);
        /* bg-slate-200/50 */
    }
    :global(.dark) .mock-grid-slot {
        background-color: rgb(51 65 85 / 0.5);
        /* dark:bg-slate-700/50 */
    }

    .grid-card {
        width: 4rem;
        /* w-16 */
        height: 5rem;
        /* h-20 */
        font-size: 1.25rem;
        /* text-xl */
        position: absolute;
        top: 50%;
        /* <-- FIX: Center the card */
        left: 50%;
        /* <-- FIX: Center the card */
        /* The base translate(-50%, -50%) will be added in the keyframes */
    }

    .mock-card-swap-1 {
        /* Card A (Right) */
        animation: swap-1 4s ease-in-out infinite;
    }
    .mock-card-swap-2 {
        /* Card B (Left) */
        animation: swap-2 4s ease-in-out infinite;
    }

    @keyframes click-and-swap {
        /* Grid cell size: 64px, gap: 8px.
Total move: 72px */
        /* Center of TR cell: x = +36px, y = -44px */
        /* Center of BL cell: x = -36px, y = +44px */
        0%,
        100% {
            opacity: 0;
            /* Start at Card A (TR) */
            transform: translate(26px, -34px) scale(1);
        }
        10% {
            opacity: 1;
            transform: translate(26px, -34px) scale(1);
        }
        20% {
            transform: translate(26px, -34px) scale(0.8);
        } /* Click 1 (TR) */
        30% {
            transform: translate(26px, -34px) scale(1);
        }
        40%,
        50% {
            opacity: 1;
            /* Move to Card B (BL) */
            transform: translate(-46px, 54px) scale(1);
        }
        60% {
            transform: translate(-46px, 54px) scale(0.8);
        } /* Click 2 (BL) */
        70% {
            transform: translate(-46px, 54px) scale(1);
            opacity: 1;
        }
        80%,
        100% {
            opacity: 0;
            /* Fade out */
        }
    }

    @keyframes swap-1 {
        /* Card 1 (starts Top-Right) */
        0% {
            transform: translate(-50%, -50%) translate(36px, -44px);
            /* <-- FIX: Add centering */
            border-width: 1px;
        }
        20% {
            /* Get selected by Click 1 */
            transform: translate(-50%, -50%) translate(36px, -44px) scale(1.05);
            /* <-- FIX */
            border: 2px solid #3b82f6;
        }
        30%,
        60% {
            /* Stay selected */
            transform: translate(-50%, -50%) translate(36px, -44px) scale(1.05);
            /* <-- FIX */
            border: 2px solid #3b82f6;
        }
        60.1% {
            /* Click 2 happens, deselect */
            transform: translate(-50%, -50%) translate(36px, -44px) scale(1);
            /* <-- FIX */
            border-width: 1px;
            animation-timing-function: ease-in-out;
        }
        80%,
        100% {
            /* Move to Bottom-Left */
            transform: translate(-50%, -50%) translate(-36px, 44px);
            /* <-- FIX */
            border-width: 1px;
        }
    }
    @keyframes swap-2 {
        /* Card 2 (starts Bottom-Left) */
        0%,
        60% {
            /* Wait */
            transform: translate(-50%, -50%) translate(-36px, 44px);
            /* <-- FIX: Add centering */
        }
        60.1% {
            /* Click 2 happens, start move */
            transform: translate(-50%, -50%) translate(-36px, 44px);
            /* <-- FIX */
            animation-timing-function: ease-in-out;
        }
        80%,
        100% {
            /* Move to Top-Right */
            transform: translate(-50%, -50%) translate(36px, -44px);
            /* <-- FIX (and fixed typo from 44px to -44px) */
        }
    }

    /* انیمیشن مرحله ۴: حذف */
    .remove-btn-animate {
        animation: show-remove-btn 3s ease-in-out infinite;
    }
    .mock-card-remove {
        animation: remove-card 3s ease-in-out infinite;
    }

    @keyframes hover-and-click {
        0%,
        100% {
            opacity: 0;
            transform: translate(0px, 30px) scale(1);
        }
        10%,
        40% {
            opacity: 1;
            transform: translate(0px, -20px) scale(1);
        } /* هاور */
        50% {
            /* <-- FIX: Coordinates adjusted to target the button center */
            /* Original was (56px, -49px) */
            transform: translate(45px, -70px) scale(1);
        } /* حرکت به سمت دکمه */
        60% {
            transform: translate(45px, -70px) scale(0.8);
            /* <-- FIX */
        } /* کلیک */
        70% {
            transform: translate(45px, -70px) scale(1);
            /* <-- FIX */
            opacity: 1;
        }
        80% {
            opacity: 0;
        }
    }
    @keyframes show-remove-btn {
        0%,
        10%,
        100% {
            opacity: 0;
            transform: scale(0.5);
        }
        40%,
        70% {
            opacity: 1;
            transform: scale(1);
        }
        80% {
            opacity: 0;
            transform: scale(0.5);
        }
    }
    @keyframes remove-card {
        0%,
        70%,
        100% {
            opacity: 1;
            transform: scale(1);
        }
        80% {
            opacity: 0;
            transform: scale(0.8);
        }
    }
</style>
