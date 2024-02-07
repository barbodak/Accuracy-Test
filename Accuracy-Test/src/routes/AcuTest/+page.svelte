<script lang="ts">
    import Overlay from "../../components/Overlay.svelte";
    import Question from "../../components/Question.svelte";
    import { tweened } from "svelte/motion";
    import { retreiveQuiz, submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    let number = 30;
    let cnt = 0;
    let timer: any;
    let ti = 0;
    let answers = Array(42).fill("0");
    let isOverlayOpen = false;

    onMount(async () => {
        const quiz = await retreiveQuiz({ quiz_type: "AcuTest" }).then(
            (quiz) => {
                console.log(quiz.quiz_info);
                if (quiz.quiz_info == "not_started") {
                    console.log("not started");
                    goto("/");
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
                        : "0"
                );
                let now = new Date();
                let qdate = new Date(quiz.quiz_info);
                let delta = now.valueOf() - qdate.valueOf();
                ti = Math.floor(delta / 1000);
                timer = tweened(5 * 60 - ti);
            }
        );
    });
    setInterval(() => {
        if ($timer > -2) $timer--;
    }, 1000);

    let submit_promise: Promise<void>;
    function handleSubmit() {
        // just because you feel it doesn't mean it's there
        // tupac
        let ans = answers.map((x) =>
            x === "A" ? 1 : x === "B" ? 2 : x === "C" ? 3 : x === "D" ? 4 : 0
        );
        submit_promise = submitAnswer({
            answers: ans,
            quiz_type: "AcuTest",
        });
    }
    $: minutes = Math.floor($timer / 60);
    $: seconds = Math.floor($timer - minutes * 60);
    $: {
        if (seconds == 0) handleSubmit();
    }
    $: {
        if (seconds == 0 && minutes == 0) {
            handleSubmit();
            console.log("submitting");
        }
    }
    $: {
        if (seconds < 0 || minutes < 0) {
            goto("/TestEnded");
        }
    }
</script>

<header class="sticky top-0">
    <nav class=" border-gray-200 px-4 lg:px-6 py-2.5 bg-blue-950 bg-blue-900">
        <div
            class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl"
        >
            <a href="#" class="flex items-center">
                <span
                    class="self-center text-2xl font-semibold whitespace-nowrap text-white"
                    >Accuracy Test</span
                >
            </a>
            <div class="flex items-center lg:order-2">
                <button
                    class="text-white focus:ring-4 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-red-950"
                    on:click={() => {
                        handleSubmit();
                        isOverlayOpen = true;
                    }}
                >
                    End Test
                </button>
            </div>
            <div
                class="hidden justify-between items-center w-full lg:flex lg:w-auto lg:order-1"
                id="mobile-menu-2 text-white"
            >
                <p
                    class="text-white p-3 rounded-3xl border-white border-2 text-lg"
                >
                    {minutes + " : " + seconds}
                </p>
            </div>
        </div>
    </nav>
</header>
{#each Array(42) as _, index (index)}
    <Question number={index + 1} bind:selected={answers[index]} />
{/each}

{#if isOverlayOpen}
    <Overlay canBeExited={false} isTransparent={true}>
        <p>
            are you sure you want to end this test? your answers are
            automatically saved and you can edit your answers until the time
            ends
        </p>
        <button
            class="bg-red-600 hover:bg-red-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
            on:click={() => {
                goto("/TestEnded");
            }}
            >End Test
        </button>
        <button
            class="bg-green-600 hover:bg-green-900 text-white font-bold py-2 px-4 rounded inline-block mt-2"
            on:click={() => {
                isOverlayOpen = false;
            }}
        >
            Continue Test</button
        >
    </Overlay>
{/if}
