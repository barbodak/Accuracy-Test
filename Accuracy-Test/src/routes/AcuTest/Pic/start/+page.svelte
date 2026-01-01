<script lang="ts">
    import { goto } from "$app/navigation";
    import { fly } from "svelte/transition";
    import { startQuiz } from "$lib/utils/api/quiz-apis";

    let isLoading = false;
    let promise: Promise<void>;

    const startQuizHandler = async () => {
        isLoading = true;
        try {
            // Assuming the backend type for part 2 is 'AcuTest_visual'
            promise = startQuiz({
                quiz_type: "AcuTest_pic",
            });
            await promise;
            // Navigate to the Visual test page
            await goto("/AcuTest/Pic");
        } catch (e) {
            console.error(e);
            isLoading = false;
        }
    };

    let currentStep = 1;
    const totalSteps = 5; // Slightly fewer steps needed than text part

    const tutorialSteps = [
        {
            title: "به بخش دوم آزمون دقت خوش آمدید",
            description:
                "در این بخش، دقت دیداری و توانایی شما در تشخیص الگوهای تصویری سنجیده می‌شود.\nبرخلاف بخش قبلی که متنی بود، در اینجا با تصاویر سر و کار دارید.",
        },
        {
            title: "نحوه انجام آزمون",
            description:
                "در هر سوال، یک «تصویر شکل» در سمت چپ به شما نمایش داده می‌شود. در سمت راست، ۴ گزینه وجود دارد. تنها یکی از این گزینه‌ها **دقیقاً** مشابه تصویر مرجع است.",
        },
        {
            title: "تشخیص تفاوت‌ها",
            description:
                "گزینه‌های انحرافی ممکن است تفاوت‌های بسیار جزئی داشته باشند (تغییر رنگ جزئی، یا حذف یک خط کوچک). شما باید با تیزبینی گزینه‌ای را پیدا کنید که هیچ تفاوتی با الگو ندارد.",
        },
        {
            title: "مدت زمان",
            description:
                "مدت زمان این بخش نیز **۵ دقیقه** است. باتوجه به محدودیت زمان در مدیریت آن کوشا باشید.",
        },
        {
            title: "آماده‌اید؟",
            description:
                "تمرکز خود را روی تصاویر بگذارید. محیط اطراف خود را ساکت نگه دارید و با زدن دکمه شروع، وارد آزمون شوید.",
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
    let direction = 1;
    $: {
        animate = false;
        setTimeout(() => (animate = true), 50);
    }
</script>

<svelte:head>
    <title>راهنمای بخش دوم آزمون دقت </title>
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
               راهنمای بخش دوم آزمون دقت
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
                class="bg-pink-600 h-2.5 rounded-full transition-all duration-500 ease-out"
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
                        <!-- Step 1: Eye Icon -->
                        {#if currentStep === 1}
                            <div
                                class="flex items-center justify-center text-pink-500 dark:text-pink-400"
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
                                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                    />
                                </svg>
                            </div>
                        {/if}

                        <!-- Step 2: Static Example (Layout Explanation) -->
                        {#if currentStep === 2}
                            <div
                                class="flex w-full max-w-md gap-4 items-center justify-between opacity-80"
                            >
                                <!-- Left: Reference -->
                                <!-- Right: Options -->
                                <div
                                    class="flex flex-col items-center gap-2 flex-1"
                                >
                                    <span
                                        class="text-xs font-bold text-slate-400"
                                        >گزینه‌ها</span
                                    >
                                    <div class="grid grid-cols-4 gap-2 w-full">
                                        <div
                                            class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 rounded flex items-center justify-center"
                                        >
                                            <div
                                                class="w-8 h-8 bg-slate-800 rounded-sm"
                                            ></div>
                                        </div>
                                        <div
                                            class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 rounded flex items-center justify-center"
                                        >
                                            <div
                                                class="w-6 h-6 bg-slate-800 rounded-full"
                                            ></div>
                                        </div>
                                        <div
                                            class="aspect-square bg-white dark:bg-slate-600 border-2 border-green-500 rounded flex items-center justify-center relative"
                                        >
                                            <div
                                                class="w-8 h-8 bg-slate-800 dark:bg-slate-200 rounded-full"
                                            ></div>
                                            <div
                                                class="absolute -top-2 -right-2 bg-green-500 text-white rounded-full p-0.5"
                                            >
                                                <svg
                                                    class="w-3 h-3"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke="currentColor"
                                                    ><path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        stroke-width="3"
                                                        d="M5 13l4 4L19 7"
                                                    /></svg
                                                >
                                            </div>
                                        </div>
                                        <div
                                            class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 rounded flex items-center justify-center"
                                        >
                                            <div
                                                class="w-8 h-8 border-4 border-slate-800 rounded-full"
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                                <div
                                    class="h-16 w-[1px] bg-slate-300 dark:bg-slate-600"
                                ></div>

                                <div class="flex flex-col items-center gap-2">
                                    <span
                                        class="text-xs font-bold text-slate-400"
                                        >الگو</span
                                    >
                                    <div
                                        class="w-16 h-16 bg-white dark:bg-slate-600 border-2 border-pink-500 rounded flex items-center justify-center"
                                    >
                                        <div
                                            class="w-8 h-8 bg-slate-800 dark:bg-slate-200 rounded-full"
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        {/if}

                        <!-- Step 3: Animation (Finding the Match) -->
                        {#if currentStep === 3 && animate}
                            <div
                                class="relative w-full max-w-lg flex items-center justify-between gap-4"
                            >
                                <div class="pointer-hand"></div>

                                <!-- Reference (Left) -->

                                <!-- Options (Right) -->
                                <div
                                    class="grid grid-cols-2 sm:grid-cols-4 gap-3 flex-1"
                                >
                                    <!-- Option 1: Wrong (Rotated) -->
                                    <div
                                        class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 dark:border-slate-600 rounded-lg flex items-center justify-center"
                                    >
                                        <svg
                                            width="30"
                                            height="30"
                                            viewBox="0 0 24 24"
                                            fill="currentColor"
                                            class="text-indigo-600 dark:text-indigo-400 transform rotate-90"
                                        >
                                            <path d="M12 2L2 22h20L12 2z" />
                                        </svg>
                                    </div>

                                    <!-- Option 2: Correct -->
                                    <div
                                        class="aspect-square bg-white dark:bg-slate-600 border-2 border-slate-200 dark:border-slate-600 rounded-lg flex items-center justify-center relative option-correct-animate"
                                    >
                                        <svg
                                            width="30"
                                            height="30"
                                            viewBox="0 0 24 24"
                                            fill="currentColor"
                                            class="text-indigo-600 dark:text-indigo-400"
                                        >
                                            <path d="M12 2L2 22h20L12 2z" />
                                        </svg>
                                    </div>

                                    <!-- Option 3: Wrong (Different Shape) -->
                                    <div
                                        class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 dark:border-slate-600 rounded-lg flex items-center justify-center"
                                    >
                                        <svg
                                            width="30"
                                            height="30"
                                            viewBox="0 0 24 24"
                                            fill="currentColor"
                                            class="text-indigo-600 dark:text-indigo-400"
                                        >
                                            <rect
                                                x="2"
                                                y="2"
                                                width="20"
                                                height="20"
                                            />
                                        </svg>
                                    </div>

                                    <!-- Option 4: Wrong (Hollow) -->
                                    <div
                                        class="aspect-square bg-white dark:bg-slate-600 border border-slate-300 dark:border-slate-600 rounded-lg flex items-center justify-center"
                                    >
                                        <svg
                                            width="30"
                                            height="30"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="3"
                                            class="text-indigo-600 dark:text-indigo-400"
                                        >
                                            <path d="M12 2L2 22h20L12 2z" />
                                        </svg>
                                    </div>
                                </div>
                                <div class="flex flex-col items-center gap-2">
                                    <div
                                        class="w-20 h-20 bg-white dark:bg-slate-600 border-2 border-slate-400 dark:border-slate-500 rounded-lg flex items-center justify-center shadow-sm"
                                    >
                                        <!-- Shape: Triangle pointing up -->
                                        <svg
                                            width="40"
                                            height="40"
                                            viewBox="0 0 24 24"
                                            fill="currentColor"
                                            class="text-indigo-600 dark:text-indigo-400"
                                        >
                                            <path d="M12 2L2 22h20L12 2z" />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        {/if}

                        <!-- Step 4: Time -->
                        {#if currentStep === 4}
                            <div
                                class="flex flex-col items-center justify-center"
                            >
                                <div
                                    class="w-20 h-20 rounded-full bg-pink-100 dark:bg-pink-900 flex items-center justify-center mb-3 animate-pulse"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="w-10 h-10 text-pink-600 dark:text-pink-300"
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
                                    class="text-3xl font-bold text-pink-700 dark:text-pink-300"
                                    >۵ دقیقه</span
                                >
                                <span
                                    class="text-sm text-slate-500 mt-2 dark:text-slate-400"
                                    >زمان برای ۴۲ سوال</span
                                >
                            </div>
                        {/if}

                        <!-- Step 5: Ready -->
                        {#if currentStep === 5}
                            <div
                                class="flex items-center justify-center text-pink-600 dark:text-pink-400"
                            >
                                <div class="relative">
                                    <span
                                        class="absolute inset-0 rounded-full bg-pink-400 opacity-20 animate-ping"
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
                                        <polygon points="5 3 19 12 5 21 5 3"
                                        ></polygon>
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
                    class="py-2 px-6 rounded-lg font-semibold text-white bg-pink-600 hover:bg-pink-700 transition-all disabled:bg-pink-400 flex items-center gap-2 shadow-lg hover:shadow-pink-500/30"
                >
                    {#if isLoading}
                        <div
                            class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
                        ></div>
                        <span>درحال آماده‌سازی...</span>
                    {:else}
                        شروع بخش دوم
                    {/if}
                </button>
            {:else}
                <button
                    on:click={nextStep}
                    class="py-2 px-5 rounded-lg font-semibold text-white bg-pink-600 hover:bg-pink-700 transition-all shadow-md hover:shadow-pink-500/20"
                >
                    بعدی
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap");

    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }

    /* Hand Pointer */
    .pointer-hand {
        width: 32px;
        height: 32px;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='black' stroke='white' stroke-width='1'><path d='M9 11.24V7.5C9 6.12 10.12 5 11.5 5S14 6.12 14 7.5v3.74c1.21-.81 2-2.18 2-3.74C16 5.01 13.99 3 11.5 3S7 5.01 7 7.5c0 1.56.79 2.93 2 3.74zm9.84 4.63l-4.54-2.26c-.17-.07-.35-.11-.54-.11H13v-6c0-.83-.67-1.5-1.5-1.5S10 6.67 10 7.5v10.74l-3.43-.72c-.08-.01-.15-.03-.24-.03-.31 0-.59.13-.79.33l-.79.8 4.94 4.94c.27.27.65.44 1.06.44h6.79c.75 0 1.33-.55 1.44-1.28l.75-5.27c.01-.07.02-.14.02-.2 0-.62-.38-1.16-.91-1.38z'/></svg>");
        background-size: contain;
        background-repeat: no-repeat;
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 20;
        opacity: 0;
        /* Animation applied */
        animation: find-option-anim 3s ease-in-out infinite;
    }

    .option-correct-animate {
        animation: option-highlight 3s ease-in-out infinite;
    }

    /* 
       Animation Logic:
       1. Start invisible at center.
       2. Move to "Correct Option" (Option 2 in grid).
       3. Click (scale down).
       4. Fade out.
    */
    @keyframes find-option-anim {
        0% {
            opacity: 0;
            transform: translate(-50%, 0px) scale(1); /* Center */
        }
        20% {
            opacity: 1;
            transform: translate(70px, -10px) scale(1); /* Move slightly Right to Option 2 */
        }
        40% {
            transform: translate(70px, -10px) scale(0.8); /* Click */
        }
        50% {
            transform: translate(70px, -10px) scale(1); /* Release */
        }
        80% {
            opacity: 1;
        }
        90%,
        100% {
            opacity: 0;
        }
    }

    @keyframes option-highlight {
        0%,
        35% {
            border-color: #e2e8f0; /* slate-200 */
            background-color: white;
        }
        36% {
            border-color: #22c55e; /* green-500 */
            background-color: #f0fdf4; /* green-50 */
            transform: scale(0.95);
        }
        45% {
            transform: scale(1);
        }
        90%,
        100% {
            border-color: #22c55e;
            background-color: #f0fdf4;
        }
    }
</style>
