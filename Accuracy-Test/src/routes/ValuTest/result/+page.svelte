<script lang="ts">
    // Import the required API function
    import {
        retreiveQuizAnswer,
        retreiveAccount,
    } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";

    // --- Data Definitions ---

    // Define the structure of the API response
    type QuizResult = {
        sharayet_kari: number;
        hemayat: number;
        ravabet: number;
        pishraft: number;
        esteghlal: number;
        tofigh: number;
    };

    // Define the descriptions for each value
    // Keys MUST match the API property names
    const descriptions: Record<
        keyof QuizResult,
        { title: string; text: string }
    > = {
        tofigh: {
            title: " توفیق (موفقیت فردی)",
            text: "اگر «توفیق» برای شما اهمیت دارد، بهتر است شغلی انتخاب کنید که:\n • با توانایی‌ها و نقاط قوتتان هماهنگ باشد،\n • نتیجه تلاش‌های خود را به‌وضوح ببینید،\n • احساس موفقیت و رضایت از عملکردتان را تجربه کنید.\n\nشما زمانی بیشترین انگیزه را دارید که تلاش‌هایتان به دستاورد مشخصی منجر شود.",
        },
        esteghlal: {
            title: "استقلال",
            text: "اگر «استقلال» برایتان مهم است، در پی مشاغلی باشید که:\n • در آن آزادی عمل و تصمیم‌گیری دارید،\n • می‌توانید ایده‌ها و ابتکار شخصی خود را به کار بگیرید،\n • در چارچوبی نسبتاً آزاد و منعطف کار کنید.\n\nشما در موقعیت‌های محدود‌کننده و زیر نظارت‌های شدید و مستمر احساس فشار می‌کنید.",
        },
        pishraft: {
            title: "پیشرفت",
            text: "اگر «پیشرفت» از ارزش‌های اصلی شماست، بهتر است مشاغلی را انتخاب کنید که:\n • فرصت رشد شغلی و ارتقای جایگاه در آن‌ها فراهم است،\n • اعتبار و پرستیژ اجتماعی خوبی دارند،\n • به شما امکان یادگیری، رهبری و افزایش مسئولیت می‌دهند.\n\nشغل مناسب شما، شغلی است که مسیر رشد در آن روشن باشد و بتوانید در آن حس پیشرفت و دیده شدن را تجربه کنید.\n",
        },
        ravabet: {
            title: "روابط",
            text: "اگر «روابط انسانی» از ارزش‌های مهم شماست، باید به دنبال محیط‌هایی باشید که:\n • همکاران و فضای کاری صمیمی، محترمانه و همدلانه دارند،\n • فرصت کمک کردن و خدمت‌رسانی به دیگران در آن وجود دارد.\n\nشما در محیط‌هایی که روابط انسانی سرد یا غیرصادقانه دارند، احساس نارضایتی و خستگی خواهید کرد.",
        },
        hemayat: {
            title: "حمایت",
            text: "اگر «حمایت» از ارزش‌های شماست، برایتان مهم است که:\n • مدیران رفتاری محترمانه و حمایت‌گر داشته باشند،\n • عدالت در سازمان رعایت شود،\n • روابط میان کارکنان و مدیران صمیمانه و انسانی باشد.\n\nدر محیط‌هایی که بی‌عدالتی، بی‌توجهی یا بی‌احترامی به کارکنان وجود دارد، دوام نخواهید آورد.",
        },
        sharayet_kari: {
            title: "شرایط کاری",
            text: "اگر «شرایط کاری» برای شما مهم‌ترین ارزش شغلی است، بهتر است در سازمان‌هایی فعالیت کنید که:\n• حقوق و مزایای منصفانه و مناسبی دارند،\n • امنیت شغلی و محیط کاری پایدار فراهم می‌کنند،\n • سبک کاری‌شان با روحیه و ترجیحات شما سازگار است (مثلاً ترجیح به کار گروهی یا فردی، تنوع در کارها یا برنامه‌ی منظم روزانه).\n\nشغل ایده‌آل برای شما، شغلی است که شرایط کاری آن با سبک زندگی و نوع کارکرد شما هم‌خوانی داشته باشد.",
        },
    };

    // --- State Variables ---

    // This will hold the promise from the API call
    let resultsPromise: Promise<QuizResult>;

    // This will store the final, processed, and sorted results for display
    let sortedResults: {
        key: string;
        title: string;
        score: number;
        description: string;
    }[] = [];

    let email: string;
    let first_name: string;
    let last_name: string;

    onMount(() => {
        resultsPromise = retreiveQuizAnswer({ quiz_type: "ValuTest" });
        resultsPromise
            .then((data) => {
                const entries = Object.entries(data) as [
                    keyof QuizResult,
                    number,
                ][];

                entries.sort((a, b) => b[1] - a[1]);

                sortedResults = entries.map(([key, score]) => ({
                    key,
                    title: descriptions[key]?.title || key,
                    score,
                    description: descriptions[key]?.text || "توضیحی یافت نشد.",
                }));
            })
            .catch((err) => {
                console.error("Failed to load quiz results:", err);
            });
    });

    onMount(async () => {
        try {
            const account = await retreiveAccount();

            if (account) {
                // By re-assigning these variables, we trigger the reactive 'tests' array to update.
                email = account.email;
                first_name = account.first_name;
                last_name = account.last_name;
            }
        } catch (error) {
            console.error("Failed to load user data or quizzes:", error);
        }
    });
</script>

<svelte:head>
    <title>گزارش پرسشنامه ارزش‌های شغلی</title>
</svelte:head>

<!-- Main container with styling inspired by your reference page -->
<div
    class="flex flex-col items-center justify-start min-h-screen bg-gray-100 dark:bg-slate-900 font-['Vazirmatn'] py-16"
    dir="rtl"
>
    <!-- Use #await to handle loading/error/success states -->
    {#await resultsPromise}
        <!-- PENDING: Show a loading state -->
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-10 text-center"
        >
            <h2 class="text-2xl font-bold text-slate-800 dark:text-white mb-4">
                در حال بارگذاری نتایج...
            </h2>
            <p class="text-slate-500 dark:text-slate-400">لطفا کمی صبر کنید.</p>
        </div>
    {:then data}
        <!-- SUCCESS: Show the main results card -->
        <h1>
            {first_name}
            {last_name}
            {email}
        </h1>
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 sm:p-10 transition-all duration-300"
        >
            <!-- Header section -->
            <div
                class="text-center border-b border-slate-200 dark:border-slate-700 pb-6 mb-8"
            >
                <h2
                    class="text-3xl font-bold text-slate-800 dark:text-white mb-4"
                >
                    گزارش پرسشنامه ارزش‌های شغلی
                </h2>
                <p
                    class="text-base text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed"
                >
در این پرسشنامه ارزش‌هایی که بالاترین نمره را کسب کرده‌اند، نشان‌دهنده‌ی مهم‌ترین اولویت‌های شغلی شما هستند. و ارزش‌های با امتیاز پایین‌تر اولوییت کمتری خواهند داشت.
شغل‌هایی با شما هماهنگ‌ترند که حداقل دو ارزش اصلی شما را در خود داشته باشند.
                </p>
            </div>

            <!-- Results List -->
            <div class="space-y-6">
                <!-- Loop through the sorted results and create a card for each -->
                {#each sortedResults as result, i (result.key)}
                    <!-- 
                        This 'in:fly' transition creates the "scroll effect".
                        Each card will fly in from below (y: 50) with a
                        staggered delay based on its index (i).
                    -->
                    <div
                        class="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl shadow-lg p-6 overflow-hidden"
                        in:fly={{ y: 50, duration: 600, delay: i * 150 }}
                    >
                        <!-- Card Header: Title and Score -->
                        <div
                            class="flex flex-col sm:flex-row justify-between sm:items-center gap-2 mb-4"
                        >
                            <h3
                                class="text-2xl font-semibold text-blue-600 dark:text-blue-400"
                            >
                                {i + 1}. {result.title}
                            </h3>
                            <span
                                class="text-3xl font-bold text-slate-800 dark:text-white shrink-0"
                            >
                                {result.score}
                                <span
                                    class="text-base font-medium text-slate-500 dark:text-slate-400"
                                >
                                    / 30</span
                                >
                            </span>
                        </div>

                        <!-- Progress Bar -->
                        <div
                            class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3 mb-5"
                        >
                            <div
                                class="bg-blue-600 h-3 rounded-full transition-all duration-1000 ease-out"
                                style="width: {(result.score / 30) * 100}%"
                            />
                        </div>

                        <!-- Description Text -->
                        <p
                            class="text-base text-slate-600 dark:text-slate-300 leading-relaxed whitespace-pre-line"
                        >
                            {result.description}
                        </p>
                    </div>
                {/each}
            </div>
        </div>
    {:catch error}
        <!-- ERROR: Show an error message -->
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-10 text-center"
        >
            <h2 class="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
                خطا در بارگذاری
            </h2>
            <p class="text-slate-500 dark:text-slate-400">
                متاسفانه مشکلی در دریافت نتایج پرسشنامه شما پیش آمد. لطفا صفحه را
                دوباره بارگذاری کنید.
            </p>
            <p class="text-sm text-slate-400 dark:text-slate-500 mt-2">
                {error.message}
            </p>
        </div>
    {/await}
</div>

<style>
    /* Import the Vazirmatn font, just like in your reference file */
    @import url("https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap");
    :global(body) {
        font-family: "Vazirmatn", sans-serif;
    }
</style>
