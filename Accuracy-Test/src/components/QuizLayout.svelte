<script>
    export let hue = 210;
</script>

<div
    class="page-wrapper"
    style="background: radial-gradient(circle at 20% 30%, hsl({hue}, 80%, 90%), transparent 50%), radial-gradient(circle at 80% 70%, hsl({(hue +
        60) %
        360}, 80%, 90%), transparent 50%), #f8fafc;
    rtl
    "

>
    <main class="quiz-container">
        <slot />
    </main>
</div>

<style>
    .page-wrapper {
        min-height: 100vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        box-sizing: border-box;
        transition: background-color 0.5s ease;
        /* Apply the dynamic background here */
        background: linear-gradient(135deg, hsl(var(--hue), 80%, 90%), hsl(var(--hue), 60%, 80%));
    }

    .quiz-container {
        width: 100%;
        max-width: 650px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
</style>

