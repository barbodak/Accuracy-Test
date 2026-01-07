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
    let hasValPerm = false;
    let hasAcuPerm = false;
    let notStartedAcuText = false;
    let notStartedAcuPic = false;
    let notStartedValPic = false;
    let first_name = "";
    let last_name = "";
    $: tests = [
        {
            title: "AcuTextTest",
            isDone: isAcuTextDone,
            hasPermission: hasAcuPerm,
            notStarted: notStartedAcuText,
            startLink: "/AcuTest/Text/start",
            continueLink: "/AcuTest/Text",
        },

        {
            title: "AcuPicTest",
            isDone: isAcuPicDone,
            hasPermission: hasAcuPerm && isAcuTextDone,
            notStarted: notStartedAcuPic,
            startLink: "/AcuTest/Pic/start",
            continueLink: "/AcuTest/Pic",
        },

        {
            title: "ValuTest",
            isDone: isValuDone,
            hasPermission: hasValPerm,
            notStarted: notStartedValPic,
            startLink: "/ValuTest/start",
            continueLink: "/ValuTest",
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
                first_name = account.first_name;
                last_name = account.last_name;
            }

            const valutest = await retreiveQuiz({ quiz_type: "ValuTest" });
            const valuans = await retreiveQuizAnswer({ quiz_type: "ValuTest" });
            console.log(valuans.tofigh);
            if (valutest?.quiz_time) {
                if (valutest?.quiz_time == "not_started")
                    notStartedValPic = true;

                const now = new Date();
                const qdate = new Date(valutest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 10 * 60) isValuDone = true;
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

<div class="min-h-screen bg-slate-100">
    <header class="bg-white shadow-sm">
        <nav
            class="container mx-auto flex items-center justify-between px-6 py-4"
        >
            <a href="/" class="text-xl font-bold text-indigo-600"
                >QuizPlatform</a
            >
            <div>
                {#if getCookies("auth_token")}
                    <button
                        on:click={() => goto("/Signup")}
                        class="rounded-lg bg-indigo-600 px-4 py-2 font-semibold text-white transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                    >
                        Signup
                    </button>
                {:else}
                    <button
                        on:click={() => goto("/Signup")}
                        class="rounded-lg bg-indigo-600 px-4 py-2 font-semibold text-white transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                    >
                        Signup
                    </button>
                {/if}
            </div>
        </nav>
    </header>

    <div class="p-4 sm:p-6 lg:p-8">
        <main class="mx-auto max-w-4xl">
            <div class="mb-8 rounded-lg bg-white p-8 shadow-xl">
                <h1 class="text-3xl font-bold text-slate-800">
                    Welcome, {first_name}
                    {last_name}
                </h1>
                <p class="mt-2 text-slate-500">
                    Here are your available assessments. Please complete them as
                    required.
                </p>
            </div>

            <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:gap-8">
                {#each tests as test}
                    {#if test.hasPermission}
                        <div
                            class="flex flex-col justify-between rounded-lg bg-white p-6 shadow-lg transition-shadow duration-200 hover:shadow-xl"
                        >
                            <h2
                                class="mb-4 text-2xl font-semibold text-slate-700"
                            >
                                {test.title}
                            </h2>

                            <div class="flex-grow">
                                {#if test.isDone}
                                    <div
                                        class="rounded-lg bg-green-100 p-4 text-green-800"
                                    >
                                        <p class="font-semibold">Completed</p>
                                        <p class="text-sm">
                                            You have already taken the {test.title}.
                                        </p>
                                    </div>
                                {:else if test.hasPermission && test.notStarted}
                                    <p class="mb-4 text-slate-600">
                                        You are cleared to start this test.
                                        Please begin when you are ready.
                                    </p>
                                {:else if test.hasPermission}
                                    <p class="mb-4 text-slate-600">
                                        Continue your quiz.
                                    </p>
                                {/if}
                            </div>

                            {#if !test.isDone && test.hasPermission && test.notStarted}
                                <button
                                    class="mt-4 w-full rounded-lg bg-indigo-600 px-5 py-3 font-bold text-white transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                                    on:click={() => goto(test.startLink)}
                                >
                                    Start
                                </button>
                            {:else if !test.isDone && test.hasPermission}
                                <button
                                    class="mt-4 w-full rounded-lg bg-green-600 px-5 py-3 font-bold text-white transition-colors duration-200 hover:bg-green-700 focus:outline-none focus:ring-4 focus:ring-green-300"
                                    on:click={() => goto(test.continueLink)}
                                >
                                    Continue
                                </button>
                            {/if}
                        </div>
                    {/if}
                {/each}
            </div>
        </main>
    </div>
</div>
