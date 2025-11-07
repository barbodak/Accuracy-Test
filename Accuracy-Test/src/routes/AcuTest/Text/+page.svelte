<script lang="ts">
    import Overlay from "$lib/../components/Overlay.svelte";
    import QuestionText from "$lib/../components/QuestionText.svelte";
    import { tweened } from "svelte/motion";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    // CHANGE: Import the questions from the new file
    import { textQuizQuestions } from "$lib/text-quiz-questions";

    let timer: any;
    // CHANGE: Initialize answers based on the imported questions array length
    let answers = Array(textQuizQuestions.length).fill("0");
    let isOverlayOpen = false;
    let hasQuizEnded = false;

    onMount(async () => {
        try {
            const quiz = await retreiveQuiz({ quiz_type: "AcuTest_text" });
            if (!quiz || quiz.quiz_time === "not_started") {
                goto("/");
                return;
            }
            answers = quiz.answers.map((x: any) =>
                x === 1 ? "S" : x === 2 ? "D" : "0",
            );
            const quizDuration = 6 * 60; // 10 minutes
            const qdate = new Date(quiz.quiz_time);
            const now = new Date();
            const timeElapsed = Math.floor(
                (now.valueOf() - qdate.valueOf()) / 1000,
            );
            timer = tweened(quizDuration - timeElapsed, { duration: 1000 });
        } catch (error) {
            console.error("Failed to retrieve quiz:", error);
            goto("/");
        }
    });

    const timerInterval = setInterval(() => {
        if (timer && $timer > -2) {
            timer.update((t: number) => t - 1);
        }
    }, 1000);

    async function handleSubmit() {
        let ans = answers.map((x) => (x === "S" ? 1 : x === "D" ? 2 : 0));
        await submitAnswer({
            answers: ans,
            quiz_type: "AcuTest_text",
        });
    }

    $: minutes = $timer > 0 ? Math.floor($timer / 60) : 0;
    $: seconds = $timer > 0 ? Math.floor($timer - minutes * 60) : 0;
    $: if ($timer !== undefined && $timer <= 0) {
        handleSubmit();
        clearInterval(timerInterval);
        hasQuizEnded = true;
    }

    const formatTime = (time: number) => time.toString().padStart(2, "0");
</script>

<svelte:head>
    <style>
        body {
            background-color: #f1f5f9;
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
        {#each textQuizQuestions as question, index (index)}
            <QuestionText
                number={index + 1}
                bind:selected={answers[index]}
                text1={question.text1}
                text2={question.text2}
            />
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

{#if hasQuizEnded}
    <Overlay
        on:close={() => (isOverlayOpen = false)}
        isTransparent={true}
        canBeExited={false}
    >
        <div class="text-center p-4">
            <h3 class="text-xl font-bold text-white mb-2">
                your time has ended continue to the second part of this quiz
            </h3>
            <p class="text-slate-300 mb-6">go to the second part</p>
            <div class="flex justify-center gap-4">
                <button
                    class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-6 rounded-lg transition-colors duration-200"
                    on:click={() => goto("/AcuTest/Pic/start")}
                >
                    Start the second prt
                </button>
            </div>
        </div>
    </Overlay>
{/if}
