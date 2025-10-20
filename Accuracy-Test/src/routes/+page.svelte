<script lang="ts">
    import { goto } from "$app/navigation";
    import { retreiveAccount, retreiveQuiz } from "$lib/utils/api/quiz-apis";
    import { onMount } from "svelte";
    import { userData } from "$lib/stores/userStore";
    import { logout } from "$lib/utils/api/authentication";

    let isAcuDone = false;
    let isValuDone = false;
    let hasValPerm = false;
    let hasAcuPerm = false;
    let first_name = "";
    let last_name = "";

    // This is a reactive statement. It will re-run whenever the variables it depends on change.
    // This fixes the bug where permissions were not updated correctly after the API call.
    $: tests = [
        {
            title: "AcuTest",
            isDone: isAcuDone,
            hasPermission: hasAcuPerm,
            startLink: "/AcuTest/Pic/start",
        },
        {
            title: "ValuTest",
            isDone: isValuDone,
            hasPermission: hasValPerm,
            startLink: "/ValuTest/start",
        },
    ];

    onMount(async () => {
        if (!$userData?.token) {
            goto("/Login");
            return;
        }

        try {
            const account = await retreiveAccount();
            if (account) {
                // By re-assigning these variables, we trigger the reactive 'tests' array to update.
                hasValPerm = account.valTest_permition;
                hasAcuPerm = account.acuTest_permition;
                first_name = account.first_name;
                last_name = account.last_name;
            }

            const valutest = await retreiveQuiz({ quiz_type: "ValuTest" });
            if (valutest?.quiz_time) {
                const now = new Date();
                const qdate = new Date(valutest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 180 * 60) isValuDone = true;
            }

            const acutest = await retreiveQuiz({ quiz_type: "AcuTest_text" });
            if (acutest?.quiz_time) {
                const now = new Date();
                const qdate = new Date(acutest.quiz_time);
                const delta = now.valueOf() - qdate.valueOf();
                if (Math.floor(delta / 1000) >= 5 * 60) isAcuDone = true;
            }
        } catch (error) {
            console.error("Failed to load user data or quizzes:", error);
        }
    });

    function handleLogout() {
        logout();
    }
</script>

<div class="bg-gray-100 min-h-screen">
    <!-- Header is now part of the page, not the layout -->
    <header class="bg-white shadow-md">
        <nav
            class="container mx-auto px-6 py-4 flex justify-between items-center"
        >
            <a href="/" class="text-xl font-bold text-blue-600">QuizPlatform</a>
            <div>
                {#if $userData?.token}
                    <button
                        on:click={handleLogout}
                        class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
                    >
                        Logout
                    </button>
                {:else}
                    <button
                        on:click={() => goto("/login")}
                        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
                    >
                        Login
                    </button>
                {/if}
            </div>
        </nav>
    </header>

    <div class="p-4 sm:p-6 lg:p-8">
        <main class="max-w-4xl mx-auto">
            <div class="bg-white rounded-2xl shadow-md p-8 mb-8">
                <h1 class="text-3xl font-bold text-gray-800">
                    Welcome, {first_name}
                    {last_name}
                </h1>
                <p class="text-gray-500 mt-2">
                    Here are your available assessments. Please complete them as
                    required.
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                {#each tests as test}
                    <div
                        class="bg-white rounded-2xl shadow-md p-6 flex flex-col justify-between"
                    >
                        <h2 class="text-2xl font-semibold text-gray-700 mb-4">
                            {test.title}
                        </h2>

                        <div class="flex-grow">
                            {#if test.isDone}
                                <div
                                    class="p-4 rounded-lg bg-green-100 text-green-800"
                                >
                                    <p class="font-semibold">Completed</p>
                                    <p class="text-sm">
                                        You have already taken the {test.title}.
                                    </p>
                                </div>
                            {:else if test.hasPermission}
                                <p class="text-gray-600 mb-4">
                                    You are cleared to start this test. Please
                                    begin when you are ready.
                                </p>
                            {:else}
                                <div
                                    class="p-4 rounded-lg bg-yellow-100 text-yellow-800"
                                >
                                    <p class="font-semibold">
                                        Permission Required
                                    </p>
                                    <p class="text-sm">
                                        You do not have permission to take the {test.title}
                                        yet.
                                    </p>
                                </div>
                            {/if}
                        </div>

                        {#if !test.isDone && test.hasPermission}
                            <button
                                class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-5 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 mt-4"
                                on:click={() => goto(test.startLink)}
                            >
                                Start {test.title}
                            </button>
                        {/if}
                    </div>
                {/each}
            </div>
        </main>
    </div>

    <!-- Footer is also now part of the page -->
</div>
