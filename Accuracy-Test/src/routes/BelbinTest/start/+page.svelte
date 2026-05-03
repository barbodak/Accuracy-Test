<script lang="ts">
    import { goto } from "$app/navigation";
    import { fly } from "svelte/transition";
    import { startQuiz } from "$lib/utils/api/quiz-apis";

    let isLoading = false;
    let promise: Promise<void>;

    const startQuizHandler = async () => {
        isLoading = true;
        try {
            promise = startQuiz({
                quiz_type: "BelbinTest",
            });
            await promise;
            await goto("/BelbinTest");
        } catch (e) {
            console.error(e);
            isLoading = false;
        }
    };

    let currentStep = 1;
    const totalSteps = 4;

    const tutorialSteps = [
        {
            title: "آزمون بلبین چیست؟",
            content: `همکاری و کار تیمی بر پایه شناسایی قابلیت‌ها و انتخاب اعضای تیم بر اساس آن‌ها بنا می‌شود. آزمون بلبین ابزاری برای معماری تیم در مدیریت نوین است.

این آزمون هشت نقش تیمی را شناسایی می‌کند:
• اجراکنندگان
• هماهنگ‌کنندگان
• وادارکنندگان (شکل‌دهندگان)
• ایده‌پردازان
• منبع‌یاب‌ها
• ارزیاب‌ها (مراقبین)
• گروهی‌کاران
• تمام‌کنندگان`,
        },
        {
            title: "فلسفه نقش‌های تیمی",
            content: `هیچ نقشی برتر از دیگری نیست. ترکیب این نقش‌ها، مانند رنگ‌های مختلفی که نور سفید را می‌سازند، به مدیریت همکارانه مؤثر منجر می‌شود.

آزمون بلبین برای درک شخصیت کاری افراد در تیم حیاتی است و به دلیل کاربردی بودن، استاندارد انتخاب منابع انسانی در شرکت‌های بین‌المللی محسوب می‌شود.`,
        },
        {
            title: "ساختار آزمون",
            content: `آزمون شامل ۷ سؤال است. هر سؤال ۸ گزینه دارد.

در هر سؤال، ۱۰ امتیاز برای تقسیم بین گزینه‌ها دارید. امتیازها را بر اساس میزان نزدیکی هر گزینه به رفتار واقعی خود در یک تیم کاری توزیع کنید.

امتیازها باید عدد صحیح باشند و می‌توانید به یک یا چند گزینه امتیاز دهید. مجموع امتیازات هر سؤال باید دقیقاً ۱۰ باشد.`,
        },
        {
            title: "نکته مهم",
            content: `پاسخ‌ها باید بازتاب خود واقعی شما باشد، نه خود ایده‌آل.

هدف این است که وضعیت فعلی شما را به‌طور دقیق نشان دهد. صادقانه پاسخ دهید تا نتایج معتبر و کاربردی باشد.

آماده‌اید؟ بیایید شروع کنیم!`,
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

    let animate = false;
    let direction = 1;
    $: {
        animate = false;
        setTimeout(() => (animate = true), 50);
    }
</script>

<svelte:head>
    <title>آزمون بلبین - راهنما</title>
</svelte:head>

<div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 p-4"
    dir="rtl"
>
    <div
        class="w-full max-w-4xl bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden"
    >
        <div class="p-8 md:p-12">
            <!-- Header -->
            <div class="text-center mb-8">
                <h1
                    class="text-4xl md:text-5xl font-bold text-purple-600 dark:text-purple-400 mb-4"
                >
                    آزمون بلبین
                </h1>
                <p class="text-gray-600 dark:text-gray-300 text-lg">
                    شناسایی نقش‌های تیمی شما
                </p>
            </div>

            <!-- Progress Bar -->
            <div class="mb-8">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                        مرحله {currentStep} از {totalSteps}
                    </span>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                        {Math.round((currentStep / totalSteps) * 100)}%
                    </span>
                </div>
                <div
                    class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3"
                >
                    <div
                        class="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full transition-all duration-500"
                        style="width: {(currentStep / totalSteps) * 100}%"
                    ></div>
                </div>
            </div>

            <!-- Tutorial -->
            <div class="min-h-[280px]">
                {#each tutorialSteps as step, i}
                    {#if currentStep === i + 1}
                        <div transition:fly={{ x: direction * 50, duration: 400 }}>
                            <h2 class="text-2xl font-semibold text-purple-700 dark:text-purple-300 mb-4">
                                {step.title}
                            </h2>
                            <p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                                {step.content}
                            </p>
                        </div>
                    {/if}
                {/each}
            </div>

            <!-- Footer -->
            <div class="flex justify-between items-center pt-8 mt-8 border-t border-gray-200 dark:border-gray-700">
                <button
                    on:click={prevStep}
                    disabled={currentStep === 1}
                    class="px-6 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 disabled:opacity-50"
                >
                    قبلی
                </button>

                {#if currentStep === totalSteps}
                    <button
                        on:click={startQuizHandler}
                        disabled={isLoading}
                        class="px-6 py-3 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-semibold flex items-center gap-2 disabled:opacity-75"
                    >
                        {#if isLoading}
                            <div class="h-4 w-4 border-2 border-white/60 border-t-transparent rounded-full animate-spin"></div>
                            <span>درحال آماده‌سازی...</span>
                        {:else}
                            شروع آزمون
                        {/if}
                    </button>
                {:else}
                    <button
                        on:click={nextStep}
                        class="px-6 py-2 rounded-lg bg-pink-600 hover:bg-pink-700 text-white font-semibold"
                    >
                        بعدی
                    </button>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap");

    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }
</style>

