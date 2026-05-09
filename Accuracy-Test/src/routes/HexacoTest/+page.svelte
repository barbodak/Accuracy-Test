<script lang="ts">
    import { hexacoQuestions } from "$lib/hexaco-data";
    import { submitAnswer } from "$lib/utils/api/quiz-apis";
    import { fly, fade } from "svelte/transition";

    let currentIndex = 0;
    let answers: Record<number, number> = {};
    let isSubmitting = false;

    $: currentQuestion = hexacoQuestions[currentIndex];
    $: allAnswered = Object.keys(answers).length === hexacoQuestions.length;
    $: hasAnsweredCurrent = answers[currentQuestion.id] !== undefined;

    // A completely chaotic pseudo-random generator.
    // This breaks the "5-color repeat" and jumps unpredictably around the 360 color wheel.
    function getQuestionHue(index: number) {
        return (
            Math.floor(Math.abs(Math.sin((index + 1) * 91.345) * 43758.5453)) %
            360
        );
    }

    // Dynamic distinct colors for the current question
    $: hue = getQuestionHue(currentIndex);
    $: bgColor = `hsl(${hue}, 85%, 85%)`; // Vibrant, exciting pastel
    $: accentColor = `hsl(${hue}, 90%, 35%)`; // Deep, rich accent
    $: hoverColor = `hsl(${hue}, 80%, 96%)`; // Very light tint for hover

    function selectAnswer(score: number) {
        answers[currentQuestion.id] = score;

        if (
            typeof window !== "undefined" &&
            window.navigator &&
            window.navigator.vibrate
        ) {
            window.navigator.vibrate(50);
        }

        if (currentIndex < hexacoQuestions.length - 1) {
            setTimeout(() => {
                nextQuestion();
            }, 250);
        }
    }

    function nextQuestion() {
        if (!hasAnsweredCurrent) return;
        if (currentIndex < hexacoQuestions.length - 1) currentIndex++;
    }

    function prevQuestion() {
        if (currentIndex > 0) currentIndex--;
    }

    // Keyboard Navigation
    function handleKeydown(event: KeyboardEvent) {
        if (["1", "2", "3", "4", "5"].includes(event.key)) {
            const choiceIndex = parseInt(event.key) - 1;
            if (currentQuestion.choices[choiceIndex]) {
                selectAnswer(currentQuestion.choices[choiceIndex].score);
            }
        }

        if (event.key === "Enter" || event.key === "ArrowLeft") {
            if (hasAnsweredCurrent && currentIndex < hexacoQuestions.length - 1)
                nextQuestion();
        }

        if (event.key === "ArrowRight") {
            prevQuestion();
        }
    }

    async function finishQuiz() {
        if (!allAnswered) {
            alert("لطفاً به تمام سؤالات پاسخ دهید.");
            return;
        }
        isSubmitting = true;
        const payload = {
            quiz_type: "HexacoTest",
            answers: Object.values(answers),
        };
        await submitAnswer(payload);
        console.log("Submitting:", payload);
        alert("آزمون با موفقیت ثبت شد!");
        isSubmitting = false;
    }
</script>

<svelte:window on:keydown={handleKeydown} />

<div
    class="page-wrapper"
    style="background-color: {bgColor}; --accent: {accentColor}; --hover-bg: {hoverColor};"
    dir="rtl"
>
    <div class="quiz-container">
        <!-- Exciting Top Header -->
        <div class="header">
            <!-- Glassmorphic Animated Pill -->
            <div class="progress-glass-pill">
                <div class="number-flipper">
                    <!-- The slot-machine animation effect for the number -->
                    {#key currentIndex}
                        <span
                            class="animated-number"
                            in:fly={{ y: -20, duration: 300, delay: 100 }}
                            out:fly={{ y: 20, duration: 300 }}
                        >
                            {currentIndex + 1}
                        </span>
                    {/key}
                </div>

                <span class="divider">از</span>
                <span class="total-number">{hexacoQuestions.length}</span>
            </div>

            <!-- Confetti-style Segmented Progress Bar -->
            <div class="progress-bar-segmented">
                {#each hexacoQuestions as _, i}
                    <div
                        class="progress-segment"
                        style="background-color: {i <= currentIndex
                            ? `hsl(${getQuestionHue(i)}, 85%, 50%)`
                            : 'transparent'}"
                    ></div>
                {/each}
            </div>
        </div>

        <!-- Question Card -->
        <div class="card-container">
            {#key currentIndex}
                <div
                    class="question-card"
                    in:fly={{ x: -40, duration: 250, delay: 150 }}
                    out:fly={{ x: 40, duration: 150 }}
                >
                    <div class="question-text-wrapper">
                        <h2>{currentQuestion.text}</h2>
                    </div>

                    <div class="choices">
                        {#each currentQuestion.choices as choice}
                            <button
                                class="choice-btn"
                                class:selected={answers[currentQuestion.id] ===
                                    choice.score}
                                on:click={() => selectAnswer(choice.score)}
                            >
                                <span class="choice-content">
                                    <span class="choice-text"
                                        >{choice.text}</span
                                    >
                                </span>
                                {#if answers[currentQuestion.id] === choice.score}
                                    <span
                                        class="check-icon"
                                        in:fade={{ duration: 150 }}>✔</span
                                    >
                                {/if}
                            </button>
                        {/each}
                    </div>
                </div>
            {/key}
        </div>

        <!-- Navigation Controls -->
        <div class="navigation">
            <button
                class="nav-btn prev-btn"
                on:click={prevQuestion}
                disabled={currentIndex === 0}
            >
                ❮ قبلی
            </button>

            {#if currentIndex === hexacoQuestions.length - 1}
                <button
                    class="finish-btn"
                    on:click={finishQuiz}
                    disabled={!allAnswered || isSubmitting}
                >
                    {isSubmitting ? "در حال ثبت..." : "پایان آزمون ✔"}
                </button>
            {:else}
                <button
                    class="nav-btn next-btn"
                    on:click={nextQuestion}
                    disabled={!hasAnsweredCurrent}
                >
                    بعدی ❯
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    .page-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        transition: background-color 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        font-family:
            system-ui,
            -apple-system,
            sans-serif;
    }

    .quiz-container {
        width: 100%;
        max-width: 650px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .header {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* --- Exciting Progress Pill --- */
    .progress-glass-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 0.6rem 1.8rem;
        border-radius: 50px;
        border: 2px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
        font-size: 1.3rem;
        font-weight: 800;
        color: #2d3748;
        margin-bottom: 1.2rem;
    }

    .pulse-icon {
        animation: pulse 2s infinite;
        margin-left: 0.3rem;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.2);
            opacity: 0.7;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    /* Slot Machine effect for numbers */
    .number-flipper {
        position: relative;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        height: 1.5em;
        width: 2.2ch; /* Keeps layout stable during flip */
        overflow: hidden;
        color: var(--accent);
        font-size: 1.5rem;
    }

    .animated-number {
        position: absolute;
        font-weight: 900;
    }

    .divider {
        font-size: 1rem;
        color: rgba(0, 0, 0, 0.4);
        margin: 0 0.2rem;
    }

    .total-number {
        color: rgba(0, 0, 0, 0.6);
    }

    /* --- Multi-Color Progress Bar --- */
    .progress-bar-segmented {
        display: flex;
        width: 100%;
        height: 12px;
        background: rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .progress-segment {
        flex: 1;
        transition: background-color 0.4s ease;
    }

    /* --- Card & Questions --- */
    .card-container {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 1fr;
        position: relative;
    }

    .question-card {
        grid-column: 1;
        grid-row: 1;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.6);
    }

    .question-text-wrapper {
        min-height: 4.8rem;
        display: flex;
        align-items: flex-start;
        margin-bottom: 2rem;
    }

    h2 {
        margin: 0;
        font-size: 1.4rem;
        line-height: 1.6;
        color: #2d3748;
        font-weight: 800;
    }

    /* --- Choices --- */
    .choices {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }

    .choice-btn {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.1rem 1.2rem;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        background: white;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 600;
        color: #4a5568;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: right;
        font-family: inherit;
    }

    .choice-content {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .choice-btn:hover {
        border-color: var(--accent);
        background: var(--hover-bg);
        transform: translateY(-2px);
    }

    .choice-btn.selected {
        border-color: var(--accent);
        background: var(--hover-bg);
        color: var(--accent);
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .check-icon {
        font-size: 1.3rem;
        color: var(--accent);
    }

    /* --- Navigation Controls --- */
    .navigation {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-btn,
    .finish-btn {
        padding: 0.9rem 1.8rem;
        border: none;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s ease;
    }

    .nav-btn.prev-btn {
        background: white;
        color: #4a5568;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .nav-btn.prev-btn:hover:not(:disabled) {
        background: #f7fafc;
        transform: translateY(-2px);
    }

    .nav-btn.next-btn {
        background: var(--accent);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .nav-btn.next-btn:hover:not(:disabled) {
        filter: brightness(1.1);
        transform: translateY(-2px);
    }

    .nav-btn:disabled {
        opacity: 0.4;
        cursor: not-allowed;
        box-shadow: none;
    }

    .finish-btn {
        background: #48bb78;
        color: white;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
    }

    .finish-btn:disabled {
        background: #cbd5e0;
        cursor: not-allowed;
        box-shadow: none;
    }
</style>
