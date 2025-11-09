<script lang="ts">
    // Import the required API function
    import {
        retreiveQuizAnswer,
        retreiveAccount,
    } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import { toJalaali } from "jalaali-js";
    import { goto } from "$app/navigation";
    import { finalize } from "$lib/utils/api/quiz-apis";

    // --- Data Definitions ---
    let form = {
        email: "",
        name: "",
        title: "",
        body: "",
    };

    let sending = false;
    let resultMsg: string | null = null;
    let errorMsg: string | null = null;

    // Define the structure of the API response
    type QuizResult = {
        sharayet_kari: number;
        hemayat: number;
        ravabet: number;
        pishraft: number;
        esteghlal: number;
        tofigh: number;
        quiz_time: string; // Add quiz_time to the type definition
    };

    async function send() {
        resultMsg = null;
        errorMsg = null;
        sending = true;
        try {
            const res = await fetch("/api/send-pdf-email", {
                method: "POST",
                headers: { "content-type": "application/json" },
                body: JSON.stringify(form),
            });
            if (!res.ok) {
                const text = await res.text();
                throw new Error(text || "Request failed");
            }
            await res.json();
            resultMsg = "Email request sent successfully.";
        } catch (e: any) {
            errorMsg = e?.message || "Failed to send.";
        } finally {
            sending = false;
        }
    }

    // Define the descriptions for each value
    // Keys MUST match the API property names
    const descriptions: Record<
        keyof QuizResult,
        { title: string; text: string }
    > = {
        tofigh: {
            title: "توفیق",
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

    let email: string = "";
    let first_name: string = "";
    let last_name: string = "";
    let age: number | null = null;
    let jalaliDate: string = "";
    let is_final: boolean;
    let sex: string = "";

    onMount(() => {
        resultsPromise = retreiveQuizAnswer({ quiz_type: "ValuTest" });
        resultsPromise
            .then((data) => {
                const quiz_time_utc = new Date(data.quiz_time);
                const y = quiz_time_utc.getUTCFullYear();
                const m = quiz_time_utc.getUTCMonth() + 1;
                const d = quiz_time_utc.getUTCDate();
                const jalaliParts = toJalaali(y, m, d);
                jalaliDate = `${jalaliParts.jy}/${jalaliParts.jm}/${jalaliParts.jd}`;

                const allEntries = Object.entries(data) as [
                    keyof QuizResult,
                    number | string, // score can be number, quiz_time is string
                ][];

                // Filter out non-score entries and ensure score is a number
                const entries = allEntries.filter(
                    ([key, value]) =>
                        key !== "quiz_time" && typeof value === "number",
                ) as [keyof Omit<QuizResult, "quiz_time">, number][]; // Cast to correct type

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
                form.email = account.email;
                form.title = `متاسان نمایشگاه کار: گزارش پرسشنامه WIL`;
                form.body = `باسپاس فراوان`;
                first_name = account.first_name;
                last_name = account.last_name;
                age = account.age;
                is_final = account.is_final;
                sex = account.sex;
            }
        } catch (error) {
            console.error("Failed to load user data or quizzes:", error);
        }

        if (is_final == false) {
            let formData = {
                first_name: first_name,
                last_name: last_name,
                age: age,
                sex: sex, // Will be 'M', 'F', or 'O'
            };
            try {
                const submitfinalize = await finalize(formData);
            } catch (e) {
                console.error("Failed to finalize account:", e);
            }
            try {
                const submitemail = await send();
            } catch (e) {
                console.error("Failed to finalize account:", e);
            }
        }
    });
</script>

<svelte:head>
    <title>گزارش پرسشنامه ارزش‌های شغلی</title>
</svelte:head>

<div
    class="flex flex-col items-center justify-start min-h-screen bg-gray-100 dark:bg-slate-900 font-['Vazirmatn'] py-16"
    dir="rtl"
>
    {#await resultsPromise}
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl p-10 text-center"
        >
            <h2 class="text-2xl font-bold text-slate-800 dark:text-white mb-4">
                در حال بارگذاری نتایج...
            </h2>
            <p class="text-slate-500 dark:text-slate-400">لطفا کمی صبر کنید.</p>
        </div>
    {:then data}
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl p-6 sm:p-10 transition-all duration-300"
        >
            <div class="flex justify-center mb-8">
                <button on:click={goto("/Signup")}>
                    <img
                        src="/images/metasan-logo-fa.svg"
                        alt="Metasan Logo"
                        class="h-16 dark:filter dark:invert"
                    />
                </button>
            </div>

            <div
                class="text-center border-b border-slate-200 dark:border-slate-700 pb-6 mb-8"
            >
                <h2
                    class="text-3xl font-bold text-slate-800 dark:text-white mb-4"
                >
                    گزارش پرسشنامه ارزش‌های شغلی
                </h2>

                <div
                    class="flex flex-col sm:flex-row justify-center items-center gap-2 sm:gap-6 text-slate-500 dark:text-slate-400 mb-6"
                >
                    {#if first_name && last_name}
                        <div class="flex items-center gap-1">
                            <span class="text-sm">نام:</span>
                            <span
                                class="font-semibold text-base text-slate-800 dark:text-slate-200"
                                >{first_name} {last_name}</span
                            >
                        </div>
                    {/if}
                    {#if age !== null}
                        {#if first_name && last_name}
                            <span
                                class="hidden sm:inline-block text-slate-400 dark:text-slate-600"
                                >|</span
                            >
                        {/if}
                        <div class="flex items-center gap-1.5">
                            <span class="text-sm">سن:</span>
                            <span
                                class="font-semibold text-base text-slate-800 dark:text-slate-200"
                                >{age}</span
                            >
                        </div>
                    {/if}
                    {#if jalaliDate}
                        {#if (first_name && last_name) || age !== null}
                            <span
                                class="hidden sm:inline-block text-slate-400 dark:text-slate-600"
                                >|</span
                            >
                        {/if}
                        <div class="flex items-center gap-1.5">
                            <span class="text-sm">تاریخ آزمون:</span>
                            <span
                                class="font-semibold text-base text-slate-800 dark:text-slate-200"
                                >{jalaliDate}</span
                            >
                        </div>
                    {/if}
                </div>
                <p
                    class="text-base text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed"
                >
                    در این پرسشنامه ارزش‌هایی که بالاترین نمره را کسب کرده‌اند،
                    نشان‌دهنده‌ی مهم‌ترین اولویت‌های شغلی شما هستند. و ارزش‌های
                    با امتیاز پایین‌تر اولوییت کمتری خواهند داشت. شغل‌هایی با
                    شما هماهنگ‌ترند که حداقل دو ارزش اصلی شما را در خود داشته
                    باشند.
                </p>
            </div>

            <div class="space-y-6">
                {#each sortedResults as result, i (result.key)}
                    <div
                        class="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl p-6 overflow-hidden"
                        in:fly={{ y: 50, duration: 600, delay: i * 150 }}
                    >
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
                                    class="text-base font-me text-slate-500 dark:text-slate-400"
                                >
                                    / 30</span
                                >
                            </span>
                        </div>

                        <div
                            class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3 mb-5"
                        >
                            <div
                                class="bg-pink-500 h-3 rounded-full transition-all duration-1000 ease-out"
                                style="width: {(result.score / 30) * 100}%"
                            />
                        </div>

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
        <div
            class="w-full max-w-3xl bg-white dark:bg-slate-800 rounded-2xl p-10 text-center"
        >
            <h2 class="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
                خطا در بارگذاری
            </h2>
            <p class="text-slate-500 dark:text-slate-400">
                متاسفانه مشکلی در دریافت نتایج پرسشنامه شما پیش آمد. لطفا صفحه
                را دوباره بارگذاری کنید.
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
