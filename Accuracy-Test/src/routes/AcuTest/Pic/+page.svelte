<script lang="ts">
    import Overlay from "../../../components/Overlay.svelte";
    import Question from "../../../components/Question.svelte";
    import { tweened } from "svelte/motion";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    let timer: any;
    let answers = Array(42).fill("0");
    let isOverlayOpen = false;
    onMount(async () => {
        try {
            const quiz = await retreiveQuiz({ quiz_type: "AcuTest_pic" });

            if (!quiz || quiz.quiz_time === "not_started") {
                console.log("Quiz not started or not found.");
                goto("/");
                return;
            }

            answers = quiz.answers.map((x: any) =>
                x === 1
                    ? "A"
                    : x === 2
                      ? "B"
                      : x === 3
                        ? "C"
                        : x === 4
                          ? "D"
                          : "0",
            );

            const quizDuration = 10 * 60; // 10 minutes in seconds
            const qdate = new Date(quiz.quiz_time);
            const now = new Date();
            const delta = now.valueOf() - qdate.valueOf();
            const timeElapsed = Math.floor(delta / 1000);

            timer = tweened(quizDuration - timeElapsed, { duration: 1000 });
        } catch (error) {
            console.error("Failed to retrieve quiz:", error);
            // Optionally, handle the error in the UI, e.g., show a message and redirect.
            goto("/");
        }
    });

    // Timer interval
    const timerInterval = setInterval(() => {
        // Svelte's $timer syntax requires the store to be subscribed to.
        // A direct check on the value is safer inside setInterval.
        if (timer && $timer > -2) {
            timer.update((t: number) => t - 1);
        }
    }, 1000);
    async function handleSubmit() {
        console.log("Handling submission...");
        let ans = answers.map((x) =>
            x === "A" ? 1 : x === "B" ? 2 : x === "C" ? 3 : x === "D" ? 4 : 0,
        );
        await submitAnswer({
            answers: ans,
            quiz_type: "AcuTest_pic",
        });
        goto("/TestEnded");
    }

    // Reactive statements to format time and handle quiz end
    $: minutes = $timer > 0 ? Math.floor($timer / 60) : 0;
    $: seconds = $timer > 0 ? Math.floor($timer - minutes * 60) : 0;
    $: if ($timer !== undefined && $timer <= 0) {
        handleSubmit();
        // Stop the interval when the timer runs out
        clearInterval(timerInterval);
    }

    // Function to format time with leading zeros
    const formatTime = (time: number) => time.toString().padStart(2, "0");
</script>

<svelte:head>
    <style>
        body {
            background-color: #f1f5f9; /* Slate 100 */
        }
    </style>
</svelte:head>

<header class="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-10">
    <nav class="container mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
            <div class="flex items-center">
                <span class="text-xl font-bold text-slate-800"
                    >Accuracy Test</span
                >
            </div>
            <div class="flex items-center space-x-4">
                <div
                    class="text-indigo-800 bg-indigo-100 font-mono text-lg font-semibold px-4 py-2 rounded-md"
                >
                    <span>{formatTime(minutes)}</span>:<span
                        >{formatTime(seconds)}</span
                    >
                </div>
                <button
                    class="text-white bg-rose-500 hover:bg-rose-600 focus:ring-4 focus:ring-rose-200 font-medium rounded-lg text-sm px-5 py-2.5 transition-colors duration-200"
                    on:click={() => {
                        isOverlayOpen = true;
                    }}
                >
                    End Test
                </button>
            </div>
        </div>
    </nav>
</header>

<main class="container mx-auto max-w-6xl p-4 sm:p-6 lg:p-8">
    <div class="grid grid-cols-1 gap-2">
        {#each answers as _, index (index)}
            <Question number={index + 1} bind:selected={answers[index]} />
        {/each}
    </div>
</main>

{#if isOverlayOpen}
    <Overlay
        on:close={() => (isOverlayOpen = false)}
        isTransparent={true}
        canBeExited={false}
    >
        <div class="text-center p-4">
            <h3 class="text-xl font-bold text-white mb-2">End the Test?</h3>
            <p class="text-slate-300 mb-6">
                Are you sure you want to end this test?
            </p>
            <div class="flex justify-center gap-4">
                <button
                    class="bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold py-2 px-6 rounded-lg transition-colors duration-200"
                    on:click={() => (isOverlayOpen = false)}
                >
                    Continue
                </button>
                <button
                    class="bg-rose-500 hover:bg-rose-600 text-white font-bold py-2 px-6 rounded-lg transition-colors duration-200"
                    on:click={handleSubmit}
                >
                    End Test
                </button>
            </div>
        </div>
    </Overlay>
{/if}
