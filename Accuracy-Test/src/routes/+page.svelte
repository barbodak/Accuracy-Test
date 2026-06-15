<script lang="ts">
    import { goto } from "$app/navigation";
    import {
        retreiveAccount,
        retreiveQuiz,
        retreiveQuizAnswer,
    } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { getCookies } from "$lib/utils/cookies";
    import { logout } from "$lib/utils/api/authentication";
    let isAcuTextDone = false;
    let isAcuPicDone = false;
    let isValuDone = false;
    let isHexacoDone = false;
    let isBelbinDone = false;
    let hasValPerm = false;
    let hasAcuPerm = false;
    let hasBelbinPerm = false;
    let hasHexacoPerm = false;
    let notStartedAcuText = false;
    let notStartedAcuPic = false;
    let notStartedVal = false;
    let notStartedBelbin = false;
    let notStartedHexaco = false;
    let first_name = "";
    let last_name = "";
    $: tests = [
        {
            title: "تست دقت",
            isDone: isAcuTextDone,
            hasPermission: hasAcuPerm,
            notStarted: notStartedAcuText,
            startLink: "/AcuTest/Text/start",
            continueLink: "/AcuTest/Text",
        },

        {
            title: "تست دقت - بخش دوم",
            isDone: isAcuPicDone,
            hasPermission: hasAcuPerm && isAcuTextDone,
            notStarted: notStartedAcuPic,
            startLink: "/AcuTest/Pic/start",
            continueLink: "/AcuTest/Pic",
        },

        {
            title: "پرسشنامه WIL",
            isDone: isValuDone,
            hasPermission: hasValPerm,
            notStarted: notStartedVal,
            startLink: "/ValuTest/start",
            continueLink: "/ValuTest",
        },
        {
            title: "پرسشنامه Belbin",
            isDone: isBelbinDone,
            hasPermission: hasBelbinPerm,
            notStarted: notStartedBelbin,
            startLink: "/BelbinTest/start",
            continueLink: "/BelbinTest",
        },
        {
            title: "پرسشنامه Hexaco",
            isDone: isHexacoDone,
            hasPermission: hasHexacoPerm,
            notStarted: notStartedHexaco,
            startLink: "/HexacoTest/start",
            continueLink: "/HexacoTest",
        },
    ];
    onMount(async () => {
        if (!getCookies("auth_token")) {
            goto("/Signup");
            return;
        } else {
            console.log("was here");
        }

        try {
            const account = await retreiveAccount();

            if (account) {
                // By re-assigning these variables, we trigger the reactive 'tests' array to update.
                hasValPerm = account.valuTest_permission;
                hasAcuPerm = account.acuTest_permission;
                hasBelbinPerm = account.belbinTest_permission;
                hasHexacoPerm = account.hexacoTest_permission;
                first_name = account.first_name;
                last_name = account.last_name;
            }

            const valutest = await retreiveQuiz({ quiz_type: "ValuTest" });
            if (valutest?.quiz_time) {
                if (valutest?.quiz_time == "not_started") notStartedVal = true;

                const now = new Date();
                const qdate = new Date(valutest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 1 * 60) isValuDone = true;
            }

            const belbintest = await retreiveQuiz({ quiz_type: "BelbinTest" });
            if (belbintest?.quiz_time) {
                if (belbintest?.quiz_time == "not_started")
                    notStartedBelbin = true;

                const now = new Date();
                const qdate = new Date(belbintest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 1 * 60) isBelbinDone = true;
            }

            const hexacotest = await retreiveQuiz({ quiz_type: "HexacoTest" });
            if (hexacotest?.quiz_time) {
                if (hexacotest?.quiz_time == "not_started")
                    notStartedHexaco = true;

                const now = new Date();
                const qdate = new Date(hexacotest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 1 * 60) isHexacoDone = true;
            }

            const acutest_text = await retreiveQuiz({
                quiz_type: "AcuTest_text",
            });
            if (acutest_text?.quiz_time) {
                if (acutest_text?.quiz_time == "not_started")
                    notStartedAcuText = true;
                const now = new Date();
                const qdate = new Date(acutest_text.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 6 * 60) isAcuTextDone = true;
            }
            const acutest_pic = await retreiveQuiz({
                quiz_type: "AcuTest_pic",
            });
            if (acutest_pic?.quiz_time) {
                if (acutest_pic?.quiz_time == "not_started")
                    notStartedAcuPic = true;
                const now = new Date();
                const qdate = new Date(acutest_pic.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 5 * 60) {
                    isAcuPicDone = true;
                }
            }
        } catch (error) {
            console.error("Failed to load user data or quizzes:", error);
        }
    });

    function handleLogout() {
        logout();
    }
</script>

<!-- بخش <script> خود را بدون تغییر اینجا نگه دارید -->

<div class="min-h-screen bg-slate-50 font-sans" dir="rtl">
    <!-- هدر با افکت شیشه‌ای -->
    <header
        class="sticky top-0 z-10 border-b border-slate-200 bg-white/80 backdrop-blur-md"
    >
        <nav
            class="container mx-auto flex items-center justify-between px-6 py-4"
        >
            <div class="flex items-center gap-2">
                <div class="h-3 w-3 rounded-full bg-indigo-600"></div>
                <a
                    href="/"
                    class="text-xl font-extrabold tracking-tight text-slate-800"
                    >پلتفرم پرسشنامه</a
                >
            </div>

            <button
                class="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                onclick={handleLogout}
            >
                ثبت‌نام
            </button>
        </nav>
    </header>

    <main class="container mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        <!-- بخش خوش‌آمدگویی -->
        <div
            class="relative mb-10 overflow-hidden rounded-2xl border border-indigo-100 bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-8 shadow-sm"
        >
            <div
                class="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-indigo-200/40 blur-3xl"
            ></div>

            <div class="relative z-10">
                <h1 class="mb-3 text-3xl font-extrabold text-slate-900">
                    سلام، <span class="text-indigo-600"
                        >{first_name} {last_name}</span
                    >! 👋
                </h1>
                <p class="text-lg text-slate-600">
                    به پنل کاربری خود خوش آمدید. برای ارزیابی و ادامه مسیر،
                    لطفاً پرسشنامه‌های زیر را با دقت تکمیل کنید.
                </p>
            </div>
        </div>

        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {#each tests as test}
                {#if test.hasPermission}
                    <div
                        class="group flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
                    >
                        <div class="mb-6 flex-grow">
                            <div class="flex items-center justify-between">
                                <h2
                                    class="text-xl font-bold text-slate-800 transition-colors group-hover:text-indigo-600"
                                >
                                    {test.title}
                                </h2>
                            </div>
                        </div>

                        <div class="mt-auto border-t border-slate-100 pt-4">
                            {#if test.isDone}
                                <!-- حالت تکمیل شده با آیکون تیک -->
                                <div
                                    class="flex items-center justify-center gap-2 rounded-xl border border-emerald-100 bg-emerald-50 py-3 text-sm font-semibold text-emerald-700"
                                >
                                    <svg
                                        class="h-5 w-5"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M5 13l4 4L19 7"
                                        />
                                    </svg>
                                    با موفقیت انجام شد
                                </div>
                            {:else if test.notStarted}
                                <a
                                    href={test.startLink}
                                    class="flex w-full justify-center rounded-xl bg-green-600 py-3 text-sm font-medium text-white shadow-md transition-all hover:bg-green-700 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                                >
                                    شروع پرسشنامه
                                </a>
                            {:else}
                                <a
                                    href={test.continueLink}
                                    class="flex w-full justify-center rounded-xl bg-blue-600 py-3 text-sm font-medium text-white shadow-md transition-all hover:bg-blue-700 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                                >
                                    ادامه پرسشنامه
                                </a>
                            {/if}
                        </div>
                    </div>
                {/if}
            {/each}
        </div>
    </main>
</div>
