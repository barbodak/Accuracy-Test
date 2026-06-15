<script>
    import { onMount } from "svelte";
    import QuizLayout from "../../components/QuizLayout.svelte";
    import QuestionCard from "../../components/QuestionCard.svelte";
    import ProgressPill from "../../components/ProgressPill.svelte";

    import { hexacoQuestions } from "$lib/hexaco-data";
    import { submitAnswer } from "$lib/utils/api/quiz-apis";
    import { goto } from "$app/navigation";

    let currentIndex = 0;
    let answers = [];
    let isSubmitting = false;
    let baseHue = 210; // Default fallback
    let diraction = 1;
    let currentAnswer;
    let isTransitioning = false;

    const quizChoices = [
        { score: 5, text: "کاملاً موافقم" },
        { score: 4, text: "موافقم" },
        { score: 3, text: "نظری ندارم" },
        { score: 2, text: "مخالفم" },
        { score: 1, text: "کاملاً مخالفم" },
    ];

    onMount(() => {
        baseHue = Math.floor(Math.random() * 360);
    });

    $: currentQuestion = hexacoQuestions[currentIndex];
    $: hue = (baseHue + currentIndex * 35) % 360; // Dynamic hue updates as you progress
    $: isLastQuestion = currentIndex === hexacoQuestions.length - 1;
    $: currentAnswer = answers[currentIndex];

    function handleSelect(score) {
        if (isTransitioning) return;
        console.log(currentQuestion);
        if (navigator.vibrate) navigator.vibrate(10);

        answers[currentIndex] = score;
        answers = [...answers];
        isTransitioning = true;

        setTimeout(() => {
            if (!isLastQuestion) {
                nextQuestion();
            }
            isTransitioning = false;
        }, 200);
    }

    function nextQuestion() {
        diraction = 1;
        if (currentIndex < hexacoQuestions.length - 1) {
            currentIndex += 1;
        }
    }

    function prevQuestion() {
        diraction = -1;
        if (currentIndex > 0) {
            currentIndex -= 1;
        }
    }

    async function finishQuiz() {
        if (
            answers.length !== hexacoQuestions.length ||
            answers.includes(undefined)
        ) {
            alert("لطفا به همه سوالات پاسخ دهید.");
            return;
        }

        isSubmitting = true;
        try {
            await submitAnswer({
                quiz_type: "HexacoTest",
                answers: answers,
            });
            goto("/");
        } catch (error) {
            console.error("Submission failed:", error);
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div dir="rtl">
    <QuizLayout {hue}>
        <div class="flex justify-center mb-6">
            <ProgressPill
                current={currentIndex + 1}
                total={hexacoQuestions.length}
            />
        </div>

        <div class="grid w-full place-items-center">
            {#key currentIndex}
                <div class="col-start-1 row-start-1 w-full">
                    <QuestionCard
                        question={currentQuestion.text}
                        choices={quizChoices}
                        selectedScore={answers[currentIndex]}
                        onSelect={handleSelect}
                        animDiraction={diraction}
                        onPrev={prevQuestion}
                        onNext={isLastQuestion ? finishQuiz : nextQuestion}
                        canAdvance={currentAnswer !== undefined}
                    />
                </div>
            {/key}
        </div>

        <!-- In RTL, the first element goes to the right (Prev), the second to the left (Next/Finish) -->
        <div class="flex justify-between items-center w-full mt-8">
            <div class="flex justify-between items-center w-full mt-8">
                <!-- Prev Button -->
                <button
                    class="flex items-center gap-2 px-6 py-3 rounded-full text-base font-semibold text-slate-700 bg-white border border-slate-200 shadow-sm transition-all duration-200 hover:bg-slate-50 hover:-translate-y-0.5 hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-sm"
                    on:click={prevQuestion}
                    disabled={currentIndex === 0 || isSubmitting}
                >
                    <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                    قبلی
                </button>

                {#if isLastQuestion}
                    <!-- Finish Button -->
                    <button
                        class="flex items-center gap-2 px-8 py-3 rounded-full text-base font-semibold text-white bg-slate-900 shadow-md transition-all duration-200 hover:bg-black hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-md"
                        on:click={finishQuiz}
                        disabled={currentAnswer === undefined || isSubmitting}
                    >
                        {isSubmitting ? "در حال ثبت..." : "پایان"}
                    </button>
                {:else}
                    <!-- Next Button -->
                    <button
                        class="flex items-center gap-2 px-6 py-3 rounded-full text-base font-semibold text-slate-700 bg-white border border-slate-200 shadow-sm transition-all duration-200 hover:bg-slate-50 hover:-translate-y-0.5 hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-sm"
                        on:click={nextQuestion}
                        disabled={currentAnswer === undefined || isSubmitting}
                    >
                        بعدی
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <polyline points="15 18 9 12 15 6"></polyline>
                        </svg>
                    </button>
                {/if}
            </div>
        </div>
    </QuizLayout>
</div>
