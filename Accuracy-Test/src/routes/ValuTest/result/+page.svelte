<script lang="ts">
    // Import the required API function
    import { retreiveQuizAnswer } from "$lib/utils/api/quiz-apis";
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
    const descriptions: Record<keyof QuizResult, { title: string; text: string }> = {
        tofigh: {
            title: "توفیq",
            text: "اگر توفیق باالترین ارزش شغلی برای شماست، به دنبال شغل هایی باشید که کامال متناسب با نقاط قوت شما است تا بتوانید به بهترین نحو توانایی هایتان را بروز دهید. برای شما مهم است که بتوانید نتایج تالش های خود را ببینید. شغلی را انتخاب کنید که بتوانید در آن احساس موفقیت داشته باشید."
        },
        esteghlal: {
            title: "استقلال",
            text: "اگر استقالل باالترین ارزش شغلی برای شماست ،به دنبال شغل هایی باشید که در آن آزادی عمل دارید، شغلی که به شما اجازه دهد کارها را با ابتکار عمل خودتان انجام داده و در آنها بتوانید نسبتا مستقال تصمیم گیری نمایید."
        },
        pishraft: {
            title: "پیشرفت",
            text: "اگر پیشرفت باالترین ارزش شغلی برای شماست ،در جستجوی شغل هایی باشید که امکان خوبی برای ارتقای رده دارند. همچنین شغل هایی که اعتبار و پرستیژ اجتماعی خوب یا فرصت های رهبری کردن در آن ها وجود دارد مطلوب شماست."
        },
        ravabet: {
            title: "روابط",
            text: "اگر روابط باالترین ارزش شغلی برای شماست ،به دنبال شغل هایی باشید که همکارانتان افرادی گرم و صمیمی باشند. همچنین شغل هایی که برای شما این موقعیت را فراهم می کند تا به دیگران کمک یا خدمت رسانی کنید برای شما مطلوب است. شما به هیچ عنوان نمی توانید شغل هایی را که با نظام ارزش هایتان هماهنگ نیست تحمل کنید."
        },
        hemayat: {
            title: "حمایت",
            text: "اگر حمایت باالترین ارزش شغلی برای شماست؛ در شرکت هایی به دنبال شغل باشید که مدیران برای کارکنانش احترام قائل هستند و از آن ها حمایت کند. همچنین دوستانه بودن سبک رهبری مدیر ارشدتان و احساس صمیمیت با او برای شما اهمیت دارد. شما به هیچ وجه نمی توانید سازمانی را که در آن عدالت رعایت نمی شود و حقوق کارکنان ضایع می شود را تحمل کنید."
        },
        sharayet_kari: {
            title: "شرایط کاری",
            text: "اگر شرایط کاری باالترین ارزش شغلی برای شماست، مشاغل و سازمان هایی را برای کار کردن انتخاب کنید که حقوق و مزایا، امنیت شغلی و شرایط کاری خوب دارد. شغلی را انتخاب کنید که با سبک کاری شما متناسب باشد (برخی افراد دوست دارند تمام وقت سرشان شلوغ باشد، یا به تنهایی کار کنند، و یا کارهای متنوعی داشته باشند). شغل هایی را انتخاب کنید که کامال با سبک کاریتان هماهنگ باشد."
        }
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

    // --- Logic ---

    onMount(() => {
        // Start the API call when the component mounts
        resultsPromise = retreiveQuizAnswer({ quiz_type: "ValuTest" });

        // When the promise resolves, process the data
        resultsPromise.then(data => {
            // Cast is necessary because Object.entries loses the specific key type
            const entries = Object.entries(data) as [keyof QuizResult, number][];

            // Sort the results: Highest score first
            entries.sort((a, b) => b[1] - a[1]);

            // Map the sorted data to a format our template can use
            sortedResults = entries.map(([key, score]) => ({
                key,
                title: descriptions[key]?.title || key,
                score,
                description: descriptions[key]?.text || "توضیحی یافت نشد."
            }));
        }).catch(err => {
            // Handle any errors during the API call
            console.error("Failed to load quiz results:", err);
            // The UI will show an error message via the #await block
        });
    });
</script>

<svelte:head>
    <title>نتیجه آزمون ارزش‌های شغلی</title>
</svelte:head>

<!-- Main container with styling inspired by your reference page -->
<div
    class="flex flex-col items-center justify-start min-h-screen bg-gray-100 dark:bg-slate-900 font-['Vazirmatn'] py-16"
    dir="rtl"
>
    <!-- Use #await to handle loading/error/success states -->
    {#await resultsPromise}
        <!-- PENDING: Show a loading state -->
        <div class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-10 text-center">
            <h2 class="text-2xl font-bold text-slate-800 dark:text-white mb-4">
                در حال بارگذاری نتایج...
            </h2>
            <p class="text-slate-500 dark:text-slate-400">
                لطفا کمی صبر کنید.
            </p>
        </div>
    {:then data}
        <!-- SUCCESS: Show the main results card -->
        <div class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 sm:p-10 transition-all duration-300">
            
            <!-- Header section -->
            <div class="text-center border-b border-slate-200 dark:border-slate-700 pb-6 mb-8">
                <h2 class="text-3xl font-bold text-slate-800 dark:text-white mb-4">
                    نتیجه آزمون ارزش‌های شغلی
                </h2>
                <p class="text-base text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
                    سقف نمرات هر ارزش در این آزمون ۳۰ می‌باشد. باالترین نمره در
                    این ارزش ها، با اهمیت ترین ارزش شغلی شماست. شغل هایی با
                    ترجیحات شما هماهنگ است که دارای حداقل ۲ ارزشی باشد که در آن
                    باالترین نمره را کسب کردید.
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
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2 mb-4">
                            <h3 class="text-2xl font-semibold text-blue-600 dark:text-blue-400">
                                {i + 1}. {result.title}
                            </h3>
                            <span class="text-3xl font-bold text-slate-800 dark:text-white shrink-0">
                                {result.score}
                                <span class="text-base font-medium text-slate-500 dark:text-slate-400">
                                    / 30</span
                                >
                            </span>
                        </div>

                        <!-- Progress Bar -->
                        <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3 mb-5">
                            <div
                                class="bg-blue-600 h-3 rounded-full transition-all duration-1000 ease-out"
                                style="width: {(result.score / 30) * 100}%"
                            />
                        </div>

                        <!-- Description Text -->
                        <p class="text-base text-slate-600 dark:text-slate-300 leading-relaxed">
                            {result.description}
                        </p>
                    </div>
                {/each}
            </div>

        </div>
    {:catch error}
        <!-- ERROR: Show an error message -->
        <div class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-10 text-center">
            <h2 class="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
                خطا در بارگذاری
            </h2>
            <p class="text-slate-500 dark:text-slate-400">
                متاسفانه مشکلی در دریافت نتایج آزمون شما پیش آمد. لطفا صفحه را
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


